"""The Euploia's deck, refitted: MAP_EUPLOIA_DECK as one 24x12 scene.

The ship lies bow to the east on aethos's animated sea, seen in Ichor's
three-quarter view: the deck from above, the starboard (south) side of the hull
from outside, the port (north) bulwark from inside. The sea round her is
borrowed from aethos (euploia_lib), so it animates and costs no tiles.

The hull, the planking, the sail, the ram, the eye and the aphlaston are
world-act1's trireme (trireme_deck.py), redrawn bow-east and a row shorter, so
she reads as the same ship that carried the player off Kalliste. The refit
(ODYSSEY §2's diagram) adds:

  stern (west)    the steering oars and the helmsman's bench, where Nausikles
                  stands; the captain's klepsydra
  aft             the hatch down; the gangplank out over the port bulwark;
                  the chart table with Odysseus's Periplous spread on it
  amidships       the mast and the square sail; gratings over the quarters below
  forward         Poseidon's altar with its bronze trident; amphorae lashed
                  under the port bulwark; a coil of rope, the water jar
  starboard       the oarsmen's benches along the rail, their oars shipped,
                  with a gap at the rail for Lynkeus the lookout
  bow (east)      the bronze ram at the waterline, the painted eye, the stem
                  post curling back over the foredeck

Every texture repeats on a 16 or 32 px grid, so repeated cells share one
metatile. Pixel coordinates are absolute (x 0-383, y 0-191).
"""
from __future__ import annotations

import math

from euploia_lib import CELL, Scene, h

W, H = 24, 12
PW, PH = W * CELL, H * CELL

# --- the hull's outline -----------------------------------------------------
# Symmetric about x = 191.5: the bow's taper is the stern's mirrored, so draw()
# copies the stern's body pixels across and Porytiles stores the bow's curves
# as the stern's tiles, flipped. The ram, eye and stem, and the aphlaston and
# steering oars, are drawn after.
XB0, XS = 104, 30         # the stern's taper starts at x=104 and closes on the post
XT0, XP = PW - 1 - XB0, PW - 1 - XS     # 279 and 353: the bow's mirror
MIRROR_W = 112            # px of the stern mirrored onto the bow (7 cells)
MAST_X = 11 * CELL + 8    # the mast's centre line (cell 11)
OARBOX = (120, PW - 1 - 120)            # the outrigger's extent, px (symmetric)
RAISED = (112, PW - 1 - 112)            # the port bulwark's raised cap, px: under the sail

HATCH = (5, 7)            # the hatch down (warp 0, MB_LADDER)
GANGPLANK = 6             # the gangplank over the port bulwark (row 2)
CHART = (7, 4)            # the chart table, 2 wide
ALTAR = (15, 4)           # Poseidon's altar; its trident rises into row 3
HELM = 3                  # the helmsman's bench, rows 4-6
KLEPSYDRA = (4, 4)
BENCHES = [x for x in range(7, 18) if x != 13]     # row 8; Lynkeus's gap at 13
GRATINGS = ((9, 6), (14, 6))
AMPHORAE = (16, 3)        # 2 wide, under the port bulwark
COIL = (19, 6)
WATER_JAR = (18, 7)


def _u(x):
    if x > PW / 2:
        x = PW - 1 - x
    return max(0.0, min(1.0, (XB0 - x) / (XB0 - XS)))


def deck_n(x):
    """Screen y of the deck's north edge (the foot of the port bulwark)."""
    return 48 + 34 * _u(x) ** 1.8


def rail_s(x):
    """Screen y of the top of the starboard rail: the sheer rises to bow and stern."""
    return 144 - 62 * _u(x) ** 1.55


def water_s(x):
    """Screen y of the waterline along the starboard side: flat amidships,
    sweeping up into the forefoot and the stern."""
    return 186 - 40 * _u(x) ** 2.2


def mirror_bow(s):
    """Copy the stern's body (bottom layer) and its water (middle) onto the bow."""
    for layer in (s.B, s.M):
        a = layer.a
        a[:, PW - MIRROR_W:] = a[:, :MIRROR_W][:, ::-1]


def hull_span(x):
    return (x > XS - 1) and (x < XP + 1)


# ---------------------------------------------------------------------------
# The ship's body (bottom layer; the sea cells move into the middle later)
# ---------------------------------------------------------------------------

