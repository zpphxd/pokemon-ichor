"""The Euploia's open deck: MAP_TRIREME_EUPLOIA_DECK as one 24x16 scene.

The ship lies bow to the west on aethos's animated sea, seen in Ichor's
three-quarter view: the deck from above, the port (south) side of the hull
from outside, the starboard (north) bulwark from inside. The sea round her
is borrowed from aethos (trireme_lib), so it animates and costs no tiles.

  bow (west)      the bronze ram at the waterline, the painted eye, the stem
                  post curling back over a narrowing foredeck, cargo lashed
                  along both rails, the lookout's place
  amidships       the mast and the square sail (full, sagging, filling), the
                  hatch to the hold, the starboard entry port, the rail's gaps
  stern (east)    the steering oars and their tillers, the captain's
                  klepsydra, a coil of rope, the aphlaston curling forward

draw(state) returns the scene for one state of the ship; trireme_build.py
diffs the states against "base" to get the setmetatile variants:

  base     sail full, oars shipped (the crossing, the night, the ferry)
  sag      the sail hangs slack (the halcyon calm)
  fill     the sail half full (casting off; the wind coming back)
  oars     the port bank's oars out, blades in the water (rowing)
  drip     the klepsydra dripping upward (during the calm only)
  coast    the mainland on the horizon to the north-east (beat 10C)

Every texture repeats on a 16 or 32 px grid, so repeated cells share one
metatile. Pixel coordinates are absolute (x 0-383, y 0-255).
"""
from __future__ import annotations

import math

from trireme_lib import CELL, Scene

W, H = 24, 16
PW, PH = W * CELL, H * CELL

# --- the hull's outline -----------------------------------------------------
# The hull is symmetric about the boundary between x = 191 and 192: the stern's
# taper is the bow's mirrored, so draw() copies the bow's body pixels across
# and Porytiles stores the stern's curves as the bow's tiles, flipped. The
# ram, eye and stem, and the aphlaston and steering oars, are drawn after.
XB0, XS = 104, 30         # the bow's taper starts at x=104 and closes on the stem
XT0, XP = PW - 1 - XB0, PW - 1 - XS     # 279 and 353: the stern's mirror
MIRROR_W = 112            # px of the bow mirrored onto the stern (7 cells)
MAST_X = 11 * CELL + 8    # the mast's centre line (cell 11)
HATCH = (14, 7)
GAPS_N = (7, 13)          # gaps in the starboard bulwark (row 3): fishing, the entry port
GAP_S = 15                # the port side's gap with a rope ladder (row 10)
OARBOX = (120, PW - 1 - 120)            # the outrigger's extent, px (symmetric)


def _u(x):
    if x > PW / 2:
        x = PW - 1 - x
    return max(0.0, min(1.0, (XB0 - x) / (XB0 - XS)))


def deck_n(x):
    """Screen y of the deck's north edge (the foot of the starboard bulwark)."""
    return 64 + 34 * _u(x) ** 1.8


def rail_s(x):
    """Screen y of the top of the port rail: the sheer rises to bow and stern."""
    return 160 - 62 * _u(x) ** 1.55


def water_s(x):
    """Screen y of the waterline along the port side: flat amidships, sweeping
    up into the forefoot and the stern."""
    return 204 - 42 * _u(x) ** 2.2


def mirror_stern(s):
    """Copy the bow's body (bottom layer) and its water (middle) onto the stern."""
    for layer in (s.B, s.M):
        a = layer.a
        a[:, PW - MIRROR_W:] = a[:, :MIRROR_W][:, ::-1]


def hull_span(x):
    return (x > XS - 1) and (x < XP + 1)


def h(x, y, salt=0, period=32):
    """A stable pseudo-random number in [0, 1) that repeats every `period` px."""
    x %= period
    y %= period
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return (v ^ (v >> 16)) % 1000 / 1000


# ---------------------------------------------------------------------------
# The ship's body (bottom layer; the sea cells move into the middle later)
# ---------------------------------------------------------------------------

