#!/usr/bin/env python3
"""The statues of the Twelve before the Propylaia (design/maps/Ascent_3F.md), drawn to the
user's reference (design/art/refs/statue_zeus_reference.png): a painted marble god on a
teal hexagonal plinth, bearded or not, the chiton's folds falling from one shoulder,
the god's own attribute in the hand, crisp dark outlines, soft shading lit from the
upper left, and a cast shadow on the snow.

Each statue is a 32 x 64 inanimate object (one frame), under its own palette tag
(OBJ_EVENT_PAL_TAG_ICHOR_STATUE), so they read at 1x and cost no tiles from the
Propylaia's tileset.

Usage: /usr/bin/python3 tools/ichor/art/statues.py [--write] [--preview out.png]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/object_events/pics/misc/ichor"
PAL_OUT = ROOT / "graphics/object_events/palettes/ichor_statue.pal"

PAL = [
    (0, 0, 0),          # 0 transparent
    (24, 24, 40),       # 1 k   the outline
    (96, 96, 128),      # 2 m0  marble in deep shade
    (144, 144, 168),    # 3 m1  shade
    (192, 192, 208),    # 4 m2  mid
    (232, 232, 240),    # 5 m3  lit
    (248, 248, 248),    # 6 m4  the highlight
    (184, 128, 40),     # 7 g1  gilding in shade
    (248, 208, 96),     # 8 g2  gilding lit
    (24, 88, 88),       # 9 t0  the plinth's teal stone, shade
    (56, 136, 128),     # 10 t1 mid
    (120, 192, 176),    # 11 t2 lit
    (176, 48, 40),      # 12 r  painted red
    (40, 72, 160),      # 13 b  painted blue
    (136, 152, 192),    # 14 sh the shadow on the snow
    (160, 96, 48),      # 15 br bronze, wood and fire's heart
]
K, M0, M1, M2, M3, M4, G1, G2, T0, T1, T2, R, B, SH, BR = range(1, 16)
W, H = 32, 64


class Cv:
    def __init__(self):
        self.a = np.zeros((H, W), np.int32)

    def px(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < W and 0 <= y < H:
            self.a[y, x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c, w=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(int(n) + 1):
            x = x0 + (x1 - x0) * i / n
            y = y0 + (y1 - y0) * i / n
            for k in range(w):
                self.px(round(x) + k, round(y), c)

    def ellipse(self, cx, cy, rx, ry, fn):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 1:
                    self.px(x, y, fn(x + 0.5 - cx, y + 0.5 - cy, d))

    def outline(self, c=K):
        m = self.a > 0
        e = np.zeros_like(m)
        e[1:] |= m[:-1]
        e[:-1] |= m[1:]
        e[:, 1:] |= m[:, :-1]
        e[:, :-1] |= m[:, 1:]
        e &= ~m
        self.a[e] = c


def marble(u):
    """Shade across a rounded form, u 0 (left, lit) .. 1 (right)."""
    return M4 if u < 0.12 else M3 if u < 0.38 else M2 if u < 0.66 else M1 if u < 0.88 else M0


def figure(cv, god):
    """The god: a robed figure standing on the plinth's top (y 50), head at y 7-14."""
    male = god in ("hermes", "dionysus", "hephaestus", "apollo", "ares", "poseidon", "zeus")
    bearded = god in ("hephaestus", "poseidon", "zeus", "dionysus")
    cx = 15.5
    # the long chiton: wider at the hem, a himation draped from the left shoulder
    for y in range(20, 50):
        t = (y - 20) / 30
        hw = 4.6 + 3.4 * t * t + (0.8 if y < 24 else 0)
        for x in range(int(cx - hw), int(cx + hw) + 1):
            u = (x + 0.5 - (cx - hw)) / (2 * hw)
            c = marble(u)
            # vertical folds below the waist, light and dark in pairs
            if y > 33 and int((x - cx + 20) * 0.7) % 2 == 0 and 0.15 < u < 0.9:
                c = M1 if u > 0.5 else M2
            cv.px(x, y, c)
    # the himation's diagonal sweep from the left shoulder to the right hip, its folds
    for i in range(14):
        y = 21 + i
        x0 = int(cx - 6 + i * 0.75)
        for k in range(4):
            cv.px(x0 + k, y, M3 if k == 0 else M2 if k < 3 else M1)
        cv.px(x0 + 4, y, M0)
    for y in range(35, 49, 3):
        cv.line(cx + 2, y, cx + 5, y + 2, M1)
    # feet under the hem
    cv.rect(cx - 4, 49, cx - 2, 49, M2)
    cv.rect(cx + 1, 49, cx + 3, 49, M1)
    # torso and shoulders: bare chest on the male gods
    for y in range(15, 21):
        hw = 6.6 if y > 16 else 5.4
        for x in range(int(cx - hw), int(cx + hw) + 1):
            u = (x + 0.5 - (cx - hw)) / (2 * hw)
            cv.px(x, y, marble(u))
    if male:
        cv.px(cx - 2, 18, M1)
        cv.px(cx + 1, 18, M1)
    # the head: hair, face, beard
    # the neck, the head
    cv.rect(cx - 1, 13, cx + 1, 15, M2)
    cv.ellipse(cx, 10, 3.2, 3.8, lambda dx, dy, d: marble((dx + 3.2) / 6.4))
    hair = M1 if god not in ("aphrodite", "artemis") else M0
    for x in range(int(cx - 4), int(cx + 4) + 1):
        cv.px(x, 6, hair)
        cv.px(x, 7, hair if abs(x + 0.5 - cx) > 1.5 or god in ("hestia", "hera", "demeter") else M3)
    if not male:
        for y in range(8, 16):
            cv.px(cx - 4, y, hair)
            cv.px(cx + 4, y, M0)
    cv.px(cx - 1.5, 10, M0)
    cv.px(cx + 1.5, 10, M0)
    cv.px(cx - 1.5, 9, M1)
    cv.px(cx + 1.5, 9, M1)
    cv.px(cx + 0.5, 11, M1)
    cv.px(cx, 12.5, M1)
    if bearded:
        cv.ellipse(cx, 14, 3.2, 2.6, lambda dx, dy, d: M2 if dx < 0 else M1)
        cv.px(cx, 13, M3)
    return cx


