"""Ariadne line: Mitoclew (Normal). Ariadne's clew, the ball of thread that
led Theseus out of the Labyrinth, under the crown Dionysus set in the stars."""
import math

import numpy as np

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Mitoclew, the living clew
# --------------------------------------------------------------------------

MITOCLEW_COLORS = [
    ("ink", INK),
    # terracotta-red thread, dark winding lines to a sunlit sheen
    ("thr0", (96, 24, 24)), ("thr1", (144, 40, 32)), ("thr2", (192, 72, 48)), ("thr3", (232, 120, 80)),
    ("thr4", (248, 176, 136)),
    # the dark inside of the ball, where the eyes peek out
    ("deep", (56, 16, 24)),
    # Corona Borealis: sun-gold stars
    ("gold0", (184, 120, 32)), ("gold1", (240, 192, 64)), ("gold2", (248, 240, 168)),
    # the shine in its bright eyes
    ("white", C.white),
]
MITOCLEW_SHINY = {
    # Aegean-blue thread, silver-white stars
    "thr0": (24, 40, 96), "thr1": (32, 72, 144), "thr2": (48, 104, 184), "thr3": (96, 152, 216),
    "thr4": (168, 208, 240), "deep": (16, 24, 64),
    "gold0": (144, 144, 168), "gold1": (208, 208, 224), "gold2": (248, 248, 248),
}

m_thread = Mat(["thr1", "thr2", "thr3", "thr4"], line="thr0", cuts=[0.2, 0.46, 0.74])
m_tail = Mat(["thr1", "thr2", "thr3"], line="thr0", cuts=[0.4, 0.7])
m_gold = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.4, 0.75])

THREAD = ["thr0", "thr1", "thr2", "thr3", "thr4"]