def plank(x, y):
    """Deck planks along the keel, 4 px wide, butt joints staggered on a 32 px
    repeat, in sun-bleached oak."""
    r = (y // 4) % 8                      # eight planks to the 32 px repeat
    yy = y % 4
    joint = (r * 13 + 5) % 32
    xx = (x - joint) % 32
    if yy == 3:
        return "wd1"
    if xx == 0:
        return "wd1"
    if xx == 1:
        return "pk3"
    base = "pk3" if r in (0, 5) else "pk2"
    if yy == 0:
        return "pk3" if base == "pk2" else "pk4"
    if xx in (3, 29) and yy == 1:
        return "pk1"                       # trenail
    g = h(x, y, 3)
    if g < 0.07:
        return "pk1"
    if g > 0.95:
        return "pk3" if base == "pk2" else "pk4"
    return base


def draw_body(s: Scene, state):
    B = s.B
    for x in range(PW):
        if not hull_span(x):
            continue
        n, rs, ws = deck_n(x), rail_s(x), water_s(x)
        ni, rsi, wsi = int(round(n)), int(round(rs)), int(round(ws))
        if rsi <= ni:
            continue
        # --- the deck
        for y in range(ni, rsi):
            c = plank(x, y)
            if y - ni < 2:
                c = "wd1" if y == ni else "pk1"          # shade under the bulwark
            elif y - ni == 2 and c not in ("wd1",):
                c = "pk1" if (x + y) % 2 else c
            B.px(x, y, c)
        # --- the starboard bulwark, seen from inside: rail cap, planked face
        top = ni - 16
        oar_box = OARBOX[0] <= x <= OARBOX[1]
        for y in range(top, ni):
            k = y - top
            if k <= 1:
                c = ("ink" if k == 0 else "wd0") if oar_box else None
            elif k == 2:
                c = "pk4"
            elif k == 3:
                c = "pk3"
            elif k == 4:
                c = "wd1"
            elif k in (9, 13):
                c = "wd1"
            elif k >= 14:
                c = "wd0"
            else:
                c = "pk2" if k < 9 else "pk1"
                if k in (5, 10):
                    c = "pk3" if k == 5 else "pk2"
            if c is None:
                continue
            # stanchions every 16 px
            sx = x % 16
            if k >= 5 and k <= 13 and sx in (6, 7, 8):
                c = {6: "wd1", 7: "pk3", 8: "pk1"}[sx]
            if k == 4 and sx in (6, 7, 8):
                c = "pk3" if sx == 7 else "wd1"
            B.px(x, y, c)
        # --- the port side, from outside: rail cap, bulwark with shields,
        # the oarbox, the lower hull with the wale, down to the waterline
        for y in range(rsi, wsi + 1):
            k = y - rsi
            depth = (y - rsi) / max(1, (wsi - rsi))
            if k == 0:
                c = "pk4"
            elif k == 1:
                c = "pk3"
            elif k == 2:
                c = "ink"
            else:
                c = "wd0"
                yy = y
                if oar_box:
                    # bulwark face 163-175, oarbox 176-190, hull 191-208
                    if 163 <= yy <= 175:
                        c = "wd0" if (yy - 163) % 4 != 3 else "ink"
                        if yy == 163:
                            c = "wd1"
                    elif yy == 176:
                        c = "ink"
                    elif 177 <= yy <= 178:
                        c = "pk2" if yy == 177 else "pk1"
                    elif 179 <= yy <= 188:
                        c = "wd1" if yy < 186 else "wd0"
                        px8 = x % 8
                        if 181 <= yy <= 184 and px8 in (3, 4):
                            c = "ink"                        # an oar port
                        elif 180 <= yy <= 185 and px8 in (2, 5):
                            c = "wd0"                        # its leather sleeve
                        elif yy == 179:
                            c = "pk1"
                    elif yy in (189, 190):
                        c = "ink"
                    elif 193 <= yy <= 194:
                        c = "rd" if yy == 193 else "rd0"     # the red wale
                    elif yy >= wsi - 2:
                        c = "ink"
                    elif yy == 191 or yy == 192:
                        c = "wd0"
                    else:
                        c = "ink" if yy % 4 == 3 else "wd0"
                else:
                    # bow and stern: the hull planking rising to the stem and
                    # stern post, with the wale following the sheer
                    wale = rsi + 3 + int((wsi - rsi) * 0.32)
                    if y in (wale, wale + 1):
                        c = "rd" if y == wale else "rd0"
                    elif y >= wsi - 2:
                        c = "ink"
                    elif y == rsi + 3:
                        c = "wd1"
                    elif y % 4 == 3:
                        c = "ink"                            # strakes, on the tile grid
                    else:
                        c = "wd0"
            B.px(x, y, c)
    # shields hung along the port bulwark, bronze, every 16 px
    for x0 in range(OARBOX[0] - 2, OARBOX[1] - 8, 16):
        shield(B, x0 + 2, 164)
    # outside the oarbox the bulwark's top edge meets the sea: outline it
    for x in range(PW):
        if hull_span(x) and not (OARBOX[0] <= x <= OARBOX[1]):
            B.px(x, int(round(deck_n(x))) - 15, "ink")


def shield(L, x, y):
    """A round bronze shield, 12 px, with a boss, hung on the rail."""
    rows = [
        "   kkkkk   ",
        "  kGGGggk  ",
        " kGGggggbk ",
        " kGgggggbk ",
        "kGgggkgggbk",
        "kggggkkggbk",
        " kgggggbbk ",
        " kbgggbbbk ",
        "  kbbbbbk  ",
        "   kkkkk   ",
    ]
    L.blit(rows, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, x, y)


# ---------------------------------------------------------------------------
# The bow: the stem post, the ram, the eye
# ---------------------------------------------------------------------------

def spline(pts, n=400):
    """Catmull-Rom through pts, n samples."""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    segs = len(pts) - 1
    for i in range(n):
        u = i / (n - 1) * segs
        k = min(int(u), segs - 1)
        t = u - k
        p0, p1, p2, p3 = P[k], P[k + 1], P[k + 2], P[k + 3]
        t2, t3 = t * t, t * t * t
        x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                   + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                   + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        out.append((x, y))
    return out


def tube(L, pts, w0, w1, bands):
    """A timber of width w0 tapering to w1 along the spline through pts, its
    cross-section painted from `bands` (left edge to right edge), outlined."""
    path = spline(pts)
    n = len(path)
    for i, (x, y) in enumerate(path):
        j = min(n - 1, i + 1)
        tx, ty = path[j][0] - path[max(0, i - 1)][0], path[j][1] - path[max(0, i - 1)][1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        w = w0 + (w1 - w0) * i / (n - 1)
        steps = int(w * 4) + 2
        for k in range(steps + 1):
            d = -w / 2 + w * k / steps
            u = (d + w / 2) / w
            c = bands[min(len(bands) - 1, int(u * len(bands)))]
            L.px(int(round(x + nx * d)), int(round(y + ny * d)), c)
    for i, (x, y) in enumerate(path):
        j = min(n - 1, i + 1)
        tx, ty = path[j][0] - path[max(0, i - 1)][0], path[j][1] - path[max(0, i - 1)][1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        w = w0 + (w1 - w0) * i / (n - 1)
        for d in (-w / 2 - 0.6, w / 2 + 0.6):
            xi, yi = int(round(x + nx * d)), int(round(y + ny * d))
            if L.get(xi, yi) is None or L.get(xi, yi) not in bands:
                L.px(xi, yi, "ink")
    return path


def draw_bow(s: Scene):
    B, M = s.B, s.M
    # the stem post: a heavy timber rising straight from the ram, curving back
    # over the foredeck at the top into a gilded volute
    tube(B, [(30, 168), (29, 128), (31, 90), (37, 62), (47, 50), (55, 54), (54, 63), (48, 64)],
         8, 4, ["wd1", "pk2", "pk2", "wd1", "wd0", "wd0"])
    B.blit([" kk ", "kGgk", "kgbk", " kk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 45, 60)
    # the eye (ophthalmos) on the port bow, white with a dark iris, rimmed red
    eye = [
        "    kkkkkkk     ",
        "  kkwwwwwwwkk   ",
        " krwwwkkkkwwwkk ",
        "krwwwkkwkkkwwwrk",
        "krwwwkkkkkkwwwrk",
        " krwwwkkkkwwwkk ",
        "  kkrrwwwwwrkk  ",
        "    kkkkkkkk    ",
    ]
    B.blit(eye, {"k": "ink", "w": "w0", "r": "rd"}, 54, 132)
    # the ram: a three-finned bronze beak at the waterline
    ram = [
        "               kkkkkkkkkkkkkkkkkkkkkkk",
        "        kkkkkkkGGGGGGGGGGGGGGGGGggggbk",
        "   kkkkkGGGGGGGgggggggggggggggggggbbbk",
        "kkkGGGGgggggggggkkkkkkkkkkkkkkkggbbbbk",
        "kGgggggggggggggkbbbbbbbbbbbbbbkkgbbbbk",
        " kkkkkkbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk",
        "kkkGGGGgggggggggkkkkkkkkkkkkkkkggbbbbk",
        "kGgggggggggggggkbbbbbbbbbbbbbbkkgbbbbk",
        " kkkkkkbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk",
        "kkkGGGGgggggggggkkkkkkkkkkkkkkkggbbbbk",
        "kGgggggggggggggkbbbbbbbbbbbbbbkkgbbbbk",
        " kkkkkkkbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk",
        "        kkkkkkkbbbbbbbbbbbbbbbbbbbbbbk",
        "               kkkkkkkkkkkkkkkkkkkkkkk",
    ]
    M.blit(ram, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 0, 148)
    # the proembolion: a small bronze ram above the main one
    pro = [
        "     kkkkkkk",
        "  kkkGGggggk",
        "kkGGgggggbbk",
        "  kkkbbbbbbk",
        "     kkkkkkk",
    ]
    M.blit(pro, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 18, 136)


# ---------------------------------------------------------------------------
# The stern: steering oars, tillers, the aphlaston
# ---------------------------------------------------------------------------

def draw_stern(s: Scene):
    B, M = s.B, s.M
    # the stern post, sweeping up out of the water
    for y in range(96, 156):
        t = (y - 96) / 60
        x = int(round(XP + 2 - 6 * t * t))
        for dx, c in ((-3, "ink"), (-2, "wd0"), (-1, "wd1"), (0, "pk2"), (1, "wd0"), (2, "ink")):
            B.px(x + dx, y, c)
    # the aphlaston: a plume of five timbers bound together, rising from the
    # post and curling forward over the helm, its tip gilded
    path = tube(B, [(345, 112), (356, 78), (356, 40), (343, 18), (327, 16), (320, 28), (327, 36),
                    (333, 30)],
                15, 5, ["pk3", "pk2", "wd1", "pk3", "pk2", "wd1", "pk2", "pk1", "wd1", "pk2",
                        "pk1", "wd0", "pk1", "wd0", "wd0"])
    ex, ey = path[-1]
    B.blit([" kkk ", "kGGgk", "kGgbk", "kgbbk", " kkk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"},
           int(ex) - 2, int(ey) - 2)
    for (bx, by) in ((349, 92), (352, 64)):          # bronze bands binding the timbers
        for dx in range(-7, 8):
            c = "g1" if dx < -3 else "g0" if dx < 4 else "br"
            if B.get(bx + dx, by) is not None:
                B.px(bx + dx, by, c)
                B.px(bx + dx, by + 1, "br" if c != "g1" else "g0")
    # the port steering oar: through the quarter, blade in the water
    for i in range(62):
        xi, yi = int(round(322 + i * 0.25)), int(round(130 + i * 1.05))
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "wd1"), (3, "ink")):
            M.px(xi + dx, yi, c)
    blade = [
        " kkkkk ",
        "kpPPppk",
        "kpPPppk",
        "kpPPppk",
        "kpPPppk",
        "kpPpppk",
        "kpPpppk",
        "kpPpppk",
        "kppppwk",
        " kkkkk ",
    ]
    M.blit(blade, {"k": "ink", "p": "pk2", "P": "pk3", "w": "wd1"}, 334, 186)
    # the port tiller: from the loom at the rail, inboard to a knob at (20,7)
    for y in range(116, 134):
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "wd1"), (3, "ink")):
            M.px(322 + dx, y, c)
    M.blit([" kkk ", "kpPPk", "kppPk", "kpppk", " kkk "], {"k": "ink", "p": "pk2", "P": "pk3"}, 320, 113)
    # the starboard oar: its loom over the bulwark, its tiller to a knob at (20,6)
    for i in range(24):
        xi, yi = int(round(320 + i * 0.45)), int(round(80 - i * 1.25))
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "ink")):
            M.px(xi + dx, yi, c)
    for y in range(80, 104):
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "wd1"), (3, "ink")):
            M.px(322 + dx, y, c)
    M.blit([" kkk ", "kpPPk", "kppPk", "kpppk", " kkk "], {"k": "ink", "p": "pk2", "P": "pk3"}, 320, 100)