def plank(x, y):
    """Deck planks along the keel, 4 px wide, butt joints staggered on a 16 px
    repeat across and 32 down, in sun-bleached oak."""
    r = (y // 4) % 8                      # eight planks to the 32 px repeat
    yy = y % 4
    joint = (r * 5 + 3) % 16
    xx = (x - joint) % 16
    if yy == 3:
        return "wd1"
    butt = r in (1, 6)                    # long planks: only two in eight butt here
    if xx == 0 and butt:
        return "wd1"
    if xx == 1 and butt:
        return "pk3"
    base = "pk3" if r in (0, 5) else "pk2"
    if yy == 0:
        return "pk3" if base == "pk2" else "pk4"
    if xx == 3 and yy == 1:
        return "pk1"                       # trenail
    g = h(x, y, 3, 16)
    if g < 0.07:
        return "pk1"
    if g > 0.95:
        return "pk3" if base == "pk2" else "pk4"
    return base


def draw_body(s: Scene):
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
        # --- the port bulwark, seen from inside: rail cap, planked face
        top = ni - 16
        oar_box = OARBOX[0] <= x <= OARBOX[1]
        raised = RAISED[0] <= x <= RAISED[1]
        for y in range(top, ni):
            k = y - top
            if k <= 1:
                c = ("ink" if k == 0 else "wd0") if raised else None
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
            sx = x % 16                                      # stanchions every 16 px
            if 5 <= k <= 13 and sx in (6, 7, 8):
                c = {6: "wd1", 7: "pk3", 8: "pk1"}[sx]
            if k == 4 and sx in (6, 7, 8):
                c = "pk3" if sx == 7 else "wd1"
            B.px(x, y, c)
        # --- the starboard side, from outside: rail cap, bulwark with
        # shields, the oarbox, the lower hull with the wale, to the waterline
        for y in range(rsi, wsi + 1):
            k = y - rsi
            if k == 0:
                c = "pk4"
            elif k == 1:
                c = "pk3"
            elif k == 2:
                c = "ink"
            else:
                c = "wd0"
                if oar_box:
                    # bulwark face 147-159, oarbox 160-174, hull 175-186
                    if 147 <= y <= 159:
                        c = "wd0" if (y - 147) % 4 != 3 else "ink"
                        if y == 147:
                            c = "wd1"
                    elif y == 160:
                        c = "ink"
                    elif 161 <= y <= 162:
                        c = "pk2" if y == 161 else "pk1"
                    elif 163 <= y <= 172:
                        c = "wd1" if y < 170 else "wd0"
                        px8 = x % 8
                        if 165 <= y <= 168 and px8 in (3, 4):
                            c = "ink"                        # an oar port
                        elif 164 <= y <= 169 and px8 in (2, 5):
                            c = "wd0"                        # its leather sleeve
                        elif y == 163:
                            c = "pk1"
                    elif y in (173, 174):
                        c = "ink"
                    elif 177 <= y <= 178:
                        c = "rd" if y == 177 else "rd0"      # the red wale
                    elif y >= wsi - 2:
                        c = "ink"
                    elif y in (175, 176):
                        c = "wd0"
                    else:
                        c = "ink" if y % 4 == 3 else "wd0"
                else:
                    # bow and stern: the hull planking rising to the stem and
                    # stern post, the wale following the sheer
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
    # shields hung along the starboard bulwark, bronze, every 16 px
    for x0 in range(OARBOX[0] - 2, OARBOX[1] - 8, 16):
        shield(B, x0 + 2, 148)
    # outside the oarbox the bulwark's top edge meets the sea: outline it
    for x in range(PW):
        if hull_span(x) and not (RAISED[0] <= x <= RAISED[1]):
            B.px(x, int(round(deck_n(x))) - 15, "ink")


def shield(L, x, y):
    """A round bronze shield, 11 px, with a boss, hung on the rail."""
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
# Splines and timbers
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


# ---------------------------------------------------------------------------
# The bow (east): the stem post, the ram, the eye
# ---------------------------------------------------------------------------

def draw_bow(s: Scene):
    B, M = s.B, s.M
    # the stem post: a heavy timber rising straight from the ram, curving back
    # over the foredeck at the top into a gilded volute
    tube(B, [(353, 152), (354, 112), (352, 74), (346, 46), (336, 34), (328, 38), (329, 47), (335, 48)],
         8, 4, ["wd0", "wd0", "wd1", "pk2", "pk2", "wd1"])
    B.blit([" kk ", "kGgk", "kgbk", " kk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 334, 44)
    # the eye (ophthalmos) on the starboard bow, white with a dark iris, rimmed
    # red, looking ahead
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
    B.blit(eye, {"k": "ink", "w": "w0", "r": "rd"}, 312, 128, hflip=True)
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
    M.blit(ram, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, PW - 38, 132, hflip=True)
    # the proembolion: a small bronze ram above the main one
    pro = [
        "     kkkkkkk",
        "  kkkGGggggk",
        "kkGGgggggbbk",
        "  kkkbbbbbbk",
        "     kkkkkkk",
    ]
    M.blit(pro, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, PW - 30, 120, hflip=True)


# ---------------------------------------------------------------------------
# The stern (west): steering oars, tillers, the aphlaston, the helm
# ---------------------------------------------------------------------------

def draw_stern(s: Scene):
    B, M = s.B, s.M
    # the stern post, sweeping up out of the water
    for y in range(80, 140):
        t = (y - 80) / 60
        x = int(round(XS - 2 + 6 * t * t))
        for dx, c in ((-2, "ink"), (-1, "wd0"), (0, "pk2"), (1, "wd1"), (2, "wd0"), (3, "ink")):
            B.px(x + dx, y, c)
    # the aphlaston: a plume of timbers bound together, rising from the post
    # and curling forward over the helm, its tip gilded
    path = tube(B, [(38, 98), (27, 64), (27, 28), (40, 6), (56, 4), (63, 16), (56, 24), (50, 18)],
                15, 5, ["pk3", "pk2", "wd1", "pk3", "pk2", "wd1", "pk2", "pk1", "wd1", "pk2",
                        "pk1", "wd0", "pk1", "wd0", "wd0"])
    ex, ey = path[-1]
    B.blit([" kkk ", "kGGgk", "kGgbk", "kgbbk", " kkk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"},
           int(ex) - 2, int(ey) - 2)
    for (bx, by) in ((34, 76), (31, 48)):          # bronze bands binding the timbers
        for dx in range(-7, 8):
            c = "g1" if dx < -3 else "g0" if dx < 4 else "br"
            if B.get(bx + dx, by) is not None:
                B.px(bx + dx, by, c)
                B.px(bx + dx, by + 1, "br" if c != "g1" else "g0")
    # the starboard steering oar: through the quarter, blade in the water
    for i in range(56):
        xi, yi = int(round(60 - i * 0.25)), int(round(112 + i * 1.05))
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
    M.blit(blade, {"k": "ink", "p": "pk2", "P": "pk3", "w": "wd1"}, 43, 168)
    # the starboard tiller: from the loom at the rail inboard to its knob
    for y in range(94, 114):
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "wd1"), (3, "ink")):
            M.px(60 + dx, y, c)
    M.blit([" kkk ", "kpPPk", "kppPk", "kpppk", " kkk "], {"k": "ink", "p": "pk2", "P": "pk3"}, 58, 91)
    # the port oar: its loom over the far bulwark, its tiller to a knob
    for i in range(22):
        xi, yi = int(round(62 - i * 0.45)), int(round(66 - i * 1.25))
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "ink")):
            M.px(xi + dx, yi, c)
    for y in range(66, 84):
        for dx, c in ((-1, "ink"), (0, "pk3"), (1, "pk2"), (2, "wd1"), (3, "ink")):
            M.px(60 + dx, y, c)
    M.blit([" kkk ", "kpPPk", "kppPk", "kpppk", " kkk "], {"k": "ink", "p": "pk2", "P": "pk3"}, 58, 81)