def _norm(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


LIGHT3 = _norm((-0.5, -0.65, 0.6))
# the wound bands: (axis, half-width, strand spacing), bottom layer first
BANDS = [(_norm((0.2, 1.0, 0.25)), 0.44, 0.24),
         (_norm((1.0, 0.1, 0.35)), 0.40, 0.24),
         (_norm((0.65, -0.65, 0.45)), 0.36, 0.24)]
BASE = (_norm((0.45, 0.75, -0.3)), 0.24)


def _wind(cx, cy, r, X, Y, rot=0.0):
    """Which band covers design point (X, Y) of the ball and where it is
    across that band's strands. rot spins the ball about its vertical axis."""
    x, y = (X - cx) / r, (Y - cy) / r
    d2 = x * x + y * y
    if d2 > 1:
        return None
    z = math.sqrt(1 - d2)
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        x, z = x * c + z * s, -x * s + z * c
    P = np.array([x, y, z])
    top = -1
    for i, (A, w, s) in enumerate(BANDS):
        if abs(P @ A) < w:
            top = i
    A, s = (BASE if top < 0 else (BANDS[top][0], BANDS[top][2]))
    return np.array([(X - cx) / r, (Y - cy) / r, math.sqrt(1 - d2)]), top, (P @ A) / s


def _ball(p, cx, cy, r, gap=None, rot=0.0, group=1):
    """The clew: a ball wound in crossing bands of thread, each strand a
    1 px line, lit from the upper left. gap = (gx, gy, grx, gry) parts the
    windings where the eyes look out."""
    pid = p.circle(cx, cy, r, m_thread, group=group)
    if not p.big:
        # icon and follower: shading from the parts renderer, a few strands
        p.stroke(bez((cx - r * 0.8, cy - r * 0.2), (cx, cy + r * 0.5), (cx + r * 0.8, cy - r * 0.3)), "thr1")
        p.stroke(bez((cx + r * 0.3, cy - r * 0.9), (cx + r * 0.1, cy + r * 0.1), (cx - r * 0.5, cy + r * 0.8)), "thr1")
        return pid
    # paint the windings pixel by pixel inside the outline
    inside = p.mask([(cx + r * math.cos(t), cy + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 64)])
    H, W = inside.shape

    def ingap(X, Y):
        if not gap:
            return False
        gx, gy, grx, gry = gap
        return ((X - gx) / grx) ** 2 + ((Y - gy) / gry) ** 2 <= 1

    for J in range(H):
        for I in range(W):
            if not inside[J, I]:
                continue
            if any(not (0 <= I + dx < W and 0 <= J + dy < H) or not inside[J + dy, I + dx]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue                          # keep the ink outline
            X, Y = (I + 0.5 - p.ox) / p.s, (J + 0.5 - p.oy) / p.s
            c = _wind(cx, cy, r, X, Y, rot)
            if c is None:
                continue
            P, top, t = c
            if ingap(X, Y):
                p.fig.px(I, J, "deep")
                continue
            v = 0.3 + 0.7 * max(0.0, float(P @ LIGHT3))
            if top < 0:
                v -= 0.12
            if P[1] > 0.78 and P[0] > -0.6:
                v += 0.14                         # light bouncing up off the ground
            k = int(min(4, max(0, v * 4.99)))
            line = edge = False
            for dx, dy in ((1, 0), (0, 1)):
                n = _wind(cx, cy, r, X + dx / p.s, Y + dy / p.s, rot)
                if n is None:
                    continue
                if n[1] != top:
                    edge = True
                elif math.floor(n[2]) != math.floor(t):
                    line = True
            near_gap = any(ingap(X + dx / p.s, Y + dy / p.s) for dx, dy in ((0, 1), (1, 0), (-1, 0)))
            if near_gap:
                k = min(4, k + 1)                 # strands curling over the lip of the gap catch the light
            elif edge:
                k = 0
            elif line:
                k = max(0, k - 2)
            p.fig.px(I, J, THREAD[k])
    return pid


def _star(p, x, y, size):
    """A four-point star of the crown: 2 (Alphecca, the brightest), 1, or 0
    (a glint at the back of the ring)."""
    if size == 2:
        p.patch(x - 3, y - 3, ["...1...", "..1e1..", "..1e1..", "11ded11", "..1e1..", "..1e1..", "...1..."],
                {"1": "ink", "e": "gold2", "d": "gold1"}, small=(x, y, ["e"]))
    elif size == 1:
        p.patch(x - 2, y - 2, ["..1..", ".1d1.", "1ded1", ".1d1.", "..1.."], {"1": "ink", "d": "gold1", "e": "gold2"},
                small=(x, y, ["d"]))
    else:
        p.px(x, y, "gold1")


def _crown(p, cx, cy, rx, ry, spin=0.0):
    """Corona Borealis floating over the clew: a faint gold circlet and its
    seven stars in a horseshoe, the brightest (Alphecca) at the front."""
    pts = []
    for d in (0, 45, -45, 95, -95, 145, -145):                # a horseshoe, open at the back
        a = math.radians(90 + d + spin)                      # front of the ring is +y
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a), math.sin(a)))
    if p.big:
        # a faint thread of light joining the stars across the front
        for i in range(64):
            a = 2 * math.pi * i / 64
            if math.sin(a) > 0.55:
                x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
                p.px(x - 0.5, y - 0.5, "gold0")
    for x, y, depth in sorted(pts, key=lambda t: t[2]):
        size = 2 if depth > 0.97 else (1 if depth > -0.4 else 0)
        _star(p, round(x - 0.5), round(y - 0.5), size)