# ---------------------------------------------------------------------------
# The rail's gaps
# ---------------------------------------------------------------------------

def draw_gaps(s: Scene):
    """Openings in the starboard bulwark (row 3) to fish from, and on the port
    side a gap with a rope ladder down the hull (row 10). Their cells become
    fishable sea in the map (MB_OCEAN_WATER)."""
    B = s.B
    for gx in GAPS_N:
        x0 = gx * CELL
        y0 = 48
        # open the bulwark: the sea shows through; keep the outrigger beam on
        # top and a lip of deck at the bottom; posts either side
        for y in range(y0 + 2, y0 + 14):
            for x in range(x0, x0 + 16):
                B.px(x, y, None)
        for x in range(x0, x0 + 16):
            B.px(x, y0 + 14, "pk3")
            B.px(x, y0 + 15, "wd1")
        for (px_, sh) in ((x0 - 1, "pk1"), (x0 + 16, "pk2")):
            for y in range(y0 + 2, y0 + 15):
                B.px(px_, y, "wd1" if y == y0 + 2 else sh)
            B.px(px_, y0 + 2, "pk4")
    # the port gap: the rail opens, a rope ladder hangs over the side
    x0 = GAP_S * CELL
    for x in range(x0 + 2, x0 + 14):
        for y in range(160, 163):
            B.px(x, y, "pk1" if y == 162 else "wd1")
    for y in range(163, 198):
        for x in (x0 + 4, x0 + 11):
            B.px(x, y, "rp")
            B.px(x + 1, y, "wd1")
        if y % 8 == 2:
            for x in range(x0 + 4, x0 + 13):
                B.px(x, y, "rp" if x not in (x0 + 4, x0 + 12) else "wd1")
    for x in range(x0 + 1, x0 + 15, 13):
        for y in range(158, 166):
            B.px(x, y, "pk3" if y == 158 else "wd1")