def arm(cv, x0, y0, x1, y1):
    """An arm from the shoulder to the hand: lit on top, a shadowed underside."""
    cv.line(x0, y0, x1, y1, M3, 2)
    cv.line(x0, y0 + 1, x1, y1 + 1, M1, 2)
    cv.ellipse(x1 + 0.5, y1 + 0.5, 1.4, 1.4, lambda dx, dy, d: M3 if dx < 0 else M2)


def attributes(cv, god, cx):
    """The hands and what they hold: the god at a glance."""
    L, Rx = cx - 7, cx + 7
    if god == "zeus":
        arm(cv, cx - 5, 17, L - 3, 12)
        cv.line(L - 2, 4, L - 5, 10, G2, 2)
        cv.line(L - 5, 10, L - 1, 11, G2, 2)
        cv.line(L - 1, 11, L - 4, 18, G2, 2)
        arm(cv, cx + 5, 18, Rx + 2, 22)
        cv.ellipse(Rx + 4, 18, 3, 2.4, lambda dx, dy, d: BR if dy > 0 else M0)
        cv.line(Rx + 1, 15, Rx + 7, 14, BR, 2)
        cv.px(Rx + 6, 17, G2)
    elif god == "hestia":
        for y in range(5, 16):
            cv.px(cx - 4, y, M1)
            cv.px(cx + 4, y, M1)
        cv.rect(cx - 4, 5, cx + 4, 6, M2)
        arm(cv, cx - 5, 19, cx - 1, 24)
        arm(cv, cx + 5, 19, cx + 1, 24)
        cv.ellipse(cx, 25, 4, 1.6, lambda dx, dy, d: G1 if dy > 0 else G2)
        for i, (dx, h_) in enumerate(((-2, 3), (0, 5), (2, 3))):
            for y in range(int(23 - h_), 24):
                cv.px(cx + dx, y, R if y > 23 - h_ + 1 else G2)
    elif god == "hermes":
        cv.rect(cx - 5, 5, cx + 5, 6, G1)
        cv.line(cx - 6, 4, cx - 9, 2, M4, 2)
        cv.line(cx + 6, 4, cx + 9, 2, M4, 2)
        arm(cv, cx + 5, 17, Rx + 1, 24)
        cv.line(Rx + 2, 8, Rx + 2, 40, G1)
        cv.ellipse(Rx + 2, 8, 2, 2, lambda dx, dy, d: G2)
        for y in range(12, 22, 3):
            cv.px(Rx + 1, y, G2)
            cv.px(Rx + 3, y + 1, G2)
        arm(cv, cx - 5, 18, L, 26)
        cv.px(cx - 3, 49, M4)
        cv.px(cx + 2, 49, M4)
    elif god == "demeter":
        cv.rect(cx - 4, 5, cx + 4, 6, G1)
        arm(cv, cx - 5, 18, cx + 1, 25)
        for i in range(-3, 4):
            cv.line(cx - 4 + i, 18, cx - 6 + i * 2, 10, G1)
            cv.px(cx - 6 + i * 2, 10, G2)
            cv.px(cx - 6 + i * 2, 9, G2)
        arm(cv, cx + 5, 18, Rx, 27)
    elif god == "dionysus":
        for x in range(int(cx - 4), int(cx + 5), 2):
            cv.px(x, 6, B)
            cv.px(x + 1, 5, B)
        arm(cv, cx + 5, 17, Rx + 1, 22)
        cv.line(Rx + 2, 6, Rx + 2, 44, BR)
        cv.ellipse(Rx + 2, 5, 2, 2.6, lambda dx, dy, d: G1 if dx > 0 else G2)
        arm(cv, cx - 5, 18, L - 1, 22)
        cv.ellipse(L - 2, 21, 2.6, 1.8, lambda dx, dy, d: G2 if dy < 0 else G1)
        cv.px(L - 2, 20, R)
        cv.px(L - 1, 20, R)
    elif god == "artemis":
        cv.ellipse(cx, 4.5, 3, 1.4, lambda dx, dy, d: G2)
        cv.ellipse(cx, 5.2, 2, 1, lambda dx, dy, d: 0)
        arm(cv, cx - 5, 18, L - 2, 21)
        for y in range(9, 34):
            t = (y - 21.5) / 12.5
            cv.px(L - 3 + int(3 * (1 - t * t)), y, G1)
        cv.line(L - 3, 9, L - 3, 33, M4)
        cv.rect(cx + 4, 15, cx + 6, 27, BR)
        cv.px(cx + 5, 14, G2)
        cv.px(cx + 4, 13, M4)
        arm(cv, cx + 5, 18, Rx, 26)
    elif god == "hephaestus":
        cv.ellipse(cx, 6, 4, 2.4, lambda dx, dy, d: BR if dx > 0 else G1)
        arm(cv, cx + 5, 17, Rx + 2, 10)
        cv.line(Rx + 2, 4, Rx + 2, 12, BR, 2)
        cv.rect(Rx - 1, 2, Rx + 5, 5, M0)
        cv.rect(Rx - 1, 2, Rx + 5, 2, M2)
        arm(cv, cx - 5, 18, L - 1, 28)
        cv.line(L - 2, 24, L - 2, 48, BR)
        cv.rect(L - 4, 24, L, 25, BR)
    elif god == "aphrodite":
        arm(cv, cx - 5, 18, L - 2, 14)
        cv.ellipse(L - 3, 11, 2.6, 2, lambda dx, dy, d: M4 if dy < 0 else M3)
        cv.line(L - 6, 10, L - 3, 12, M4)
        cv.px(L - 1, 10, G2)
        arm(cv, cx + 5, 18, Rx, 27)
        cv.ellipse(cx + 1, 48.5, 4.5, 2.5, lambda dx, dy, d: R if (int(dx + 5) % 2) else M4)
    elif god == "apollo":
        cv.ellipse(cx, 6, 4.2, 1.6, lambda dx, dy, d: G1 if (int(dx + 5) % 2) else G2)
        arm(cv, cx - 5, 18, L, 24)
        cv.line(L - 3, 16, L - 4, 28, G1, 2)
        cv.line(L + 2, 16, L + 3, 28, G1, 2)
        cv.line(L - 4, 28, L + 3, 28, G1, 2)
        cv.line(L - 3, 16, L + 2, 16, G2)
        for x in range(int(L - 2), int(L + 2)):
            cv.line(x, 17, x, 27, M4)
        arm(cv, cx + 5, 18, Rx, 26)
    elif god == "ares":
        cv.ellipse(cx, 7.5, 4.2, 3.6, lambda dx, dy, d: BR if dx > 0 else G1)
        cv.rect(cx - 1, 1, cx + 1, 4, R)
        cv.rect(cx + 2, 2, cx + 4, 3, R)
        cv.rect(cx - 2, 9, cx + 2, 11, M3)
        arm(cv, cx + 5, 17, Rx + 1, 20)
        cv.line(Rx + 2, 0, Rx + 2, 48, BR)
        cv.line(Rx + 1, 1, Rx + 3, 1, G2)
        cv.px(Rx + 2, 0, M4)
        cv.ellipse(L - 1, 30, 5.5, 7, lambda dx, dy, d: G1 if d > 0.7 else R if d > 0.25 else G2)
    elif god == "poseidon":
        arm(cv, cx + 5, 17, Rx + 1, 22)
        cv.line(Rx + 2, 2, Rx + 2, 48, G1)
        for dx in (-2, 0, 2):
            cv.line(Rx + 2 + dx, 1, Rx + 2 + dx, 6, G2)
        cv.line(Rx, 6, Rx + 4, 6, G2)
        arm(cv, cx - 5, 18, L, 27)
        cv.rect(cx - 6, 21, cx + 6, 22, B)
    elif god == "athena":
        cv.ellipse(cx, 7, 4.2, 3.4, lambda dx, dy, d: G1 if dx > 0 else G2)
        cv.rect(cx - 4, 2, cx + 3, 3, R)
        cv.rect(cx - 2, 1, cx + 1, 1, R)
        arm(cv, cx + 5, 17, Rx + 1, 21)
        cv.line(Rx + 2, 0, Rx + 2, 48, BR)
        cv.px(Rx + 2, 0, M4)
        cv.rect(cx - 4, 16, cx + 4, 19, G1)
        cv.px(cx, 17, R)
        cv.ellipse(L - 1, 14, 2.6, 3, lambda dx, dy, d: M1 if dx > 0 else M2)
        cv.px(L - 2, 13, G2)
        cv.px(L, 13, G2)
        arm(cv, cx - 5, 18, L - 1, 20)
    elif god == "hera":
        cv.rect(cx - 4, 3, cx + 4, 6, G1)
        cv.rect(cx - 4, 3, cx + 4, 3, G2)
        arm(cv, cx + 5, 17, Rx + 1, 22)
        cv.line(Rx + 2, 4, Rx + 2, 48, G1)
        cv.ellipse(Rx + 2, 4, 1.8, 1.8, lambda dx, dy, d: B)
        arm(cv, cx - 5, 18, L - 1, 25)
        for i, (fx, fy) in enumerate(((L - 4, 18), (L - 6, 22), (L - 5, 27), (L - 3, 31))):
            cv.ellipse(fx, fy, 1.6, 1.6, lambda dx, dy, d: B if d < 0.4 else T1)