def mitoclew(p, view, phase):
    if view == "icon":
        # party icon: the clew, its slit of gold eyes and a bold crown
        b = phase
        p.limb(bez3((47, 50), (56, 48), (58, 56), (62, 60)), 4.4, 3.4, m_tail, group=5)
        p.circle(32, 44 - b, 17, m_thread, group=1)
        p.stroke(bez((17, 42 - b), (32, 54 - b), (47, 38 - b)), "thr1")
        p.stroke(bez((38, 28 - b), (36, 46 - b), (24, 59 - b)), "thr1")
        p.blob(26, 40 - b, 9, 3.6, Mat(["deep"]), group=6)
        p.px(21.5, 40 - b, "gold2")
        p.px(28.5, 40 - b, "gold2")
        for x, y in ((18, 20), (32, 23), (46, 20)):
            p.poly([(x, y - 5 - b), (x + 1.6, y - 1.6 - b), (x + 5, y - b), (x + 1.6, y + 1.6 - b), (x, y + 5 - b),
                    (x - 1.6, y + 1.6 - b), (x - 5, y - b), (x - 1.6, y - 1.6 - b)], m_gold, group=9 + x)
        return
    if view in ("front", "side"):
        b = 1 if phase == 1 else 0
        lift = b if view == "front" else 0
        # the loose end, trailing behind like a tail and fraying on the ground
        tail = bez3((41, 50), (49, 48 - lift), (53, 55), (56, 59.5)) if not b else \
            bez3((41, 50), (50, 47), (55, 52), (58, 57))
        p.limb(tail, 3.4, 2.4, m_tail, group=5)
        if p.big:
            for i in range(2, len(tail) - 2, 3):
                p.px(tail[i][0] - 0.5, tail[i][1] - 0.5, "thr0")
        # the clew itself, eyes peeking through a parting in the windings
        _ball(p, 30, 47 - lift, 13, gap=(24.8, 45.6 - lift, 7.2, 3.3), rot=0.18 * b)
        if p.big:
            L = lift
            blink = view == "front" and b
            if blink:
                # frame 2: a happy squint, the eyes curving up
                p.patch(19, 44 - L, [".ee....ee.", "e..d..e..d"], {"e": "gold2", "d": "gold1"})
            else:
                p.patch(19, 43 - L, [".ee...eee.", "ea1e.ea11e", "e11d.e111d", ".dd...ddd."],
                        {"a": "white", "e": "gold2", "d": "gold1", "1": "ink"})
        else:
            p.px(20, 45 - lift, "gold2")
            p.px(26, 45 - lift, "gold2")
        # Corona Borealis
        _crown(p, 30, 27 - lift, 12, 4, spin=14 * b)
        return

    if view == "back":
        # over the shoulder at about 1.2x: the clew from behind, its loose
        # end trailing toward us, one eye peering round to the right
        p.limb(bez3((26, 52), (18, 56), (14, 60), (10, 66)), 4.2, 3.6, m_tail, group=5)
        _ball(p, 33, 50, 18, gap=(47.5, 46.5, 4.2, 5.2), rot=2.2)
        if p.big:
            p.patch(45, 44, [".ee.", "eea1", "ee11", "ed11", ".dd."], {"a": "white", "e": "gold2", "d": "gold1", "1": "ink"})
        _crown(p, 33, 23, 15, 4.8, spin=8)
        return

    if view in ("down", "up"):
        # follower: rolling along, the thread unspooling behind it
        b = phase
        if view == "up":
            p.limb(bez3((36, 56), (42, 60), (44 + b, 58), (50, 61)), 3.2, 2.4, m_tail)
        _ball(p, 32, 46 - b, 13, gap=(32, 44.5 - b, 8, 3.4) if view == "down" else None, rot=0.5 * b)
        if view == "down" and p.big:
            p.patch(25, 43 - b, [".ee....ee.", "ea1e..e1ae", "e11d..d11e", ".dd....dd."],
                    {"a": "white", "e": "gold2", "d": "gold1", "1": "ink"})
        elif view == "down":
            p.px(29, 45 - b, "gold2")
            p.px(35, 45 - b, "gold2")
        _crown(p, 32, 27 - b, 12, 4, spin=14 * b)
        return


MONS = [
    Mon("Mitoclew", MITOCLEW_COLORS, MITOCLEW_SHINY, mitoclew, foot="blank"),
]