# ---------------------------------------------------------------------------
# On deck: the mast, the hatch, the helm, cargo, the klepsydra, rope
# ---------------------------------------------------------------------------

def draw_mast(s: Scene):
    B, M, T = s.B, s.M, s.T
    x = MAST_X - 2
    # the pole, from the deck up through the bulwark row (sail rows draw the rest)
    for y in range(48, 116):
        layer = B if y < 64 else T
        for dx, c in ((0, "ink"), (1, "pk1"), (2, "pk3"), (3, "pk2"), (4, "wd1"), (5, "ink")):
            layer.px(x + dx - 1, y, c)
    # the foot: a collar at the partners, halyards belayed round it
    foot = [
        "    kkkkkkkk    ",
        "  kkrrpPPprrkk  ",
        " krrpkpPPpkprrk ",
        "krrkrrpPPprrkrrk",
        "krkrrkpPPpkrrkrk",
        "kRkrrrpPPprrrkRk",
        "kRRkkkpPPpkkkRRk",
        " kRRRRkkkkRRRRk ",
        "  kkkRRRRRRkkk  ",
        "     kkkkkk     ",
    ]
    M.blit(foot, {"k": "ink", "r": "rp", "R": "wd1", "p": "pk2", "P": "pk3"}, 11 * CELL, 7 * CELL + 3)
    # the pole above the collar, over the foot cell's top
    for y in range(7 * CELL - 2, 7 * CELL + 4):
        for dx, c in ((0, "ink"), (1, "pk1"), (2, "pk3"), (3, "pk2"), (4, "wd1"), (5, "ink")):
            T.px(x + dx - 1, y, c)