def plinth(cv):
    """The teal hexagonal plinth, its top face lit, with a cast shadow on the snow."""
    for y in range(52, 64):
        for x in range(8, 32):
            d = ((x + 0.5 - 23) / 9.5) ** 2 + ((y - 59.5) / 4.2) ** 2
            if d < 1 and cv.a[y, x] == 0:
                cv.px(x, y, SH)
    for y in range(49, 61):
        rel = y - 49
        if rel < 4:
            hw = 11 + rel
        else:
            hw = 14
        for x in range(int(16 - hw), int(16 + hw)):
            if rel < 4:
                c = T2 if x < 15 else T1
                if rel == 0:
                    c = T2
            elif rel < 10:
                c = T1 if x < 13 else T0
                if (x - 2) % 9 == 0:
                    c = T0
            else:
                c = T0
            cv.px(x, y, c)
    for x in range(5, 27):
        cv.px(x, 53, T0)


def statue(god):
    cv = Cv()
    plinth(cv)
    fig = Cv()
    cx = figure(fig, god)
    attributes(fig, god, cx)
    fig.outline(K)
    m = fig.a > 0
    cv.a[m] = fig.a[m]
    cv.outline(K) if False else None
    return cv.a


# ---------------------------------------------------------------------------
# v2 (2026-11-18, second pass): a pose for every god, a face on every head
# ---------------------------------------------------------------------------
MARBLE = [M0, M1, M2, M3, M4]       # deep shade .. highlight