def draw_helm(s: Scene):
    """The helmsman's bench across the stern deck at x = 3, rows 4-6, the two
    tillers' knobs resting on it."""
    M = s.M
    x0 = HELM * CELL + 2
    for y in range(4 * CELL + 4, 7 * CELL - 4):
        for dx, c in ((0, "ink"), (1, "pk3"), (2, "pk3"), (3, "pk2"), (4, "pk2"), (5, "pk1"),
                      (6, "wd1"), (7, "ink")):
            M.px(x0 + dx, y, c)
    for y in (4 * CELL + 4, 7 * CELL - 5):
        for dx in range(8):
            M.px(x0 + dx, y, "ink")


# ---------------------------------------------------------------------------
# On deck
# ---------------------------------------------------------------------------

def draw_mast(s: Scene):
    """The pole from under the sail down to its foot at (11,6): top layer over
    the deck (walk behind it), in the sail's colors so the cells under the sail
    stay in one palette."""
    M, T = s.M, s.T
    x = MAST_X - 2
    cols = ((0, "ink"), (1, "wd1"), (2, "rp"), (3, "pk2"), (4, "wd1"), (5, "ink"))
    for y in range(40, 6 * CELL + 4):
        for dx, c in cols:
            T.px(x + dx - 1, y, c)
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
    M.blit(foot, {"k": "ink", "r": "rp", "R": "wd1", "p": "pk2", "P": "pk3"}, 11 * CELL, 6 * CELL + 3)


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


