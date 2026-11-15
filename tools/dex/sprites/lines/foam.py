"""Foam line: Aphrell, Aphrogene (Kythera Isle). Aphrodite, born of the sea
foam, rode ashore on a scallop shell (Hesiod, Theogony 188-200)."""
import math

from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts

INK = C.ink


def _fan(hx, hy, R, a0, a1, ribs, bump=0.7, sy=1.0, xr=1.0, n=6):
    """A scallop valve: the hinge at (hx, hy) and a fluted rim from angle a0
    to a1 (degrees, screen space: 0 is right, 90 is down). Each rib ends in a
    small round lobe on the rim. sy squashes the fan toward its hinge line
    and xr its right half (the far side, in three-quarter view). Returns the
    polygon and the rib angles."""
    pts = [(hx, hy)]
    rib_angles = []
    for i in range(ribs):
        t0, t1 = i / ribs, (i + 1) / ribs
        rib_angles.append(a0 + (a1 - a0) * (t0 + t1) / 2)
        for k in range(n + 1):
            t = t0 + (t1 - t0) * k / n
            th = math.radians(a0 + (a1 - a0) * t)
            r = R + bump * math.sin(math.pi * k / n)
            x = r * math.cos(th)
            pts.append((hx + x * (xr if x > 0 else 1.0), hy + r * math.sin(th) * sy))
    return pts, rib_angles


def _fanpt(hx, hy, r, ang, sy=1.0, xr=1.0):
    th = math.radians(ang)
    x = r * math.cos(th)
    return (hx + x * (xr if x > 0 else 1.0), hy + r * math.sin(th) * sy)


# --------------------------------------------------------------------------
# Aphrell, the foam scallop
# --------------------------------------------------------------------------

APHRELL_COLORS = [
    ("ink", INK),
    # marble and pale terracotta shell
    ("sh0", (184, 112, 88)), ("sh1", (224, 160, 128)), ("sh2", (240, 208, 184)), ("sh3", (248, 240, 232)),
    # Aegean blue: the shadows between the ribs, and the sea under the foam
    ("ae0", (24, 56, 120)), ("ae1", (48, 104, 176)), ("ae2", (112, 168, 224)), ("ae3", (176, 216, 240)),
    ("white", C.white),
    # the rose-pink lip, and the soft body inside the shell
    ("rose0", (176, 72, 104)), ("rose1", (224, 128, 152)), ("rose2", (248, 192, 200)),
    ("plum", (88, 40, 72)),
]
APHRELL_SHINY = {
    # sun-gold shell with pearl-white ribs
    "sh0": (184, 112, 32), "sh1": (224, 160, 48), "sh2": (248, 208, 96), "sh3": (248, 248, 232),
}

a_shell = Mat(["sh0", "sh1", "sh2", "sh3"], line="sh0", cuts=[0.2, 0.46, 0.72])
a_low = Mat(["sh0", "sh1", "sh2"], line="sh0", cuts=[0.4, 0.7])
a_foam = Mat(["ae2", "ae3", "white"], line="ae2", cuts=[0.36, 0.62])
a_sea = Mat(["ae0", "ae1", "ae2"], line="ae0", cuts=[0.3, 0.62])
a_lip = Mat(["rose0", "rose1", "rose2"], line="rose0", cuts=[0.4, 0.7])
a_dark = Mat(["plum"], line="plum")


def _foam_curl(p, x, y, w, L=0, flip=False):
    """A curl of sea foam: a breaking wave under the shell, crest curling
    over at the front (x, y is the middle of its base)."""
    s = -1 if flip else 1
    # the wave body, blue under its white crest
    p.blob(x + 2 * s, y + 1.5, w * 0.5, 3.2, a_sea, group=60)
    # rolling foam along the top
    p.blob(x + 3 * s, y - 0.5, w * 0.46, 2.6, a_foam, group=61)
    # the crest curling forward and over
    cx = x - w * 0.42 * s
    p.limb(bez((cx + 4 * s, y + 2), (cx - 1 * s, y - 4 - L), (cx - 5 * s, y - 1 - L)), 4.4, 2.6, a_foam, group=62)
    p.circle(cx - 5 * s, y - 0.2 - L, 1.7, a_foam, group=62)