def ramp_x(u, steps=MARBLE):
    """Marble across a rounded form lit from the upper left, u 0 (left) .. 1 (right)."""
    i = 4 if u < 0.14 else 3 if u < 0.4 else 2 if u < 0.68 else 1 if u < 0.88 else 0
    return steps[i]


def fill_poly(cv, pts, shade=True, color=None, lit=0.0):
    from PIL import Image as _I, ImageDraw as _D
    m = _I.new("1", (W, H), 0)
    _D.Draw(m).polygon(pts, fill=1)
    a = np.array(m)
    ys, xs = np.nonzero(a)
    if not len(xs):
        return a
    for y in set(ys.tolist()):
        row = xs[ys == y]
        x0, x1 = row.min(), row.max()
        for x in row:
            if color is not None:
                c = color
            else:
                u = (x + 0.5 - x0) / max(1, x1 - x0 + 1) - lit
                c = ramp_x(max(0.0, min(1.0, u)))
            cv.px(x, y, c)
    return a


def limb(cv, x0, y0, x1, y1, w=2, tone=None):
    """An arm or a leg: a thick stroke lit on its upper-left edge."""
    n = int(max(abs(x1 - x0), abs(y1 - y0), 1) * 2)
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        for k in range(w):
            c = tone or (M3 if k == 0 else M2 if k < w - 1 else M1)
            cv.px(round(x + k - (w - 1) / 2), round(y), c)


def head(cv, cx, cy, beard=False, hair="short", veil=False, helm=None, cap=None, wreath=None):
    """A head about 7 px wide lit from the upper left: a mass of hair, the face set
    into it, brow, eyes, nose and mouth in a few values, the neck, a beard."""
    # the neck first, so the head sits on it
    cv.rect(cx - 1, cy + 3, cx + 1, cy + 7, M2)
    cv.rect(cx - 1, cy + 3, cx - 1, cy + 7, M3)
    cv.rect(cx + 1, cy + 3, cx + 1, cy + 7, M1)
    # the hair: a rounded mass, lit on its upper left
    cv.ellipse(cx, cy - 1.2, 3.9, 3.5, lambda dx, dy, d: M2 if (dx < -0.5 and dy < 0) else M1 if d < 0.8 else M0)
    if hair == "long":
        for y in range(int(cy), int(cy + 6)):
            cv.px(cx - 4, y, M1)
            cv.px(cx - 3, y, M2)
            cv.px(cx + 3, y, M0)
            cv.px(cx + 4, y, M0)
    # the face, set into the hair
    cv.ellipse(cx, cy + 0.8, 2.8, 3.0, lambda dx, dy, d: M4 if dx < -0.8 else M3 if dx < 0.9 else M2)
    # brow, eyes in soft shadow under it, the nose's lit ridge and its shadow, the mouth
    cv.px(cx - 2, cy - 0.5, M2)
    cv.px(cx - 1, cy - 0.5, M2)
    cv.px(cx + 1, cy - 0.5, M1)
    cv.px(cx + 2, cy - 0.5, M1)
    cv.px(cx - 1.5, cy + 0.5, M0)
    cv.px(cx + 1.5, cy + 0.5, M0)
    cv.px(cx, cy + 0.5, M4)
    cv.px(cx, cy + 1.5, M3)
    cv.px(cx + 1, cy + 1.5, M1)
    cv.px(cx, cy + 3, M1)
    if beard:
        cv.ellipse(cx, cy + 3.8, 3.4, 2.7, lambda dx, dy, d: M3 if dx < -1.2 else M2 if dx < 1.2 else M1)
        for x in (cx - 2, cx, cx + 2):
            cv.px(x, cy + 5, M1 if x <= cx else M0)
        cv.px(cx - 1, cy + 3, M0)
        cv.px(cx, cy + 3, M0)
        cv.px(cx + 1, cy + 3, M0)
    if veil:
        for y in range(int(cy - 4), int(cy + 7)):
            cv.px(cx - 4, y, M3)
            cv.px(cx + 4, y, M1)
        for x in range(int(cx - 3), int(cx + 4)):
            cv.px(x, cy - 4, M3 if x < cx else M2)
            cv.px(x, cy - 5, M2)
    if helm == "corinthian":
        cv.ellipse(cx, cy - 1.5, 3.8, 3.4, lambda dx, dy, d: G2 if dx < -1 else G1)
        cv.rect(cx - 1, cy - 1, cx + 1, cy + 1, M3)
        cv.px(cx - 1.5, cy, K)
        cv.px(cx + 1.5, cy, K)
        for i, x in enumerate(range(int(cx - 4), int(cx + 5))):
            top = cy - 6 - (2 if 1 < i < 7 else 1)
            for y in range(int(top), int(cy - 4)):
                cv.px(x, y, R)
            cv.px(x, top, R if x > cx else G2)
    if helm == "athena":
        cv.ellipse(cx, cy - 2, 3.8, 2.6, lambda dx, dy, d: G2 if dx < -1 else G1)
        for x in range(int(cx - 3), int(cx + 4)):
            cv.px(x, cy - 6, R)
            cv.px(x, cy - 5, R)
        cv.px(cx - 4, cy - 1, G1)
    if cap == "petasos":
        cv.rect(cx - 4, cy - 4, cx + 4, cy - 4, G1)
        cv.rect(cx - 3, cy - 5, cx + 3, cy - 5, G2)
        for i in range(3):
            cv.px(cx - 5 - i, cy - 5 - i, M4)
            cv.px(cx + 5 + i, cy - 5 - i, M4)
            cv.px(cx - 5 - i, cy - 4 - i, M3)
            cv.px(cx + 5 + i, cy - 4 - i, M3)
    if cap == "pilos":
        fill_poly(cv, [(cx - 4, cy - 3), (cx, cy - 8), (cx, cy - 3)], color=G1)
        fill_poly(cv, [(cx, cy - 8), (cx + 4, cy - 3), (cx, cy - 3)], color=BR)
    if cap == "polos":
        cv.rect(cx - 3, cy - 7, cx + 3, cy - 4, G1)
        cv.rect(cx - 3, cy - 7, cx + 3, cy - 7, G2)
        cv.px(cx, cy - 6, B)
    if wreath:
        for x in range(int(cx - 4), int(cx + 5)):
            if (x + int(cx)) % 2:
                cv.px(x, cy - 3, wreath)
        cv.px(cx - 4, cy - 2, wreath)
        cv.px(cx + 4, cy - 2, wreath)