def draw_hatch(s: Scene):
    M = s.M
    x0, y0 = HATCH[0] * CELL, HATCH[1] * CELL
    hatch = [
        " kkkkkkkkkkkkkk ",
        "kPPPPPPPPPPPPPPk",
        "kpkkkkkkkkkkkkpk",
        "kpkwwwwwwwwwwkpk",
        "kpkddddddddddkpk",
        "kpkwppppppppwkpk",
        "kpkkPPPPPPPPkkpk",
        "kpkkkkkkkkkkkkpk",
        "kpkkppppppppkkpk",
        "kpkkPPPPPPPPkkpk",
        "kpkkkkkkkkkkkkpk",
        "kpkkkppppppkkkpk",
        "kpkkkkkkkkkkkkpk",
        "kddddddddddddddk",
        "kddddddddddddddk",
        " kkkkkkkkkkkkkk ",
    ]
    M.blit(hatch, {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd0", "d": "wd1"}, x0, y0)


def draw_helm(s: Scene):
    """The helmsman's bench across the stern deck at (20, 5-7), the two
    tillers' knobs resting on it (draw_stern), and the planked stern beyond."""
    M = s.M
    bench = ["kkkkkkkkkk", "kPPPPPPPPk", "kppppppppk", "kpwwwwwwpk", "kp      pk", "kk      kk"]
    for y in (5 * CELL + 2, 6 * CELL + 10):
        pass
    for y in range(5 * CELL + 2, 8 * CELL - 2):
        for dx, c in ((0, "ink"), (1, "pk3"), (2, "pk3"), (3, "pk2"), (4, "pk2"), (5, "pk1"),
                      (6, "wd1"), (7, "ink")):
            M.px(20 * CELL + 6 + dx, y, c)
    for y in (5 * CELL + 2, 8 * CELL - 3):
        for dx in range(8):
            M.px(20 * CELL + 6 + dx, y, "ink")
    del bench


def draw_oar_bundle(s: Scene, x, y):
    """Spare oars lashed along the port rail: two cells, blades forward."""
    M = s.M
    x0, y0 = x * CELL, y * CELL
    for k, yy in enumerate((y0 + 3, y0 + 7, y0 + 11)):
        for xx in range(x0 + 2, x0 + 31):
            M.px(xx, yy - 1, "ink")
            M.px(xx, yy, "pk3")
            M.px(xx, yy + 1, "wd1")
            M.px(xx, yy + 2, "ink")
        M.blit(["kkkkkkk ", "kPPPPPPk", "kpppppPk", "kwwwwwwk", " kkkkkk "],
               {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1"}, x0, yy - 2)
    for xx in (x0 + 12, x0 + 24):
        for yy in range(y0 + 1, y0 + 15):
            M.px(xx, yy, "rp" if yy % 2 else "rp1")
            M.px(xx + 1, yy, "rp1")


def draw_grating(s: Scene, x, y):
    """A grating over the rowers' benches: light and air for the hold."""
    M = s.M
    x0, y0 = x * CELL, y * CELL
    for yy in range(y0 + 1, y0 + 15):
        for xx in range(x0 + 1, x0 + 15):
            gx, gy = (xx - x0 - 1) % 4, (yy - y0 - 1) % 4
            if xx in (x0 + 1, x0 + 14) or yy in (y0 + 1, y0 + 14):
                c = "wd1" if yy == y0 + 14 or xx == x0 + 14 else "pk3"
            elif gx == 0 or gy == 0:
                c = "pk2" if gy == 0 else "pk1"
            else:
                c = "wd0" if (gx + gy) % 3 else "ink"
            M.px(xx, yy, c)
    for xx in range(x0, x0 + 16):
        M.px(xx, y0, "ink")
        M.px(xx, y0 + 15, "ink")
    for yy in range(y0, y0 + 16):
        M.px(x0, yy, "ink")
        M.px(x0 + 15, yy, "ink")


def draw_water_jar(s: Scene, x, y):
    """The crew's water: a big two-handled jar with a ladle, lashed upright."""
    M = s.M
    jar = [
        "    kkkkkk    ",
        "   k333333k   ",
        "  kkk2222kkk  ",
        " k1k k22k k1k ",
        " k1k322221k1k ",
        "  k32222221k  ",
        " k3222222211k ",
        " k3222222211k ",
        " k3222222211k ",
        " k3222222111k ",
        "  k22222211k  ",
        "  k22222111k  ",
        "   k221111k   ",
        "    kkkkkk    ",
        "  rrrrrrrrrr  ",
    ]
    M.blit(jar, {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1", "r": "rp1"}, x * CELL + 1, y * CELL + 1)


def amphora(L, x, y):
    """A transport amphora, 7 px wide, 14 tall, standing."""
    rows = [
        "  kkk  ",
        " k3k3k ",
        "  k2k  ",
        " k322k ",
        "k32221k",
        "k32221k",
        "k32221k",
        "k22211k",
        " k2211k",
        " k2211k",
        "  k21k ",
        "  k11k ",
        "   kk  ",
        "   k   ",
    ]
    L.blit(rows, {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1"}, x, y)


def draw_cargo(s: Scene):
    M = s.M
    # amphorae lashed in a rack along the starboard bulwark at the bow:
    # (5,4) and (6,4)
    for i, x in enumerate(range(5 * CELL + 1, 7 * CELL - 4, 8)):
        amphora(M, x, 4 * CELL + 1)
    for x in range(5 * CELL, 7 * CELL):
        M.px(x, 4 * CELL + 7, "rp" if x % 3 else "rp1")         # the lashing
        M.px(x, 4 * CELL + 14, "wd1")
        M.px(x, 4 * CELL + 15, "wd0")
    for x in (5 * CELL, 7 * CELL - 1):
        for y in range(4 * CELL, 4 * CELL + 16):
            M.px(x, y, "wd1")
    # crates and a sack along the port rail at the bow: (5,9) and (6,9)
    crate = [
        "kkkkkkkkkkkkkk",
        "k33333333333wk",
        "k3k2222222k2wk",
        "k32k22222k22wk",
        "k322k222k222wk",
        "k3222k2k2222wk",
        "k32222k22222wk",
        "k3222k2k2222wk",
        "k322k222k222wk",
        "k32k22222k22wk",
        "kwwwwwwwwwwwwk",
        "kkkkkkkkkkkkkk",
    ]
    M.blit(crate, {"k": "ink", "3": "pk3", "2": "pk2", "w": "wd1"}, 5 * CELL + 1, 8 * CELL + 2)
    sack = [
        "   kk  kk   ",
        "  kssk ksk  ",
        "  kSsskssk  ",
        " kSSsssssk  ",
        "kSSssssssrk ",
        "kSsssssssrk ",
        "kSssssssrrk ",
        "kssssssrrrk ",
        " kssssrrrk  ",
        "  kkkkkkk   ",
    ]
    M.blit(sack, {"k": "ink", "S": "rp", "s": "s3", "r": "rp1"}, 6 * CELL + 2, 8 * CELL + 4)
    M.blit(crate[:8] + crate[-2:], {"k": "ink", "3": "pk3", "2": "pk2", "w": "wd1"}, 6 * CELL + 6, 8 * CELL - 2)


def draw_klepsydra(s: Scene, drip_up=False):
    """The captain's water clock at (18,4): a bronze bowl on a stand dripping
    into a second bowl below. drip_up draws the drops climbing out of the
    lower bowl into the upper one."""
    M = s.M
    x0, y0 = 19 * CELL, 4 * CELL
    k = [
        "  kkkkkkkkkkkk  ",
        " kGGGGGGGGGGggk ",
        " kbbbbbbbbbbbbk ",
        "  kgBBBBBBBggk  ",
        "   kgggggggbk   ",
        "    kkkbkkkk    ",
        "      kbk       ",
        "   m   W   m    ",
        "   m       m    ",
        "  kkkkkkkkkkkk  ",
        "  kGbbbbbbbbgk  ",
        "  kgBBBBBBBgbk  ",
        "   kgggggggbk   ",
        "   mkkkkkkkkm   ",
        "   mm      mm   ",
        "  mmm      mmm  ",
    ]
    if drip_up:
        k = list(k)
        k[5] = "    kkkbkkkk    "
        k[6] = "       W        "
        k[7] = "   m        m   "
        k[8] = "   m   W    m   "
        k[0] = "  kkkkkkkkkkkk W"
    M.blit(k, {"k": "ink", "G": "g1", "g": "g0", "b": "b1", "B": "b2", "m": "m3", "W": "b3"},
           x0, y0)


def draw_coil(s: Scene, x, y):
    M = s.M
    coil = [
        "    kkkkkkk     ",
        "  kkrrRrrrrkk   ",
        " krrkkkkkkkrrk  ",
        "krrkRrrrRrrkrrk ",
        "krkrkkkkkkkrkrk ",
        "krkrkdddddkrkrk ",
        "krkrkkkkkkkrkrk ",
        "krrkrrRrrrrkrrk ",
        " krrkkkkkkkrrk  ",
        "  kkrrrrrRrkk   ",
        "    kkkkkkkrrrk ",
        "            kkk ",
    ]
    M.blit(coil, {"k": "ink", "r": "rp", "R": "rp1", "d": "wd0"}, x * CELL, y * CELL + 2)


# ---------------------------------------------------------------------------
# The sail: three states, symmetric about the mast so its halves share tiles
# ---------------------------------------------------------------------------

SAIL_X0, SAIL_X1 = 8, 14          # cells
SAIL_HALF = 60                    # the cloth's half width in px


def draw_sail(s: Scene, state):
    """Rows 0-2 over the sea, top layer (the dark trireme passes behind it)."""
    T = s.T
    cx = MAST_X                     # the cloth is mirrored about x = cx - 0.5
    hw = SAIL_HALF
    yard_y = 6
    # the masthead and its block
    for y in range(0, 48):
        for dx, c in ((-3, "ink"), (-2, "wd1"), (-1, "pk2"), (0, "rp"), (1, "wd1"), (2, "ink")):
            T.px(cx + dx, y, c)
    # the yard, two spars fished together, tapering to the arms
    for x in range(cx - hw - 6, cx + hw + 6):
        d = abs(x - cx + 0.5)
        thick = 3 if d < hw - 10 else 2
        T.px(x, yard_y - 1, "ink")
        T.px(x, yard_y, "pk2")
        T.px(x, yard_y + 1, "wd1")
        if thick == 3:
            T.px(x, yard_y + 2, "wd0")
            T.px(x, yard_y + 3, "ink")
        else:
            T.px(x, yard_y + 2, "ink")
    # lifts from the masthead to the yardarms
    for side in (-1, 1):
        x0, y0 = cx + side * 2, 1
        x1, y1 = cx + side * (hw + 2), yard_y - 1
        T.line(x0, y0, x1, y1, "rp1")

    def foot(d):
        """The sail's bottom edge at distance d from the mast."""
        f = d / hw
        if state == "full":
            return 40 + int(round(4 * (1 - f * f)))
        if state == "fill":
            return 41 + int(round(2 * math.cos(f * math.pi * 2.5) ** 2))
        return 41 + int(round(3 * math.cos(f * math.pi * 2.5) ** 2))

    for x in range(cx - hw, cx + hw):
        d = abs(x - cx + 0.5)
        f = d / hw
        bottom = foot(d)
        for y in range(yard_y + 3, bottom + 1):
            v = (y - yard_y) / (bottom - yard_y)
            if state == "full":
                # a bellied sail, lit in the middle, shading to the leeches
                light = 1 - f ** 1.6 * 0.9 - (v - 0.45) ** 2 * 0.6
                c = "ln1" if light > 0.75 else "ln2" if light > 0.45 else "ln3"
                if f > 0.93:
                    c = "ln3"
                # brails: rope lines running down the face, bowed by the wind
                bx = d + (v * (1 - v)) * 6 * f
                if int(round(bx)) % 16 == 8:
                    c = "rp1" if c != "ln3" else "ln4"
                    if y % 8 == 4:
                        c = "wd1"                     # the brail rings
                # seams across the cloth
                if y % 8 == 0:
                    c = "ln2" if c == "ln1" else "ln3" if c == "ln2" else c
            elif state == "fill" or y < 16:
                # the head, lashed to the yard, is the same in every state;
                # filling, the sail is full to halfway and slack below
                if y < 24:
                    light = 1 - f ** 1.6 * 0.9 - (v - 0.45) ** 2 * 0.6
                    c = "ln1" if light > 0.75 else "ln2" if light > 0.45 else "ln3"
                    if f > 0.93:
                        c = "ln3"
                    bx = d + (v * (1 - v)) * 6 * f
                    if int(round(bx)) % 16 == 8:
                        c = "rp1" if c != "ln3" else "ln4"
                        if y % 8 == 4:
                            c = "wd1"
                    if y % 8 == 0:
                        c = "ln2" if c == "ln1" else "ln3" if c == "ln2" else c
                else:
                    fold = math.sin(d / hw * math.pi * 4.5)
                    c = "ln1" if fold > 0.5 else "ln2" if fold > -0.4 else "ln3"
                    if int(round(d)) % 16 == 8:
                        c = "rp1" if c != "ln3" else "ln4"
            else:
                # slack: hanging in vertical folds, darker, creased at the foot
                fold = math.sin(d / hw * math.pi * 4.5)
                c = "ln2" if fold > 0.2 else "ln3" if fold > -0.6 else "ln4"
                if v > 0.75 and fold < 0:
                    c = "ln4"
                if v < 0.15:
                    c = "ln2" if c == "ln3" else c
                if int(round(d)) % 16 == 8:
                    c = "rp1" if c == "ln2" else "ln4"
            T.px(x, y, c)
        # the bolt rope along the foot
        T.px(x, bottom + 1, "ink")
        if state != "sag":
            T.px(x, bottom, "ln4" if f > 0.2 else "ln3")
    # the red band sewn across the head
    for x in range(cx - hw + 2, cx + hw - 2):
        T.px(x, yard_y + 4, "rd")
        T.px(x, yard_y + 5, "rd0")
    # leeches (the sail's side edges)
    for y in range(yard_y + 3, foot(hw - 1) + 1):
        T.px(cx - hw, y, "ink")
        T.px(cx + hw - 1, y, "ink")
    # sheets from the clews down toward the rail
    for side in (-1, 1):
        x0 = cx + side * (hw - 1) - (1 if side > 0 else 0)
        y0 = foot(hw - 1) + 1
        if state == "sag":
            for i in range(0, 8):
                T.px(x0 + side * (i // 3), y0 + i, "rp1")
        else:
            T.line(x0, y0, x0 + side * 4, 47, "rp1")
    # the pennant at the masthead: streaming in the wind, or hanging
    if state == "full":
        T.blit(["kkkkkkk  ", "krrrrrrk ", "krRrrrrrk", "kkkkkkkk "],
               {"k": "ink", "r": "rd", "R": "rd0"}, cx + 3, 0)
    elif state == "fill":
        T.blit(["kkkkk ", "krrrrk", "krRrk ", "kkk   "], {"k": "ink", "r": "rd", "R": "rd0"},
               cx + 3, 0)
    else:
        T.blit(["kk", "kr", "kr", "kR", "kr", "kk"], {"k": "ink", "r": "rd", "R": "rd0"}, cx + 3, 0)


# ---------------------------------------------------------------------------
# The oars, run out along the port side
# ---------------------------------------------------------------------------

def draw_oars(s: Scene):
    """Shafts from the oarbox ports down past the hull into the water, a blade
    and a ripple at each; drawn over the hull (middle layer) and the sea."""
    M = s.M
    for x0 in range(OARBOX[0] + 3, OARBOX[1] - 2, 8):
        x, y = x0 + 0.5, 186.0
        while y < 236:
            xi, yi = int(round(x)), int(round(y))
            M.px(xi, yi, "pk2")
            M.px(xi + 1, yi, "wd1")
            y += 1
            x -= 0.42
        xi, yi = int(round(x)), int(round(y))
        M.blit(["kpk", "kPk", "kPk", "kpk", " k "], {"k": "ink", "p": "pk2", "P": "pk3"},
               xi - 1, yi - 3)
        M.px(xi - 2, yi + 2, "w0")
        M.px(xi + 2, yi + 2, "b2")
        M.px(xi - 3, yi + 3, "b2")
        M.px(xi + 3, yi + 3, "w0")


# ---------------------------------------------------------------------------
# The sea round the hull: shadow and foam on the water
# ---------------------------------------------------------------------------

def draw_water(s: Scene):
    M = s.M
    for x in range(XS + 4, XP - 2):
        ws = int(round(water_s(x)))
        for k in range(1, 5):
            c = "b0" if k < 3 else ("b0" if (x + k) % 2 else None)
            if c:
                M.px(x, ws + k, c)
        if x % 6 in (0, 1, 2):
            M.px(x, ws + 1, "w0" if x % 12 < 6 else "b2")


def draw_wakes(s: Scene):
    M = s.M
    # the bow wave and a little wake at the stern
    for i in range(12):
        M.px(30 - i, 166 + i // 2, "w0" if i % 3 else "b2")
        M.px(34 - i, 169 + i // 2, "b2" if i % 2 else None)
    for i in range(14):
        M.px(XP + 4 + i, 158 + i // 3, "w0" if i % 2 else "b2")


# ---------------------------------------------------------------------------
# The mainland on the horizon (beat 10C)
# ---------------------------------------------------------------------------

COAST_X0, COAST_X1 = 1, 4         # cells, rows 0-1: ahead of the bow


def draw_coast(s: Scene):
    """The mainland low on the horizon ahead of the bow (north-west): hazy
    mountains, the city on its hill, the long walls running inland, and a
    forest of masts in the harbor (middle layer over the sea, rows 0-1)."""
    M = s.M
    x0, x1 = COAST_X0 * CELL, COAST_X1 * CELL + 16
    shore = 27
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        ramp = min(1.0, t / 0.12, (1 - t) / 0.18)
        far = (9 + 4 * math.sin(t * 9.1 + 1.2) + 3 * math.sin(t * 23.0)) * ramp
        near = (5 + 3 * math.sin(t * 5.3 + 0.4)) * ramp
        ftop, ntop = int(round(shore - 6 - far)), int(round(shore - near))
        for y in range(max(0, ftop), shore):
            c = "hz3" if y == ftop else "hz1" if y < ntop else "hz2"
            if y >= ntop and y == ntop:
                c = "hz1"
            M.px(x, y, c)
    # the city on its hill: white houses and a temple front catching the sun
    for (hx, hy) in ((8, 20), (12, 19), (16, 21), (21, 20), (25, 21)):
        M.rect(x0 + hx, hy, 3, 2, "w0")
        M.px(x0 + hx + 2, hy + 1, "m3")
    M.rect(x0 + 13, 14, 9, 1, "m2")
    M.rect(x0 + 14, 13, 7, 1, "m3")
    M.rect(x0 + 13, 15, 9, 3, "w0")
    for i in range(5):
        M.px(x0 + 14 + i * 2, 16, "m3")
    # the long walls: two pale lines running inland from the harbor to the city
    for i in range(20):
        M.px(x0 + 44 - i, 25 - i // 5, "m2")
        M.px(x0 + 47 - i, 26 - i // 5, "m2")
    # a forest of masts in the harbor
    for mx in range(x0 + 40, x0 + 58, 3):
        top = 15 + (mx * 7) % 6
        for y in range(top, shore):
            M.px(mx, y, "ink" if y < shore - 2 else "m4")
        if (mx // 3) % 2:
            M.px(mx - 1, top + 2, "m4")
            M.px(mx + 1, top + 2, "m4")
    # the shoreline and the water in front
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        if min(t / 0.12, (1 - t) / 0.18) > 0.15:
            M.px(x, shore, "b3" if x % 4 else "w0")
            M.px(x, shore + 1, "b2" if x % 3 else None)


# ---------------------------------------------------------------------------
# Assembling a state
# ---------------------------------------------------------------------------

STATES = ("base", "sag", "fill", "oars", "drip", "coast")


def draw(state="base"):
    s = Scene("deck" if state == "base" else "deck_" + state, W, H)
    draw_body(s, state)
    draw_water(s)
    mirror_stern(s)
    draw_bow(s)
    draw_gaps(s)
    draw_wakes(s)
    draw_stern(s)
    draw_mast(s)
    draw_hatch(s)
    draw_helm(s)
    draw_cargo(s)
    draw_klepsydra(s, drip_up=(state == "drip"))
    draw_coil(s, 18, 9)
    draw_oar_bundle(s, 9, 9)
    draw_grating(s, 8, 6)
    draw_grating(s, 17, 6)
    draw_water_jar(s, 11, 9)
    draw_sail(s, {"sag": "sag", "fill": "fill"}.get(state, "full"))
    if state == "oars":
        draw_oars(s)
    if state == "coast":
        draw_coast(s)
    finish(s)
    walkability(s)
    return s


def finish(s: Scene):
    """Decide which cells are dry deck and which sit on borrowed sea, and move
    the art of sea cells into one layer above the water."""
    for y in range(H):
        for x in range(W):
            b = s.cell("bottom", x, y)
            if (b[..., 3] > 0).all():
                continue
            # not fully covered by the ship: it stands on the sea
            s.ground[(x, y)] = "sea"
            m, t = s.cell("middle", x, y), s.cell("top", x, y)
            if (t[..., 3] > 0).any():
                # keep the top layer (sail, aphlaston over the water): push
                # the body and middle under it
                for src in (m, b):
                    mm = (src[..., 3] > 0) & (t[..., 3] == 0)
                    t[mm] = src[mm]
                m[:] = 0
            else:
                mm = (b[..., 3] > 0) & (m[..., 3] == 0)
                m[mm] = b[mm]
            b[:] = 0
    s.flatten()


def walkability(s: Scene):
    """Collision and behaviors per cell (see trireme_lib.Scene)."""
    for y in range(H):
        for x in range(W):
            s.walk[y][x] = "~" if s.ground.get((x, y)) == "sea" else "X"
    # the deck: rows 4-9 between the bow cargo and the helm
    for y in range(4, 10):
        for x in range(2, 20):
            cx, cy = x * CELL + 8, y * CELL + 8
            if deck_n(cx) <= cy - 6 and rail_s(cx) >= cy + 6 and s.ground.get((x, y)) != "sea":
                s.walk[y][x] = "."
    for (x, y) in ((11, 7), (5, 4), (6, 4), (5, 8), (6, 8), (19, 4), (18, 9), (9, 9), (10, 9),
                   (11, 9)):
        s.walk[y][x] = "X"
    s.set_walk(*HATCH, "w", "MB_LADDER")
    for gx in GAPS_N:
        s.set_walk(gx, 3, "f", "MB_OCEAN_WATER")
    s.set_walk(GAP_S, 10, "f", "MB_OCEAN_WATER")
    # named pieces for the catalog
    s.piece("bow", "The bow: ram, eye and stem post", 0, 4, 5, 8,
            "The bronze ram at the waterline with the proembolion above it, the painted eye on "
            "the port bow, the stem post curling back into a gilded scroll, and the foredeck "
            "narrowing between the bulwarks. Walkable to x = 3.")
    s.piece("midship", "Midship cross-section", 8, 3, 2, 10,
            "Starboard bulwark from inside (row 3), the deck (rows 4-9, oak planks on a 32 px "
            "repeat), the port rail with bronze shields (row 10), the oarbox with its ports "
            "(row 11), the black hull and red wale down to the waterline (row 12), shadow and "
            "foam on the water (row 13).")
    s.piece("stern", "The stern: aphlaston, steering oars, helm", 20, 0, 4, 13,
            "The aphlaston's six timbers fanning up and curling forward with gilded tips, the "
            "port steering oar through the quarter with its blade in the water, both tillers, "
            "and the helmsman's bench at x = 20, where the tillers' knobs rest: (20,6) and (20,7). Solid.")
    s.piece("sail", "Mast and sail", SAIL_X0, 0, SAIL_X1 - SAIL_X0 + 1, 3,
            "The yard, the lifts, the square linen sail with its red head band and brails, "
            "and the pennant, on the top layer over the sea. Variants: sail_sag, sail_fill.")
    s.piece("mast", "Mast pole and foot", 11, 3, 1, 5,
            "The pole through the bulwark row and over the deck (top layer, walk behind it) "
            "and the collar at its foot with the halyards belayed. The foot (11,7) is solid.")
    s.piece("hatch", "Hatch to the hold", HATCH[0], HATCH[1], 1, 1,
            "A raised coaming round the ladder down. MB_LADDER: put the warp here.")
    s.piece("gap_starboard", "Gap in the starboard bulwark", GAPS_N[0], 3, 1, 1,
            "An opening onto the sea. MB_OCEAN_WATER, walkable collision at water "
            "elevation: face it from the deck to fish. Also at x = 13 (the entry port).")
    s.piece("gap_port", "Port gap with a rope ladder", GAP_S, 10, 1, 1,
            "The rail opens over a rope ladder down the hull. MB_OCEAN_WATER, fishable.")
    s.piece("amphorae", "Amphorae lashed in a rack", 5, 4, 2, 1, "Solid.")
    s.piece("crates", "Crates and a sack", 5, 8, 2, 1, "Solid.")
    s.piece("oars_stowed", "Spare oars lashed along the rail", 9, 9, 2, 1, "Solid.")
    s.piece("grating", "Grating over the rowers", 8, 6, 1, 1, "Walkable. Also at (17,6).")
    s.piece("water_jar", "The crew's water jar", 11, 9, 1, 1, "Solid.")
    s.piece("klepsydra", "The captain's klepsydra", 19, 4, 1, 1,
            "A bronze bowl dripping into a second bowl. Variant klepsydra_up: the drops climb.")
    s.piece("rope_coil", "A coil of rope", 18, 9, 1, 1, "Solid. The Heart Scale is hidden in it.")