def _dome(cx, cy, rx, ry, hx, hy, ribs, a0=8, a1=172, lobe=0.8, ear=None):
    """A domed valve in perspective: the front rim is the near half of an
    ellipse (cx, cy, rx, ry), fluted into one lobe per rib, and the back
    climbs to the hinge at (hx, hy). Returns (polygon, rim points at the rib
    ends, rim points between the ribs)."""
    rim, ends, grooves = [], [], []
    n = 6
    for i in range(ribs):
        for k in range(n + 1):
            t = (i + k / n) / ribs
            th = math.radians(a0 + (a1 - a0) * t)
            bump = lobe * math.sin(math.pi * k / n)
            rim.append((cx + (rx + bump) * math.cos(th), cy + (ry + bump) * math.sin(th)))
        th = math.radians(a0 + (a1 - a0) * (i + 0.5) / ribs)
        ends.append((cx + (rx + lobe) * math.cos(th), cy + (ry + lobe) * math.sin(th)))
        if i:
            th = math.radians(a0 + (a1 - a0) * i / ribs)
            grooves.append((cx + rx * math.cos(th), cy + ry * math.sin(th)))
    # rim runs right to left along the front; close over the back through
    # the shoulders of the dome to the hinge
    lx, ly = rim[-1]
    rx_, ry_ = rim[0]
    back = bez3((lx, ly), (lx - 1.5, ly - 6), (hx - rx * 0.7, hy + 1), (hx, hy), n=10)[1:]
    back += bez3((hx, hy), (hx + rx * 0.5, hy + 1), (rx_ + 1.5, ry_ - 6), (rx_, ry_), n=10)[1:-1]
    return rim + back, ends, grooves


def _rib_lines(p, hinge, pts, bulge, color, start=0.22, cx=None):
    """Grooves from near the hinge out to the rim, bowed outward with the dome."""
    hx, hy = hinge
    for x, y in pts:
        a = (hx + (x - hx) * start, hy + (y - hy) * start)
        mx, my = (hx + x) / 2, (hy + y) / 2
        ox = (mx - (cx if cx is not None else hx)) * bulge
        p.stroke(bez(a, (mx + ox, my - abs(ox) * 0.3), (x, y), n=8), color)


def _aph_shell(p, L=0, hop=0, face=True, closed=False, sym=False):
    """The scallop open wide toward us: a ribbed lid cocked up over the soft
    rose body and its big eyes, wing ears at the hinge, a ribbed bowl below,
    riding a cushion of foam. sym draws it square-on (the follower)."""
    y0 = -hop
    p.blob(32, 58.2, 16.5, 1.9, a_sea, group=60)
    for cx, cy, rx, ry in ((18, 55.4, 3.4, 2.4), (24, 56.0, 3.8, 2.2), (31, 56.2, 4.4, 2.0), (38.5, 56.0, 4.0, 2.1),
                           (45, 55.2, 3.4, 2.3)):
        p.blob(cx, cy, rx, ry, a_foam, group=61)
    hx, a0, a1 = (32, 30, 150) if sym else (36, 42, 178)
    # wing ears at the hinge
    p.poly([(hx, 27.5 - L + y0), (hx - 5, 22 - L + y0), (hx - 10.5, 20 - L + y0), (hx - 9.5, 24 - L + y0),
            (hx - 5, 28 - L + y0)], a_shell, group=5)
    p.poly([(hx, 27.5 - L + y0), (hx + 4.5, 22.5 - L + y0), (hx + 9.5, 22 - L + y0), (hx + 8.5, 25.5 - L + y0),
            (hx + 4.5, 28.5 - L + y0)], a_shell, group=6, bias=0.1)
    # the dark inside and the soft rose body in the mouth
    p.blob(31 if not sym else 32, 43 - L * 0.5 + y0, 13, 7.6, a_dark, ang=0 if sym else -14, group=4)
    p.blob(30.5 if not sym else 32, 44 - L * 0.5 + y0, 10.2, 6.8, a_lip, group=3)
    # the ribbed bowl below, its lip rose-pink
    low, langs = _fan(30 if not sym else 32, 61 + y0, 15.5, 192 if not sym else 200, 332 if not sym else 340, 5, 1.0, 0.68)
    p.poly(low, a_low, group=2, bias=0.1)
    # the lid, cocked up over its face
    top, angs = _fan(hx, 27 - L + y0, 17.5, a0, a1, 5, 1.5, 0.74)
    p.poly(top, a_shell, group=1)
    if p.big:
        for i in range(len(angs) - 1):
            a = (angs[i] + angs[i + 1]) / 2
            p.stroke([_fanpt(hx, 27 - L + y0, 4, a, 0.74), _fanpt(hx, 27 - L + y0, 17, a, 0.74)], "ae1")
    if face:
        ex = 23 if not sym else 25
        if p.big:
            p.eye(ex, 39 + y0, 5, 7, shine="white")
            p.eye(ex + 10 if not sym else 35, 40 + y0, 4, 6, shine="white")
        else:
            p.px(ex + 2, 42 + y0, "ink")
            p.px(ex + 11, 42 + y0, "ink")