def robe(cv, cx, top, bottom, w_top, w_hem, sway=0.0, folds=True, short=False):
    """A long chiton from the shoulders down: wider at the hem, folds in value bands."""
    pts = [(cx - w_top, top), (cx + w_top, top), (cx + w_hem + sway, bottom), (cx - w_hem + sway, bottom)]
    fill_poly(cv, pts)
    if folds:
        for y in range(int(top + 6), int(bottom)):
            t = (y - top) / max(1, bottom - top)
            hw = w_top + (w_hem - w_top) * t
            x0 = cx - hw + sway * t
            for k in range(1, 5):
                x = int(x0 + k * (2 * hw) / 5)
                cv.px(x, y, M1 if k > 2 else M2)
                if k <= 2:
                    cv.px(x - 1, y, M4 if k == 1 else M3)


def drape(cv, x0, y0, x1, y1, w=3):
    """A himation or a sash crossing the body: its lit edge, its folds, its shadow."""
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(int(n) + 1):
        x = x0 + (x1 - x0) * i / n
        y = y0 + (y1 - y0) * i / n
        for k in range(w):
            cv.px(round(x) + k, round(y), M4 if k == 0 else M3 if k < w - 1 else M1)
        cv.px(round(x) + w, round(y), M0)


def torso(cv, cx, top, waist, w_sh, w_waist, bare=False):
    fill_poly(cv, [(cx - w_sh, top), (cx + w_sh, top), (cx + w_waist, waist), (cx - w_waist, waist)])
    if bare:
        cv.px(cx - 2, top + 3, M2)
        cv.px(cx + 1, top + 3, M1)
        cv.px(cx, top + 5, M1)
        cv.px(cx, top + 7, M1)


def legs(cv, cx, top, bottom, stride=0, w=3):
    """Two legs, close together and solid (no gap at the thigh), feet at the bottom."""
    limb(cv, cx - 1.2, top, cx - 1.5 - stride, bottom, w + 1)
    limb(cv, cx + 1.2, top, cx + 1.5 + stride, bottom, w)
    cv.rect(cx - 2.5 - stride, bottom, cx - 0.5 - stride, bottom, M2)
    cv.rect(cx + 1.0 + stride, bottom, cx + 3 + stride, bottom, M1)


POSES = {}


def pose(name):
    def deco(fn):
        POSES[name] = fn
        return fn
    return deco


@pose("zeus")
def _zeus(cv):
    cx = 15.5
    robe(cv, cx + 0.5, 27, 50, 5, 8)
    torso(cv, cx, 16, 27, 6.5, 5, bare=True)
    drape(cv, cx - 6, 17, cx + 3, 29, 3)
    limb(cv, cx - 6, 17, cx - 10, 9, 3)                 # the right arm raised
    limb(cv, cx - 10, 9, cx - 10, 5, 2)
    cv.line(cx - 9, 0, cx - 12, 4, G2, 2)                 # the thunderbolt
    cv.line(cx - 12, 4, cx - 8, 5, G2, 2)
    cv.line(cx - 8, 5, cx - 11, 11, G1, 2)
    limb(cv, cx + 6, 17, cx + 10, 23, 3)                 # the left arm out, the eagle on it
    fill_poly(cv, [(cx + 9, 19), (cx + 12, 12), (cx + 16, 9), (cx + 14, 19)], color=BR)   # the raised wing
    cv.line(cx + 11, 13, cx + 15, 10, G1)
    fill_poly(cv, [(cx + 8, 20), (cx + 13, 18), (cx + 13, 23), (cx + 9, 23)], color=BR)    # the body
    cv.line(cx + 9, 21, cx + 12, 19, G1)
    cv.ellipse(cx + 12.5, 17, 1.8, 1.6, lambda dx, dy, d: M4 if dx < 0.5 else M3)         # the white head
    cv.px(cx + 14, 17, G2)
    cv.px(cx + 12, 16.5, K)
    head(cv, cx, 9, beard=True, hair="long")