def draw_grating(s: Scene, x, y):
    """A grating over the quarters below: light and air for the bunk and the hearth."""
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


def draw_gangplank(s: Scene):
    """The gangplank run out over the port bulwark at x = GANGPLANK: a broad
    cleated plank from the deck's edge up over the rail and away north, its
    far end with an iron ring; rope handrails on two stanchions at the rail.
    Middle layer, so the player stands in front of it."""
    M = s.M
    x0 = GANGPLANK * CELL
    top = 12
    for y in range(top, 47):
        for dx in range(2, 14):
            k = dx - 2
            c = "pk3" if k < 2 else "pk2" if k < 9 else "wd1"
            if (y - top) % 5 == 2 and 0 < k < 11:
                c = "wd1"                                   # a cleat
            elif (y - top) % 5 == 1 and 0 < k < 11:
                c = "pk4" if k < 6 else "pk3"
            M.px(x0 + dx, y, c)
        M.px(x0 + 1, y, "ink")
        M.px(x0 + 14, y, "ink")
    for dx in range(1, 15):
        M.px(x0 + dx, top - 1, "ink")
        M.px(x0 + dx, 47, "ink")
    M.blit([" kk ", "k  k", " kk "], {"k": "ink"}, x0 + 6, top + 1)   # the iron ring
    for dx in range(2, 14):                          # the plank's lip over the rail
        M.px(x0 + dx, 33, "wd0")
        M.px(x0 + dx, 34, "wd1")
    # stanchions at the rail and the rope handrails running out
    for px_ in (x0, x0 + 15):
        for y in range(20, 40):
            M.px(px_, y, "pk3" if y < 22 else "wd1")
        M.px(px_, 19, "ink")
        M.px(px_, 40, "ink")
    for y in range(top + 2, 20):
        M.px(x0 + 1 if y % 2 else x0, y, "rp")
        M.px(x0 + 14 if y % 2 else x0 + 15, y, "rp")


def draw_chart_table(s: Scene):
    """Alethea's chart table, 2 cells wide: Odysseus's Periplous spread on it,
    the coasts he knew inked in, Alethea's red corrections, and the west left
    blank; a rolled chart and a stylus. Sail colors (the papyrus is linen's)."""
    M, T = s.M, s.T
    x0, y0 = CHART[0] * CELL, CHART[1] * CELL
    # the table top, legs and apron
    for x in range(x0 + 1, x0 + 31):
        for y in range(y0 + 1, y0 + 10):
            M.px(x, y, "pk2" if (y - y0) % 4 else "wd1")
        M.px(x, y0, "ink")
        M.px(x, y0 + 10, "wd1")
        M.px(x, y0 + 11, "wd0")
        M.px(x, y0 + 12, "ink")
    for y in range(y0, y0 + 13):
        M.px(x0, y, "ink")
        M.px(x0 + 31, y, "ink")
    for lx in (x0 + 2, x0 + 3, x0 + 28, x0 + 29):
        for y in range(y0 + 13, y0 + 16):
            M.px(lx, y, "wd0" if lx in (x0 + 3, x0 + 29) else "ink")
    # the chart: papyrus, the east inked and washed blue, the west blank
    cx0, cx1, cy0, cy1 = x0 + 3, x0 + 29, y0 + 2, y0 + 9
    for x in range(cx0, cx1):
        for y in range(cy0, cy1):
            c = "ln1" if (x + y) % 7 else "ln2"
            if x > cx0 + 14:
                c = "b1" if (x + 2 * y) % 5 == 0 else ("ln2" if (x + y) % 3 else "ln1")
            M.px(x, y, c)
        M.px(x, cy1, "ln3")
    for y in range(cy0, cy1 + 1):
        M.px(cx0 - 1, y, "ln4")
        M.px(cx1, y, "ln4")
    # Aethos's coast on the east of the chart, an island or two, the route
    coast = [(cx1 - 1, cy0), (cx1 - 3, cy0 + 1), (cx1 - 4, cy0 + 2), (cx1 - 3, cy0 + 3),
             (cx1 - 5, cy0 + 4), (cx1 - 6, cy0 + 5), (cx1 - 5, cy0 + 6)]
    for (a, b) in coast:
        M.px(a, b, "ink")
    for (a, b) in ((cx0 + 18, cy0 + 2), (cx0 + 19, cy0 + 2), (cx0 + 12, cy0 + 5)):
        M.px(a, b, "ink")
    for i, (a, b) in enumerate(((cx1 - 7, cy0 + 4), (cx1 - 10, cy0 + 4), (cx0 + 14, cy0 + 3),
                                (cx0 + 10, cy0 + 3), (cx0 + 7, cy0 + 4))):
        M.px(a, b, "rd")                    # Alethea's red: the route, corrected
    # the west: blank, but for a question mark in red
    M.blit([" rr", "r  r", "  r", "  r", "", "  r"], {"r": "rd0"}, cx0 + 2, cy0)
    # weights on the corners
    for (a, b) in ((cx0, cy0 - 1), (cx1 - 2, cy0 - 1), (cx0, cy1 - 1), (cx1 - 2, cy1 - 1)):
        M.blit(["kk", "kk"], {"k": "rd0"}, a, b)
    # a rolled chart and a stylus along the back edge (top layer: walk behind)
    for x in range(x0 + 6, x0 + 24):
        T.px(x, y0 - 3, "ink")
        T.px(x, y0 - 2, "ln1" if x % 6 else "ln2")
        T.px(x, y0 - 1, "ln3")
    T.px(x0 + 5, y0 - 2, "ink")
    T.px(x0 + 24, y0 - 2, "ink")
    for i in range(4):
        T.px(x0 + 25 + i, y0 - 4 + i, "ink" if i % 3 == 0 else "wd1")