def aphrell(p, view, phase):
    if view in ("front", "side", "icon"):
        hop = 2 if (view == "side" and phase == 1) else 0
        L = 1 if (phase == 1 and view == "front") else 0
        _aph_shell(p, L, hop, closed=L == 1)
        return

    if view == "back":
        # over the shoulder: the hinge and its ears toward us, the ribs fanning
        # away to the rim, the crack curling round the right side where one
        # eye peeks out
        hx, hy = 28, 58
        p.blob(31, 65, 26, 5, a_sea, group=60)
        for cx, r in ((10, 5), (18, 6), (40, 6), (49, 5)):
            p.blob(cx, 61, r, 3.2, a_foam, group=61)
        p.poly(_fan(hx + 1.6, hy - 1.4, 25, 196, 344, 8, 1.0, 0.92)[0], a_low, group=2, bias=0.2)
        p.poly(_fan(hx + 1.0, hy - 0.8, 24.6, 200, 343, 8, 0.8, 0.92)[0], a_dark, group=3)
        top, angs = _fan(hx, hy, 24, 196, 340, 8, 1.2, 0.9)
        p.poly(top, a_shell, group=1)
        p.poly([(hx - 10, hy + 1.5), (hx + 10, hy + 1.5), (hx + 9, hy - 3.6), (hx - 9.6, hy - 3.6)], a_shell,
               group=5, bias=-0.05)
        if p.big:
            for i in range(len(angs) - 1):
                a = (angs[i] + angs[i + 1]) / 2
                p.stroke([_fanpt(hx, hy, 7, a, 0.9), _fanpt(hx, hy, 23.4, a, 0.9)], "ae1")
            p.eye(48, 38, 3, 5, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # the follower claps its shell to hop along
        clap = phase
        if view == "down":
            _aph_shell(p, L=clap, sym=True)
        else:
            p.blob(32, 58.2, 14, 1.9, a_sea, group=60)
            for cx in (22, 28, 34, 40):
                p.blob(cx, 55.6, 3.6, 2.2, a_foam, group=61)
            top, angs = _fan(32, 52 - clap, 19, 200, 340, 6, 1.2, 0.95)
            p.poly(top, a_shell, group=1)
            p.poly([(32, 52.5 - clap), (25, 50 - clap), (19, 51.5 - clap), (24, 55 - clap)], a_shell, group=5)
            p.poly([(32, 52.5 - clap), (39, 50 - clap), (45, 51.5 - clap), (40, 55 - clap)], a_shell, group=6)
            if p.big:
                for i in range(len(angs) - 1):
                    a = (angs[i] + angs[i + 1]) / 2
                    p.stroke([_fanpt(32, 52 - clap, 5, a, 0.95), _fanpt(32, 52 - clap, 18.4, a, 0.95)], "ae1")
        return


# --------------------------------------------------------------------------
# Aphrogene, the foam-born
# --------------------------------------------------------------------------

APHROGENE_COLORS = [
    ("ink", INK),
    # the Aegean-blue body, the sea she is made of
    ("bd0", (24, 48, 112)), ("bd1", (48, 96, 176)), ("bd2", (96, 152, 216)), ("bd3", (160, 208, 240)),
    # marble-white foam, shadowed sea-gray
    ("fm0", (120, 160, 192)), ("fm1", (200, 224, 232)), ("fm2", (248, 248, 240)),
    # marble and pale terracotta shell
    ("sh0", (168, 96, 72)), ("sh1", (216, 152, 120)), ("sh2", (240, 200, 168)), ("sh3", (248, 240, 224)),
    # rose: her cheeks and the shell's lip
    ("rose0", (184, 80, 112)), ("rose1", (232, 136, 160)), ("rose2", (248, 200, 208)),
]
APHROGENE_SHINY = {
    # a sun-gold shell, and foam turned soft rose pink
    "sh0": (176, 104, 32), "sh1": (224, 160, 48), "sh2": (248, 208, 96), "sh3": (248, 240, 176),
    "fm0": (192, 120, 152), "fm1": (240, 184, 200), "fm2": (248, 232, 232),
}

g_body = Mat(["bd0", "bd1", "bd2", "bd3"], line="bd0", cuts=[0.16, 0.42, 0.72])
g_face = Mat(["bd1", "bd2", "bd3"], line="bd1", cuts=[0.5, 0.78])
g_foam = Mat(["fm0", "fm1", "fm2"], line="fm0", cuts=[0.5, 0.74])
g_sea = Mat(["bd0", "bd1", "bd2", "fm1"], line="bd0", cuts=[0.2, 0.46, 0.72])
g_shell = Mat(["sh0", "sh1", "sh2", "sh3"], line="sh0", cuts=[0.2, 0.46, 0.72])
g_in = Mat(["sh1", "sh2", "sh3"], line="sh0", cuts=[0.36, 0.68])
g_lip = Mat(["rose0", "rose1", "rose2"], line="rose0", cuts=[0.4, 0.7])


def _lock(p, path, w0, w1, **kw):
    """A lock of foam hair: a tapering ribbon of foam."""
    return p.limb(path, w0, w1, g_foam, **kw)


def aphrogene(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        # the upper valve, opened wide behind her like a fan
        hx, hy = 39, 48
        fan, angs = _fan(hx, hy, 28.5, 190, 350, 9, 1.5, 1.18, 0.76)
        p.poly(fan, g_shell, group=1, bias=-0.08)
        if p.big:
            for i in range(len(angs) - 1):
                a = (angs[i] + angs[i + 1]) / 2
                p.stroke([_fanpt(hx, hy, 7, a, 1.18, 0.76), _fanpt(hx, hy, 28, a, 1.18, 0.76)], "bd1")
        # the long foam hair falling down her back, curling out over the fan
        _lock(p, bez3((33, 7 - L), (43, 8), (45, 18), (48, 26 + L)), 7.0, 3.2, group=40)
        p.circle(48.6, 27.2 + L, 2.4, g_foam, group=40)
        _lock(p, bez3((34, 12 - L), (41, 17), (40, 27), (44, 35 + L)), 6.4, 2.8, group=41)
        p.circle(44.8, 36 + L, 2.3, g_foam, group=41)
        _lock(p, bez3((34, 17 - L), (38, 23), (36.5, 31), (39.5, 39)), 4.8, 2.4, group=39, bias=0.15)
        p.circle(40, 39.6, 1.8, g_foam, group=39, bias=0.15)
        # the far arm, down at her side
        p.limb([(34.5, 25), (37.5, 30.5), (37, 35)], 3.0, 2.4, g_body, bias=0.25, group=20)
        # the lower valve: a dish she stands in, its lip rose-pink
        dish = [(8, 51), (14, 56), (26, 59.5), (38, 60), (50, 58), (59, 53), (58.5, 49.5), (48, 47.6), (34, 47),
                (20, 47.8), (9, 49.4)]
        p.poly(dish, g_shell, group=2)
        p.poly(ellipse_pts(33.5, 50, 24, 3.6, ang=-1.5), g_in, group=3)
        p.poly([(9, 50.4), (20, 52.8), (34, 53.8), (48, 52.8), (58.6, 50.2), (58.6, 51.6), (48, 54.2), (34, 55.2),
                (20, 54.2), (9, 52)], g_lip, group=4)
        # surf: her lower body dissolving into foam that fills the shell and
        # spills over its front rim
        p.poly([(27.5, 35), (33.5, 35), (36, 40), (42, 45.5), (51, 48.5), (44, 51.5), (30, 52.5), (16, 51.5),
                (11, 49), (18, 45.5), (25, 40)], g_sea, group=10)
        for cx, cy, rx, ry in ((14.5, 49.6, 4.6, 2.4), (23, 50.8, 5.2, 2.4), (32, 51, 5, 2.2), (40.5, 50, 5, 2.2),
                               (48, 48.8, 3.6, 2.0), (30.5, 43.8, 4.0, 2.4), (24.5, 46.6, 3.6, 2.0), (36.5, 46.2, 3.4, 2.0)):
            p.blob(cx, cy, rx, ry, g_foam, group=11)
        p.limb(bez3((11, 49.5), (6.5, 51), (6, 55), (7.5, 60)), 4.6, 2.8, g_foam, group=12)
        p.limb(bez((12.5, 52.5), (12, 57), (13.5, 60.5)), 3.2, 2.0, g_foam, group=12)
        # torso: slender, the Aegean body
        p.limb([(30, 24), (30.3, 29.5), (30.8, 35.5)], 7.6, 5.4, g_body, group=21)
        p.blob(29.4, 26.5, 4.2, 3.2, g_body, group=21)
        # neck and head
        p.limb([(28.5, 18 - L), (29.5, 24)], 3.4, 4.0, g_body, group=21)
        p.blob(25.4, 13.6 - L, 5.8, 6.2, g_face, group=30, bias=-0.15)
        # a frothy ruff of foam around the shoulders
        for cx, cy, r in ((25, 23.8, 2.0), (28, 24.8, 2.3), (31.4, 25, 2.3), (34.4, 24, 2.0)):
            p.circle(cx, cy, r, g_foam, group=35)
        # foam hair: a cap over the crown, swept back, bangs over the brow and
        # a lock framing the cheek
        p.blob(29.5, 8.6 - L, 6.4, 5.0, g_foam, group=42)
        p.lens((31.5, 4.5 - L), (19.6, 10 - L), 4.8, g_foam, bend=1.4, group=43)
        p.lens((32.5, 8 - L), (31.5, 19.5 - L), 4.6, g_foam, bend=-1.0, group=44)
        # the near arm, raised, wringing out a lock of hair at her temple:
        # elbow thrown out to the left
        p.limb([(25, 23.5), (18, 21.5), (12.5, 17)], 3.4, 2.8, g_body, group=22)
        p.limb([(12.5, 17), (14, 12), (17, 8.5 - L)], 2.8, 2.4, g_body, group=22)
        _lock(p, bez3((22, 6.5 - L), (20, 5.5 - L), (17.5, 6 - L), (17, 8 - L)), 3.0, 2.6, group=45)
        p.blob(17, 8.8 - L, 1.9, 1.9, g_body, group=23, bias=-0.1)
        _lock(p, bez((17, 10.6 - L), (17.6, 14), (17, 18 + L)), 2.4, 1.4, group=46)
        p.drop((16.8, 19.6 + L), 17.0, 22.2 + L, 1.2, g_sea, group=47)
        p.drop((16.6, 25.6 + 2 * L), 16.8, 27.6 + 2 * L, 0.9, g_sea, group=48)
        if p.big:
            p.eye(21, 12 - L, 2, 5, shine="fm2", pupil="bd0", shine_at=(1, 1))
            p.eye(24, 12 - L, 3, 5, shine="fm2", pupil="bd0")
            p.pxs([(21, 17 - L), (24, 17 - L), (25, 17 - L)], "rose1")
        else:
            p.px(21.5, 14 - L, "bd0")
            p.px(26, 14 - L, "bd0")
        return

    if view == "back":
        # over the shoulder: the open valve's ribbed back fills the foreground,
        # she rises above its rim, head turned right, foam hair pouring over
        # the shell, one hand raised to gather it at the nape
        hx, hy = 32, 82
        fan, angs = _fan(hx, hy, 40, 222, 318, 9, 1.6, 1.0, 1.0)
        # her back and shoulders, behind the shell's rim
        p.limb([(31, 50), (33, 40), (36, 32)], 17, 13, g_body, group=21)
        p.blob(35.5, 32.5, 10, 5, g_body, group=21)
        # her right arm, down at her side
        p.limb([(45, 33), (49, 40), (49, 46)], 4.8, 4.0, g_body, group=22)
        # a frothy ruff of foam over the shoulders
        for cx, cy, r in ((26, 34, 2.6), (30.5, 32.4, 2.8), (35.5, 31.6, 2.8), (40.5, 32, 2.8), (45, 33.4, 2.6)):
            p.circle(cx, cy, r, g_foam, group=35)
        # neck and head in right profile
        p.limb([(37.5, 29), (39, 23)], 5.4, 5.0, g_body, group=21)
        p.blob(41, 17, 7.4, 7.6, g_face, group=30, bias=-0.15)
        p.blob(48, 19.5, 3.0, 2.6, g_face, group=30, bias=-0.15)
        # foam hair: the crown, and the long fall pouring down her back and
        # over the shell
        p.blob(36.5, 14, 8.0, 7.2, g_foam, group=42)
        _lock(p, bez3((33, 16), (24, 22), (26, 34), (15, 44)), 7.4, 3.6, group=40)
        _lock(p, bez3((35, 20), (29, 28), (31, 38), (24, 47)), 5.6, 3.0, group=41)
        p.circle(15, 44.6, 2.8, g_foam, group=40)
        p.circle(24, 47.6, 2.4, g_foam, group=41)
        p.lens((40, 8), (48.5, 12.5), 4.4, g_foam, bend=-0.8, group=43)
        # the shell's ribbed back, nearest us
        p.poly(fan, g_shell, group=1, bias=0.05)
        if p.big:
            for i in range(len(angs) - 1):
                a = (angs[i] + angs[i + 1]) / 2
                p.stroke([_fanpt(hx, hy, 18, a), _fanpt(hx, hy, 39.4, a)], "bd1")
            p.eye(44, 15, 3, 5, shine="fm2", pupil="bd0", shine_at=(1, 1))
            p.pxs([(45, 21), (46, 21)], "rose1")
        return

    if view in ("down", "up"):
        # the follower drifts on a patch of foam, the open shell behind her
        sw = phase
        fan, angs = _fan(32, 44, 21, 198, 342, 9, 1.2, 1.1)
        if view == "down":
            p.poly(fan, g_shell, group=1, bias=-0.05)
            if p.big:
                for i in range(len(angs) - 1):
                    a = (angs[i] + angs[i + 1]) / 2
                    p.stroke([_fanpt(32, 44, 6, a, 1.1), _fanpt(32, 44, 20.4, a, 1.1)], "bd1")
        # hair falling behind her shoulders
        _lock(p, bez3((27, 14), (20, 22), (22, 34), (19 - sw, 42)), 6, 3, group=40)
        _lock(p, bez3((37, 14), (44, 22), (42, 34), (45 + sw, 42)), 6, 3, group=41)
        # the surf she rises from, on its patch of foam
        p.poly([(27, 38), (37, 38), (41, 46), (46, 53), (18, 53), (23, 46)], g_sea, group=10)
        for cx, cy, rx, ry in ((22, 55, 5, 2.6), (32, 56, 6, 2.8), (42, 55, 5, 2.6), (32, 47, 4.4, 2.2)):
            p.blob(cx, cy + (sw if cx == 32 else 0), rx, ry, g_foam, group=11)
        # body and arms
        p.limb([(32, 26), (32, 32), (32, 39)], 9, 6.4, g_body, group=21)
        p.limb([(27.5, 27), (25, 33), (25.5, 38 - sw)], 3.2, 2.6, g_body, group=22)
        p.limb([(36.5, 27), (39, 33), (38.5, 38 - (1 - sw))], 3.2, 2.6, g_body, group=23)
        for cx in (27, 30.5, 33.5, 37):
            p.circle(cx, 26, 2.0, g_foam, group=35)
        p.limb([(32, 21), (32, 25)], 3.6, 4, g_body, group=21)
        p.blob(32, 17, 6.4, 6.8, g_face, group=30, bias=-0.15)
        p.blob(32, 12.5, 7.4, 4.8, g_foam, group=42)
        if view == "down":
            p.lens((33, 9), (25.6, 15), 4.4, g_foam, bend=1.0, group=43)
            p.lens((31, 9), (38.4, 15), 4.4, g_foam, bend=-1.0, group=44)
            p.eye(27.5, 16, 3, 4, shine="fm2", pupil="bd0")
            p.eye(33.5, 16, 3, 4, shine="fm2", pupil="bd0")
            if p.big:
                p.pxs([(27, 21), (36, 21)], "rose1")
        else:
            _lock(p, bez3((32, 12), (29, 22), (34, 32), (31, 44)), 9, 4, group=45)
            p.poly(fan, g_shell, group=1, bias=0.1)
            if p.big:
                for i in range(len(angs) - 1):
                    a = (angs[i] + angs[i + 1]) / 2
                    p.stroke([_fanpt(32, 44, 6, a, 1.1), _fanpt(32, 44, 20.4, a, 1.1)], "bd1")
        return


MONS = [
    Mon("Aphrell", APHRELL_COLORS, APHRELL_SHINY, aphrell, foot="blank", icon_pal=0),
    Mon("Aphrogene", APHROGENE_COLORS, APHROGENE_SHINY, aphrogene, foot="blank"),
]