@pose("poseidon")
def _poseidon(cv):
    cx = 15.5
    legs(cv, cx, 34, 49, stride=3, w=3)
    fill_poly(cv, [(cx - 5, 26), (cx + 5, 26), (cx + 7, 37), (cx - 7, 37)])   # a drape round the hips
    torso(cv, cx, 16, 27, 6.5, 5, bare=True)
    limb(cv, cx - 6, 17, cx - 9, 25, 3)
    cv.line(cx - 9, 1, cx - 9, 50, G1, 1)                 # the trident
    cv.line(cx - 10, 1, cx - 10, 50, G2, 1)
    for dx in (-3, 0, 3):
        cv.line(cx - 9 + dx, 0, cx - 9 + dx, 4, G2)
    cv.line(cx - 12, 4, cx - 6, 4, G2)
    limb(cv, cx + 6, 17, cx + 11, 21, 3)                 # the left arm flung out, striding
    head(cv, cx + 0.5, 9, beard=True, hair="long")


@pose("athena")
def _athena(cv):
    cx = 15.5
    robe(cv, cx, 22, 50, 5.5, 8.5)
    torso(cv, cx, 16, 23, 6, 5.5)
    fill_poly(cv, [(cx - 5, 17), (cx + 5, 17), (cx + 4, 22), (cx - 4, 22)], color=G1)   # the aegis
    cv.px(cx, 19, R)
    limb(cv, cx - 6, 17, cx - 10, 12, 3)                 # the spear arm, raised
    cv.line(cx - 10, 0, cx - 10, 50, BR)
    cv.line(cx - 11, 1, cx - 9, 1, M4)
    cv.px(cx - 10, 0, M4)
    cv.ellipse(cx + 9, 30, 5.5, 7, lambda dx, dy, d: G2 if d > 0.78 and dx < 0 else G1 if d > 0.72 else
               B if d > 0.2 else R)                       # the shield, held out
    head(cv, cx, 9, helm="athena", hair="long")
    cv.ellipse(cx + 7, 13, 1.8, 2.2, lambda dx, dy, d: M2 if dx < 0 else M1)   # the owl on her shoulder
    cv.px(cx + 6.5, 12.5, G2)
    cv.px(cx + 7.5, 12.5, G2)


@pose("artemis")
def _artemis(cv):
    cx = 15.5
    legs(cv, cx, 35, 49, stride=2)
    fill_poly(cv, [(cx - 5, 22), (cx + 5, 22), (cx + 6, 36), (cx - 6, 36)])  # the short chiton
    for y in range(26, 36, 3):
        cv.px(cx - 2, y, M4)
        cv.px(cx + 2, y, M1)
    torso(cv, cx, 16, 23, 5.5, 5)
    cv.rect(cx + 3, 13, cx + 5, 24, BR)                    # the quiver on her back
    cv.px(cx + 4, 12, M4)
    cv.px(cx + 3, 12, R)
    limb(cv, cx - 5, 17, cx - 11, 17, 2)                 # the bow arm, straight out
    for y in range(9, 26):
        t = (y - 17) / 8.5
        cv.px(cx - 13 + int(2.5 * t * t), y, G1)
        cv.px(cx - 12 + int(2.5 * t * t), y, G2 if abs(t) < 0.6 else G1)
    cv.line(cx - 13, 9, cx - 2, 17, M4)                   # the string, drawn back
    cv.line(cx - 13, 25, cx - 2, 17, M4)
    limb(cv, cx + 4, 17, cx - 2, 17, 2)                  # the drawing arm
    cv.line(cx - 14, 16, cx - 2, 16, BR)                 # the arrow
    cv.px(cx - 15, 16, M4)
    head(cv, cx, 9, hair="long")
    cv.ellipse(cx, 4.5, 2.6, 1.2, lambda dx, dy, d: G2)    # the crescent
    cv.px(cx, 4.5, M3)


@pose("apollo")
def _apollo(cv):
    cx = 15.5
    legs(cv, cx, 33, 49, stride=1, w=3)
    drape(cv, cx - 6, 18, cx + 4, 34, 3)
    torso(cv, cx, 16, 30, 6.5, 4.5, bare=True)
    fill_poly(cv, [(cx - 5, 30), (cx + 5, 30), (cx + 6, 35), (cx - 6, 35)])
    limb(cv, cx + 6, 17, cx + 2, 23, 3)
    fill_poly(cv, [(cx - 6, 17), (cx - 2, 17), (cx - 1, 27), (cx - 7, 27)], color=G1)   # the lyre
    cv.line(cx - 7, 16, cx - 8, 13, G2, 1)
    cv.line(cx - 1, 16, cx, 13, G2, 1)
    for x in range(int(cx - 6), int(cx - 1)):
        cv.line(x, 18, x, 25, M4)
    limb(cv, cx - 6, 17, cx - 6, 24, 2)
    head(cv, cx, 9, hair="long", wreath=G2)