def draw_altar(s: Scene):
    """Poseidon's altar at ALTAR: a small marble block with a blue wave frieze,
    a bronze offering bowl on top, and Poseidon's trident standing behind it,
    its tines in the row above (top layer: walk behind them)."""
    M, T = s.M, s.T
    x0, y0 = ALTAR[0] * CELL, ALTAR[1] * CELL
    altar = [
        "  kkkkkkkkkkkk  ",
        "  kggGGGGGGgbk  ",
        "   kbbbbbbbbk   ",
        " kkkkkkkkkkkkkk ",
        " kwwwwwwwwwwwwk ",
        " kmmmmmmmmmmmMk ",
        " kBbBBbBBbBBbMk ",
        " kbBbbBbbBbbBMk ",
        " kmmmmmmmmmmmMk ",
        " kwmmmmmmmmmmMk ",
        " kmmmmmmmmmmmMk ",
        "kkkkkkkkkkkkkkkk",
        "kwwwwwwwwwwwwwMk",
        "kMMMMMMMMMMMMMMk",
        " kkkkkkkkkkkkkk ",
    ]
    # the trident first, so the altar's bowl stands in front of its shaft
    for y in range(y0 - 12, y0 + 4):
        layer = T if y < y0 else M
        for dx, c in ((6, "ink"), (7, "g1"), (8, "g0"), (9, "ink")):
            layer.px(x0 + dx, y, c)
    tines = [
        "k   kk   k",
        "Gk kGgk kg",
        "Gk kGgk kg",
        "Gk kGgk kg",
        "GkkkGgkkkg",
        "kGGGGggggk",
        " kkkkkkkk ",
    ]
    T.blit(tines, {"k": "ink", "G": "g1", "g": "g0"}, x0 + 3, y0 - 15)
    M.blit(altar, {"k": "ink", "w": "w0", "m": "m2", "M": "m3", "b": "b1", "B": "b2", "g": "g0",
                   "G": "g1"}, x0, y0 + 1)
    for x in range(x0 + 4, x0 + 12):            # the bowl's rim catches the light
        M.px(x, y0 + 2, "br" if x > x0 + 9 else "g0")