@pose("hephaestus")
def _hephaestus(cv):
    cx = 15.5
    legs(cv, cx, 33, 49, stride=2, w=4)
    fill_poly(cv, [(cx - 7, 24), (cx + 7, 24), (cx + 8, 35), (cx - 8, 35)])   # the exomis
    torso(cv, cx, 16, 25, 8, 7, bare=True)
    drape(cv, cx + 4, 16, cx - 6, 25, 2)
    limb(cv, cx + 8, 17, cx + 10, 10, 4)                 # the hammer over his shoulder
    cv.line(cx + 10, 10, cx + 3, 3, BR, 2)
    cv.rect(cx, 0, cx + 5, 4, M1)
    cv.rect(cx, 0, cx + 5, 0, M3)
    cv.rect(cx, 1, cx, 4, M2)
    limb(cv, cx - 8, 17, cx - 10, 27, 4)                 # the other fist, the tongs
    cv.line(cx - 10, 27, cx - 12, 33, BR)
    head(cv, cx, 9, beard=True, cap="pilos")


@pose("hermes")
def _hermes(cv):
    cx = 15.5
    limb(cv, cx - 1, 33, cx - 5, 49, 4)                  # mid-step: one leg forward, one back
    limb(cv, cx + 2, 33, cx + 5, 46, 4)
    limb(cv, cx + 5, 46, cx + 7, 49, 3)
    for (x, y) in ((cx - 7, 47), (cx - 8, 46), (cx + 8, 47), (cx + 9, 46)):
        cv.px(x, y, M4)                                   # the winged sandals
    fill_poly(cv, [(cx - 5, 26), (cx + 5, 26), (cx + 5, 34), (cx - 5, 34)])
    torso(cv, cx, 16, 27, 6, 4.5, bare=True)
    fill_poly(cv, [(cx + 2, 15), (cx + 7, 15), (cx + 9, 30), (cx + 4, 28)])  # the chlamys from his shoulder
    limb(cv, cx - 6, 17, cx - 9, 24, 2)
    cv.line(cx - 10, 6, cx - 10, 40, G1)                  # the caduceus
    cv.ellipse(cx - 10, 6, 1.8, 1.8, lambda dx, dy, d: G2)
    for y in range(10, 24, 4):
        cv.px(cx - 11, y, G2)
        cv.px(cx - 9, y + 2, G2)
    cv.px(cx - 12, 8, M4)
    cv.px(cx - 8, 8, M4)
    limb(cv, cx + 6, 17, cx + 9, 12, 2)
    head(cv, cx, 9, cap="petasos")


@pose("ares")
def _ares(cv):
    cx = 15.5
    legs(cv, cx, 34, 49, stride=2, w=3)
    fill_poly(cv, [(cx - 5, 26), (cx + 5, 26), (cx + 6, 35), (cx - 6, 35)])
    for y in range(28, 35, 2):
        cv.px(cx - 3, y, BR)
        cv.px(cx + 3, y, BR)
    torso(cv, cx, 16, 27, 7, 5.5)
    fill_poly(cv, [(cx - 6, 16), (cx + 6, 16), (cx + 5, 26), (cx - 5, 26)], color=G1)    # the cuirass
    cv.line(cx, 17, cx, 25, BR)
    limb(cv, cx - 7, 17, cx - 10, 22, 3)
    cv.line(cx - 10, 0, cx - 10, 50, BR)                 # the spear
    cv.line(cx - 11, 1, cx - 9, 1, M4)
    cv.px(cx - 10, 0, M4)
    cv.ellipse(cx + 5, 29, 6, 7.5, lambda dx, dy, d: G2 if d > 0.8 and dx < 0 else G1 if d > 0.7 else
               R if d > 0.22 else G2)                    # the shield braced in front
    head(cv, cx, 9, helm="corinthian")


@pose("aphrodite")
def _aphrodite(cv):
    cx = 15.5
    robe(cv, cx + 1, 28, 50, 5, 7.5, sway=-1.5)          # the drape low round her hips, the hip shifted
    fill_poly(cv, [(cx - 5, 16), (cx + 5, 16), (cx + 6, 29), (cx - 3, 29)])   # contrapposto: the hip out
    drape(cv, cx - 5, 20, cx + 5, 22, 2)
    limb(cv, cx - 5, 17, cx - 6, 10, 2)                  # a hand raised to her hair
    limb(cv, cx + 5, 17, cx + 8, 27, 2)
    head(cv, cx - 0.5, 9, hair="long")
    cv.ellipse(cx + 1, 49, 4.5, 2.4, lambda dx, dy, d: R if int(dx + 6) % 2 else M4)   # the scallop shell


@pose("demeter")
def _demeter(cv):
    cx = 15.5
    robe(cv, cx, 16, 50, 6, 8.5)
    drape(cv, cx - 6, 18, cx + 5, 30, 3)
    limb(cv, cx - 6, 18, cx, 25, 3)                      # cradling the sheaf
    for i in range(7):
        x = cx - 7 + i
        cv.line(x, 28, x - 3 + i * 0.5, 13, G1)
        cv.px(x - 3 + i * 0.5, 13, G2)
        cv.px(x - 3 + i * 0.5, 14, G2)
    cv.rect(cx - 6, 24, cx, 25, BR)
    limb(cv, cx + 6, 18, cx + 8, 28, 2)
    head(cv, cx + 0.5, 9, veil=True, cap="polos")