def bench(L, x0, y0, cushion):
    """An oarsman's bench (a thwart) along the starboard rail, a cushion on it,
    the oar shipped: its loom angled down past the rail to its port."""
    L.blit([
        " kkkkkkkkkkkkkk ",
        "kPPPPPPPPPPPPPPk",
        "kppppppppppppppk",
        "kwwwwwwwwwwwwwwk",
        "kkkkkkkkkkkkkkkk",
        " kwk        kwk ",
        " kwk        kwk ",
        " kkk        kkk ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1"}, x0, y0 + 6)
    c = ("rd", "rd0") if cushion else ("b1", "ink")
    L.blit([" kkkkkkkk ", "kccccccccC", "kCCCCCCCCk", " kkkkkkkk "], {"k": "ink", "c": c[0], "C": c[1]},
           x0 + 3, y0 + 3)
    # the loom of the shipped oar, from the handle across the bench to the rail
    for k in range(10):
        x, y = x0 + 12 + k // 3, y0 + 6 + k
        L.px(x, y, "pk3")
        L.px(x + 1, y, "wd1")
        L.px(x + 2, y, "ink")


def draw_benches(s: Scene):
    M = s.M
    for x in BENCHES:
        bench(M, x * CELL, 8 * CELL, x % 2 == 1)


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
    # amphorae lashed in a rack under the port bulwark, forward
    x0, y0 = AMPHORAE[0] * CELL, AMPHORAE[1] * CELL
    for x in range(x0 + 1, x0 + 28, 8):
        amphora(M, x, y0 + 1)
    for x in range(x0, x0 + 32):
        M.px(x, y0 + 7, "rp" if x % 3 else "rp1")         # the lashing
        M.px(x, y0 + 14, "wd1")
        M.px(x, y0 + 15, "wd0")
    for x in (x0, x0 + 31):
        for y in range(y0, y0 + 16):
            M.px(x, y, "wd1")
    water_jar(M, *WATER_JAR)
    rope_coil(M, *COIL)


def water_jar(M, cx, cy):
    """The crew's water jar, lashed upright, in cell (cx, cy). Below deck draws
    the same one, so its tiles are shared."""
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
    M.blit(jar, {"k": "ink", "3": "tc3", "2": "tc2", "1": "tc1", "r": "rp1"}, cx * CELL + 1, cy * CELL + 1)


def rope_coil(M, cx, cy):
    """A coil of rope in cell (cx, cy); shared with below deck."""
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
    M.blit(coil, {"k": "ink", "r": "rp", "R": "rp1", "d": "wd0"}, cx * CELL, cy * CELL + 2)


def draw_klepsydra(s: Scene):
    """The captain's water clock by the helm: a bronze bowl on a stand
    dripping into a second bowl below."""
    M = s.M
    x0, y0 = KLEPSYDRA[0] * CELL, KLEPSYDRA[1] * CELL
    k = [
        "  kkkkkkkkkkkk  ",
        " kGGGGGGGGGGggk ",
        " kbbbbbbbbbbbbk ",
        "  kgBBBBBBBggk  ",
        "   kgggggggbk   ",
        "    kkkbkkkk    ",
        "      kbk       ",
        "   k   W   k    ",
        "   k       k    ",
        "  kkkkkkkkkkkk  ",
        "  kGbbbbbbbbgk  ",
        "  kgBBBBBBBgbk  ",
        "   kgggggggbk   ",
        "   kkkkkkkkkk   ",
        "   kk      kk   ",
        "  kkk      kkk  ",
    ]
    M.blit(k, {"k": "ink", "G": "g1", "g": "g0", "b": "b1", "B": "b2", "W": "b3"}, x0, y0)


# ---------------------------------------------------------------------------
# The sail: symmetric about the mast so its halves share tiles
# ---------------------------------------------------------------------------

SAIL_HALF = 60                    # the cloth's half width in px


def draw_sail(s: Scene):
    """Rows 0-1 over the sea and the top of the port bulwark, top layer."""
    T = s.T
    cx = MAST_X
    hw = SAIL_HALF
    yard_y = 4
    for y in range(0, 40):                            # the masthead
        for dx, c in ((-3, "ink"), (-2, "wd1"), (-1, "pk2"), (0, "rp"), (1, "wd1"), (2, "ink")):
            T.px(cx + dx, y, c)
    for x in range(cx - hw - 6, cx + hw + 6):         # the yard
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
    for side in (-1, 1):                              # lifts to the yardarms
        T.line(cx + side * 2, 0, cx + side * (hw + 2), yard_y - 1, "rp1")

    def foot(d):
        f = d / hw
        return 36 + int(round(4 * (1 - f * f)))

    for x in range(cx - hw, cx + hw):
        d = abs(x - cx + 0.5)
        f = d / hw
        bottom = foot(d)
        for y in range(yard_y + 3, bottom + 1):
            v = (y - yard_y) / (bottom - yard_y)
            # a bellied sail, lit in the middle, shading to the leeches
            light = 1 - f ** 1.6 * 0.9 - (v - 0.45) ** 2 * 0.6
            c = "ln1" if light > 0.75 else "ln2" if light > 0.45 else "ln3"
            if f > 0.93:
                c = "ln3"
            bx = d + (v * (1 - v)) * 6 * f          # brails, bowed by the wind
            if int(round(bx)) % 16 == 8:
                c = "rp1" if c != "ln3" else "ln4"
                if y % 8 == 4:
                    c = "wd1"
            if y % 8 == 0:                          # seams
                c = "ln2" if c == "ln1" else "ln3" if c == "ln2" else c
            T.px(x, y, c)
        T.px(x, bottom + 1, "ink")
        T.px(x, bottom, "ln4" if f > 0.2 else "ln3")
    for x in range(cx - hw + 2, cx + hw - 2):         # the red head band
        T.px(x, yard_y + 4, "rd")
        T.px(x, yard_y + 5, "rd0")
    for y in range(yard_y + 3, foot(hw - 1) + 1):     # leeches
        T.px(cx - hw, y, "ink")
        T.px(cx + hw - 1, y, "ink")
    for side in (-1, 1):                              # sheets down to the rail
        x0 = cx + side * (hw - 1) - (1 if side > 0 else 0)
        y0 = foot(hw - 1) + 1
        T.line(x0, y0, x0 + side * 3, 47, "rp1")
    # the pennant at the masthead, streaming east before a fair wind
    T.blit(["kkkkkkk  ", "krrrrrrk ", "krRrrrrrk", "kkkkkkkk "], {"k": "ink", "r": "rd", "R": "rd0"},
           cx + 3, 0)


# ---------------------------------------------------------------------------
# The sea round the hull: shadow and foam on the water
# ---------------------------------------------------------------------------

def draw_water(s: Scene):
    M = s.M
    for x in range(XS + 4, XP - 2):
        ws = int(round(water_s(x)))
        for k in range(1, 5):
            c = "b0" if k < 3 else ("b0" if (x + k) % 2 else None)
            if c and ws + k < PH:
                M.px(x, ws + k, c)
        if x % 8 in (0, 1, 2):
            M.px(x, ws + 1, "w0" if x % 16 < 8 else "b2")