@pose("hera")
def _hera(cv):
    cx = 15.5
    fill_poly(cv, [(cx - 9, 10), (cx + 9, 10), (cx + 9, 48), (cx - 9, 48)], color=B)   # the throne's back
    fill_poly(cv, [(cx - 9, 10), (cx + 9, 10), (cx + 9, 11), (cx - 9, 11)], color=G2)
    for y in range(13, 46, 4):
        cv.px(cx - 8, y, G1)
        cv.px(cx + 8, y, G1)
    fill_poly(cv, [(cx - 6, 28), (cx + 7, 28), (cx + 7, 37), (cx - 6, 37)])   # her lap, seated
    limb(cv, cx - 3, 37, cx - 3, 49, 3)
    limb(cv, cx + 3, 37, cx + 3, 49, 3)
    fill_poly(cv, [(cx - 5, 16), (cx + 5, 16), (cx + 5, 29), (cx - 5, 29)])
    drape(cv, cx - 5, 17, cx + 4, 28, 2)
    limb(cv, cx - 5, 17, cx - 7, 26, 2)
    cv.line(cx - 8, 4, cx - 8, 48, G1)                    # the sceptre, a cuckoo on it
    cv.ellipse(cx - 8, 4, 1.6, 1.6, lambda dx, dy, d: B)
    cv.px(cx - 7, 3, G2)
    limb(cv, cx + 5, 17, cx + 6, 27, 2)
    cv.ellipse(cx + 8, 33, 1.6, 1.6, lambda dx, dy, d: T1 if d > 0.4 else B)   # a peacock's eye on the arm
    head(cv, cx, 10, veil=True, cap="polos")


@pose("dionysus")
def _dionysus(cv):
    cx = 15.5
    robe(cv, cx, 24, 50, 5, 7.5)
    torso(cv, cx, 16, 25, 6, 5, bare=True)
    drape(cv, cx + 5, 16, cx - 5, 27, 3)
    limb(cv, cx + 6, 17, cx + 9, 24, 3)
    cv.line(cx + 10, 4, cx + 10, 48, BR)                 # the thyrsus, a pine cone on it
    cv.ellipse(cx + 10, 3.5, 2, 2.8, lambda dx, dy, d: G1 if dx > 0 else G2)
    limb(cv, cx - 6, 17, cx - 10, 11, 2)                 # the cup raised
    cv.ellipse(cx - 11, 9, 3, 1.8, lambda dx, dy, d: G2 if dy < 0 else G1)
    cv.px(cx - 11, 8, R)
    cv.px(cx - 12, 8, R)
    head(cv, cx, 9, hair="long", wreath=B)


@pose("hestia")
def _hestia(cv):
    cx = 15.5
    robe(cv, cx, 16, 50, 6, 8)
    drape(cv, cx - 6, 18, cx + 5, 32, 3)
    limb(cv, cx - 6, 18, cx - 2, 24, 3)
    limb(cv, cx + 6, 18, cx + 2, 24, 3)
    cv.ellipse(cx, 24.5, 4.5, 1.8, lambda dx, dy, d: G1 if dy > 0 else G2)   # the hearth-bowl
    for (dx, hh) in ((-2, 4), (0, 6), (2, 4)):
        for y in range(int(23 - hh), 24):
            cv.px(cx + dx, y, R if y > 23 - hh + 1 else G2)
        cv.px(cx + dx + 1, 22, BR)
    head(cv, cx, 9, veil=True)


def statue_v2(god):
    cv = Cv()
    plinth(cv)
    fig = Cv()
    POSES[god](fig)
    fig.outline(K)
    m = fig.a > 0
    cv.a[m] = fig.a[m]
    return cv.a


statue = statue_v2


GODS = ["hestia", "hermes", "demeter", "dionysus", "artemis", "hephaestus",
        "aphrodite", "apollo", "ares", "poseidon", "athena", "hera", "zeus"]


def save(arr, path):
    im = Image.fromarray(arr.astype(np.uint8), "P")
    flat = []
    for c in PAL:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path, transparency=0)


def main():
    args = sys.argv[1:]
    arrs = {g: statue(g) for g in GODS}
    if "--write" in args:
        for g, a in arrs.items():
            save(a, OUT / f"statue_{g}.png")
        PAL_OUT.write_text("JASC-PAL\n0100\n16\n" + "".join(f"{r} {g_} {b}\n" for r, g_, b in PAL))
        print(f"wrote {len(arrs)} statues and {PAL_OUT}")
    if "--preview" in args:
        out = args[args.index("--preview") + 1]
        sheet = Image.new("RGB", (len(GODS) * 34 + 2, 66), (208, 216, 240))
        for i, g in enumerate(GODS):
            a = arrs[g]
            rgb = np.array([PAL[v] for v in a.ravel()], np.uint8).reshape(H, W, 3)
            im = Image.fromarray(rgb)
            mask = Image.fromarray(((a > 0) * 255).astype(np.uint8))
            sheet.paste(im, (2 + i * 34, 1), mask)
        sheet.save(out)
        big = sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST)
        big.save(out.replace(".png", "_3x.png"))
        print(out)


if __name__ == "__main__":
    main()