def draw_wakes(s: Scene):
    M = s.M
    # the bow wave at the stem (east) and a little wake at the stern (west)
    for i in range(12):
        M.px(PW - 31 + i, 150 + i // 2, "w0" if i % 3 else "b2")
        M.px(PW - 35 + i, 153 + i // 2, "b2" if i % 2 else None)
    for i in range(14):
        M.px(XS - 5 - i, 142 + i // 3, "w0" if i % 2 else "b2")


# ---------------------------------------------------------------------------
# Assembling the deck
# ---------------------------------------------------------------------------

def draw():
    s = Scene("deck", W, H)
    draw_body(s)
    draw_water(s)
    mirror_bow(s)
    draw_bow(s)
    draw_wakes(s)
    draw_stern(s)
    draw_mast(s)
    draw_hatch(s)
    draw_helm(s)
    draw_cargo(s)
    draw_klepsydra(s)
    for (x, y) in GRATINGS:
        draw_grating(s, x, y)
    draw_benches(s)
    draw_chart_table(s)
    draw_altar(s)
    draw_gangplank(s)
    draw_sail(s)
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
            s.ground[(x, y)] = "sea"
            m, t = s.cell("middle", x, y), s.cell("top", x, y)
            if (t[..., 3] > 0).any():
                for src in (m, b):
                    mm = (src[..., 3] > 0) & (t[..., 3] == 0)
                    t[mm] = src[mm]
                m[:] = 0
            else:
                mm = (b[..., 3] > 0) & (m[..., 3] == 0)
                m[mm] = b[mm]
            b[:] = 0
    s.flatten()


SOLID = [(HELM, 4), (HELM, 5), (HELM, 6), KLEPSYDRA, CHART, (CHART[0] + 1, CHART[1]), (11, 6),
         ALTAR, AMPHORAE, (AMPHORAE[0] + 1, AMPHORAE[1]), COIL, WATER_JAR] + [(x, 8) for x in BENCHES]


def walkability(s: Scene):
    """Collision and behaviors per cell (see euploia_lib.Scene)."""
    for y in range(H):
        for x in range(W):
            s.walk[y][x] = "~" if s.ground.get((x, y)) == "sea" else "X"
    for y in range(3, 9):
        for x in range(2, 22):
            cx, cy = x * CELL + 8, y * CELL + 8
            if deck_n(cx) <= cy - 6 and rail_s(cx) >= cy + 6 and s.ground.get((x, y)) != "sea":
                s.walk[y][x] = "."
    for (x, y) in SOLID:
        s.walk[y][x] = "X"
    s.set_walk(*HATCH, "w", "MB_LADDER")
    # named pieces for the catalog
    s.piece("bow", "The bow: ram, eye and stem post", 19, 2, 5, 9,
            "The bronze ram at the waterline with the proembolion above it, the painted eye on "
            "the starboard bow, the stem post curling back into a gilded scroll, and the foredeck "
            "narrowing between the bulwarks. Walkable to x = 21 (row 5).")
    s.piece("midship", "Midship cross-section", 9, 2, 2, 10,
            "Port bulwark from inside (row 2), the deck (rows 3-8, oak planks on a 32 px repeat), "
            "the starboard rail with bronze shields (row 9), the oarbox with its ports (row 10), "
            "the black hull and red wale down to the waterline (row 11).")
    s.piece("stern", "The stern: aphlaston, steering oars, helm", 0, 0, 4, 12,
            "The aphlaston's timbers rising and curling forward with a gilded tip, the starboard "
            "steering oar through the quarter with its blade in the water, the port oar's loom "
            "over the far bulwark, both tillers resting on the helmsman's bench at x = 3 "
            "(rows 4-6, solid). Nausikles stands at (4,5).")
    s.piece("sail", "Mast and sail", 7, 0, 10, 3,
            "The yard, the lifts, the square linen sail with its red head band and brails, and "
            "the pennant, on the top layer over the sea and the port bulwark.")
    s.piece("mast", "Mast pole and foot", 11, 3, 1, 4,
            "The pole over the deck (top layer, walk behind it) and the collar at its foot with "
            "the halyards belayed. The foot (11,6) is solid.")
    s.piece("hatch", "Hatch down", HATCH[0], HATCH[1], 1, 1,
            "A raised coaming round the ladder down. MB_LADDER: warp 0, to below deck's ladder.")
    s.piece("gangplank", "The gangplank", GANGPLANK, 0, 1, 3,
            "Run out over the port bulwark and away north over the water, cleated, with rope "
            "handrails. Solid; its bg event at (6,2) runs EventScript_IchorLeaveShip, read from (6,3).")
    s.piece("chart_table", "Alethea's chart table", CHART[0], CHART[1] - 1, 2, 2,
            "Odysseus's Periplous spread on the table: the east inked and washed blue, Alethea's "
            "corrections in red, the west blank but for a question mark. A rolled chart and a "
            "stylus on the back edge (top layer). The table (row 4) is solid.")
    s.piece("altar", "Poseidon's altar", ALTAR[0], ALTAR[1] - 1, 1, 2,
            "A marble block with a blue wave frieze and a bronze bowl, the bronze trident standing "
            "behind it with its tines in the row above (top layer). The altar (15,4) is solid.")
    s.piece("benches", "The oarsmen's benches", 7, 8, 2, 1,
            "A thwart along the starboard rail with a cushion (red and blue alternating) and the "
            "oar shipped, its loom angled down past the rail. Row 8, x = 7-12 and 14-17. Solid.")
    s.piece("rail_gap", "The rail where Lynkeus watches", 13, 8, 1, 2,
            "No bench at x = 13: Lynkeus stands at the rail at (13,8).")
    s.piece("grating", "Grating over the quarters below", GRATINGS[0][0], GRATINGS[0][1], 1, 1,
            "Walkable. Also at (14,6).")
    s.piece("amphorae", "Amphorae lashed in a rack", AMPHORAE[0], AMPHORAE[1], 2, 1, "Solid.")
    s.piece("water_jar", "The crew's water jar", WATER_JAR[0], WATER_JAR[1], 1, 1, "Solid.")
    s.piece("klepsydra", "The captain's klepsydra", KLEPSYDRA[0], KLEPSYDRA[1], 1, 1,
            "A bronze bowl dripping into a second bowl, by the helm. Solid.")
    s.piece("rope_coil", "A coil of rope", COIL[0], COIL[1], 1, 1, "Solid.")
