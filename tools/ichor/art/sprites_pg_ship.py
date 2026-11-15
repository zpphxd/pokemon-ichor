#!/usr/bin/env python3
"""The Euploia at sea: the player's ship avatar for the post-game's sailing
layer (design/ODYSSEY.md §2 and §4, design/postgame/SPRITES.md).

Usage:
    python3 tools/ichor/art/sprites_pg_ship.py [--write] [--preview DIR]

--write    writes graphics/object_events/pics/ichor/pg_euploia.png (sail full)
           and pg_euploia_slack.png (sail slack), each nine 64x64 frames side
           by side, and the shared palette
           graphics/object_events/palettes/ichor_euploia.pal
--preview  writes DIR/euploia_frames.png (both sheets at 3x over the aethos
           sea) for review

Both sheets use the standard Emerald layout so sAnimTable_Standard plays them
and the engine can swap one for the other in place:

    0 face south   1 face north   2 face west
    3, 4 go south  5, 6 go north  7, 8 go west     (east is west, flipped)

The ship is a black-hulled trireme seen from above at three-quarters, as Homer
paints them: black ships with red cheeks (miltoparēos) and a painted eye at the
bow, a three-finned bronze ram at the waterline, two banks of oars, the
aphlaston curling over the stern, two steering oars, and a linen sail on a grid
of brails with the Dioskouroi's star, the sailor's sign of fair sailing.

The oars carry the walk: the standing frame holds them square to the hull,
walk A has them swept aft (the end of the stroke, blades in the water, a
splash at each), walk B forward (the catch). sAnim_Go* plays A, stand, B,
stand, so the banks row. The wake streams from the stern and a bow wave curls
round the ram while she moves; at rest only a ripple rings the hull.

Where the ship sits in the frame: a 64x64 object stands on the bottom-middle
16x16 of its frame (rows 48-63, columns 24-39). Facing south the bow and ram
are on that tile; facing north the stern; facing west or east, midships.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/ichor")
PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_euploia.pal")
N = 64

COLORS = [
    # char, name, rgb                        used for
    ("k", "ink", (24, 24, 40)),             # outline, the eye's pupil, ropes in shadow
    ("d", "pitch", (48, 48, 64)),           # the black hull
    ("D", "pitch_l", (96, 96, 112)),        # sheen on the pitch, lit wales
    ("w", "wood_d", (112, 72, 40)),         # deck seams, oar shafts, the yard's shade
    ("W", "wood", (176, 120, 72)),          # deck planks, mast, yard
    ("e", "wood_l", (224, 176, 112)),       # lit planks, oar blades, the gangway
    ("o", "bronze_d", (168, 104, 40)),      # ram and fittings in shade
    ("O", "bronze", (240, 192, 88)),        # the ram, the stern's gilt
    ("R", "red_d", (136, 32, 40)),          # red in shade, the star seen through the sail
    ("r", "red", (208, 64, 48)),            # the cheeks, the Dioskouroi's star
    ("l", "linen_d", (200, 184, 152)),      # sail shade, brail lines
    ("L", "linen", (248, 240, 216)),        # the sail, the eye's white
    ("b", "sea_d", (32, 72, 136)),          # the hull's shadow on the water
    ("a", "spray", (128, 184, 232)),        # wake and ripple
    ("f", "foam", (240, 248, 248)),         # foam
]
PAL = Palette([(name, rgb) for _, name, rgb in COLORS])
LEGEND = {ch: name for ch, name, _ in COLORS}


class Pic:
    """A 64x64 index map painted with palette chars."""

    def __init__(self):
        self.a = np.zeros((N, N), np.int32)

    def idx(self, ch):
        return 0 if ch in (None, "_") else PAL[LEGEND[ch]]

    def px(self, x, y, ch, under=False):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < N and 0 <= y < N:
            if under and self.a[y, x] != 0:
                return
            self.a[y, x] = self.idx(ch)

    def get(self, x, y):
        if 0 <= x < N and 0 <= y < N:
            return self.a[y, x]
        return -1

    def mask(self, fn):
        im = Image.new("L", (N, N), 0)
        fn(ImageDraw.Draw(im))
        return np.array(im) > 0

    def poly(self, pts, ch, clip=None, under=False):
        m = self.mask(lambda d: d.polygon([tuple(p) for p in pts], fill=255, outline=255))
        self.fill(m, ch, clip, under)

    def fill(self, m, ch, clip=None, under=False):
        m = m.copy()
        if clip is not None:
            m &= np.isin(self.a, [self.idx(c) for c in clip])
        if under:
            m &= self.a == 0
        self.a[m] = self.idx(ch)

    def line(self, pts, ch, under=False):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for x, y in bresenham(int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))):
                self.px(x, y, ch, under)

    def patch(self, x0, y0, rows, under=False):
        """ASCII patch: '.' and ' ' leave a pixel, '_' clears it."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in ". ":
                    continue
                self.px(x0 + i, y0 + j, ch, under)

    def outline(self, region, ch="k"):
        """Pixels of `region` (a bool mask) that touch a pixel outside it
        (4-neighbour) take `ch`."""
        r = region
        nb = np.zeros_like(r)
        nb[1:, :] |= ~r[:-1, :]
        nb[:-1, :] |= ~r[1:, :]
        nb[:, 1:] |= ~r[:, :-1]
        nb[:, :-1] |= ~r[:, 1:]
        nb[0, :] = True
        nb[-1, :] = True
        nb[:, 0] = True
        nb[:, -1] = True
        self.a[r & nb] = self.idx(ch)

    def region(self, chars):
        return np.isin(self.a, [self.idx(c) for c in chars])


def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# ==========================================================================
# Shared parts
# ==========================================================================

POSE_STAND, POSE_A, POSE_B = "stand", "A", "B"
SWEEP = {POSE_STAND: 0, POSE_A: -1, POSE_B: 1}   # -1 aft (end of stroke), +1 forward (catch)

# The Dioskouroi's star: a red disc with eight rays, for the sail's face
STAR = [
    "....r....",
    ".r..r..r.",
    "..r.r.r..",
    "...rrr...",
    "rrrrRrrrr",
    "...rrr...",
    "..r.r.r..",
    ".r..r..r.",
    "....r....",
]
# seen through the linen from behind
STAR_BACK = [
    "...R...",
    ".R.R.R.",
    "..RRR..",
    "RRRRRRR",
    "..RRR..",
    ".R.R.R.",
    "...R...",
]
# braced, seen at an angle (west view)
STAR_SIDE = [
    "..r..",
    "r.r.r",
    ".rrr.",
    "rrRrr",
    ".rrr.",
    "r.r.r",
    "..r..",
]


def half_width(ds, length, beam=8.0, stern_run=8.0, bow_run=14.0):
    """The hull's half-beam at distance ds from the stern tip."""
    if ds < 0 or ds > length:
        return None
    st = min(1.0, ds / stern_run)
    bw = min(1.0, (length - ds) / bow_run)
    return max(0.6, beam * min(math.sqrt(st) * 1.02, 0.15 + 0.85 * bw ** 0.85))


# ==========================================================================
# South and north: the hull runs down the frame
# ==========================================================================

CX = 32  # the hull is symmetric about the line between columns 31 and 32


# Half-beams from the stern tip to the deck's point at the bow. Columns
# CX-h .. CX-1+h; midships h=9, columns 23..40.
_STERN_RUN = [2, 4, 5, 6, 7, 8, 8, 9]
_BOW_RUN = [9, 8, 8, 7, 7, 6]
_LENGTH = 40   # deck rows, stern tip to the bow face


def deck_rows(bow_down):
    """{y: h} for the deck, stern tip first; and the stern and bow-face rows."""
    hs = _STERN_RUN + [9] * (_LENGTH - len(_STERN_RUN) - len(_BOW_RUN)) + _BOW_RUN
    if bow_down:
        stern = 9
        rows = {stern + i: h for i, h in enumerate(hs)}
        face = stern + len(hs)          # the bow's face starts here
    else:
        stern = 51
        rows = {stern - i: h for i, h in enumerate(hs)}
        face = stern - len(hs)          # the deck's point, where the stem rises
    return rows, stern, face


def deck_row(h):
    """One row of the deck, outline to outline, 2h wide."""
    if h <= 2:
        return "k" * (2 * h)
    if h <= 5:
        return "k" + "D" + "d" * (2 * h - 3) + "k"
    inner = 2 * h - 10
    deck = []
    for i in range(inner):
        rel = i - inner // 2           # 0 and -1 are the gangway
        if rel in (-1, 0):
            deck.append("e")
        elif rel in (-4, 3):
            deck.append("w")
        elif rel == -3:
            deck.append("e")
        else:
            deck.append("W")
    # the black wales (lit on the left), the rails, then the planking
    return "kDdd" + "w" + "".join(deck) + "w" + "dddk"


def draw_hull_vertical(p, bow_down):
    rows, stern, face = deck_rows(bow_down)
    # the hull's shadow on the water, a little down and right
    for y, h in rows.items():
        for x in range(CX - h + 1, CX + h + 2):
            p.px(x, y + 2, "b", under=True)
    for y, h in rows.items():
        r = deck_row(h)
        p.patch(CX - h, y, [r])
    # thwarts across the deck, the gangway left whole
    for i in range(12, 34, 5):
        y = stern + (i if bow_down else -i)
        h = rows[y]
        for x in range(CX - h + 5, CX + h - 5):
            if x not in (CX - 1, CX):
                p.px(x, y, "w")
    return rows, stern, face


# The bow seen from ahead and above: red cheeks with the painted eyes, the
# stem's black face running down to the ram at the waterline.
BOW_FACE_SOUTH = [
    "kDddwweeWWwdddk.",
    "kdrrrrdwwdrrrrdk",
    "kdrLLrddddrLLrdk",
    "drLkkLrddrLkkLrd",
    "kdrLLrddddrLLrdk",
    ".kdrrrddddrrrdk.",
    "..kdRdDDddRdk...",
    "...kddDDddk.....",
    "....kdDDdk......",
    ".....kDDk.......",
    "......kk........",
]
RAM_SOUTH = [
    "..kkkk..",
    ".kOOOok.",
    "kOOOOOok",
    ".kOooOk.",
    "..kOOk..",
    "...kk...",
]

# Facing north: the deck runs to a point, the stem's top, and the ram's tip
# beyond it at the waterline.
BOW_NORTH = [
    "..kk..",
    ".kOOk.",
    "kOOOok",
    "kOooOk",
    ".kddk.",
    "kDddwk",
]

# The aphlaston facing south: a fan of curled timbers rising over the stern
APHLASTON_SOUTH = [
    ".kk..kk.",
    "kOOkkOOk",
    "kddkkddk",
    ".kdkkdk.",
    ".kdDDdk.",
    "..kdDk..",
    "..kdDk..",
    ".kddDdk.",
    "kddRRddk",
]

# Facing north: the transom with its gilt band, the aphlaston rising from it
# and curling forward over the after deck
APHLASTON_NORTH = [
    "kOk..kOk",
    "kdDkkDdk",
    ".kdDDdk.",
    "..kddk..",
    "..kdDk..",
    "..kdDk..",
    "..kRrk..",
    "..kdDk..",
    "..kdDk..",
    "..kdDk..",
    "..kdDk..",
]
TRANSOM_NORTH = [
    "kdOOOOOOOOOOdk",
    "kddddDDdddddk.",
    ".kdddDDddddk..",
    "..kddDDdddk...",
    "...kdDDddk....",
    "....kkkkk.....",
]


def draw_bow_stern_south(p, stern, face):
    # the bow face: 16 px wide, centred
    for j, r in enumerate(BOW_FACE_SOUTH):
        p.patch(CX - 8, face - 1 + j, [r])
    ram_y = face - 1 + len(BOW_FACE_SOUTH) - 2
    for j, r in enumerate(RAM_SOUTH):
        p.patch(CX - 4, ram_y + j, [r])
    # steering oars on the quarters, blades trailing aft in the water
    p.line([(CX - 7, stern + 5), (CX - 11, stern - 3)], "W")
    p.line([(CX + 6, stern + 5), (CX + 10, stern - 3)], "W")
    p.patch(CX - 13, stern - 7, ["kek", "kek", "kWk", ".k."])
    p.patch(CX + 9, stern - 7, ["kek", "kek", "kWk", ".k."])
    for j, r in enumerate(APHLASTON_SOUTH):
        p.patch(CX - 4, stern - 8 + j, [r])


def draw_bow_stern_north(p, stern, face):
    for j, r in enumerate(BOW_NORTH):
        p.patch(CX - 3, face - 5 + j, [r])
    p.line([(CX - 7, stern - 5), (CX - 11, stern + 4)], "W")
    p.line([(CX + 6, stern - 5), (CX + 10, stern + 4)], "W")
    p.patch(CX - 13, stern + 3, [".k.", "kWk", "kek", "kek"])
    p.patch(CX + 9, stern + 3, [".k.", "kWk", "kek", "kek"])
    for j, r in enumerate(TRANSOM_NORTH):
        p.patch(CX - 7, stern + j, [r])
    for j, r in enumerate(APHLASTON_NORTH):
        p.patch(CX - 4, stern - 10 + j, [r])


def draw_oars_vertical(p, rows, bow_down, stern, pose):
    """Two banks of oars both sides, drawn under the hull. Walk A has them
    swept aft with a splash at each blade, walk B forward."""
    aft = -1 if bow_down else 1
    sweep = SWEEP[pose]                 # -1 aft, +1 forward
    for i, ds in enumerate(range(12, 37, 3)):
        bank = i % 2
        y = stern + (ds if bow_down else -ds)
        h = rows[y]
        length = 11 if bank == 0 else 8
        droop = 2 if bank == 0 else 1
        swing = (4 if bank == 0 else 3)
        dy = droop + (aft * swing if sweep == -1 else (-aft * swing if sweep == 1 else 0))
        for side in (-1, 1):
            rx = (CX - h - 1) if side < 0 else (CX + h)
            tx = rx + side * length
            ty = y + dy
            p.line([(rx, y), (tx - side, ty)], "W", under=True)
            p.px(tx, ty, "e", under=True)
            p.px(tx + side, ty, "e", under=True)
            p.px(tx, ty + 1, "w", under=True)
            p.px(tx + side, ty + 1, "w", under=True)
            if pose == POSE_A:
                p.px(tx + 2 * side, ty, "f", under=True)
                p.px(tx + side, ty - aft, "a", under=True)
                p.px(tx + 2 * side, ty + 1, "a", under=True)


def draw_wake_vertical(p, rows, bow_down, stern, tip, pose):
    """tip: the ram's tip row. Wake astern, a bow wave, ripples at rest."""
    aft = -1 if bow_down else 1
    fwd = -aft
    if pose == POSE_STAND:
        for (dx, dy) in ((-12, 3), (11, 5), (-14, 18), (13, 21), (-13, 31), (12, 34)):
            y = stern - aft * dy
            for k in (0, 1):
                p.px(CX + dx + k, y, "a", under=True)
        for dx in (-6, -5, 4, 5):
            p.px(CX + dx, tip - fwd, "a", under=True)
        return
    phase = 0 if pose == POSE_A else 1
    # astern: a V of broken foam with churned water between
    for i in range(1, 13):
        y = stern + aft * i
        spread = 3 + (i * 2) // 3
        for side in (-1, 1):
            x = (CX - 1 - spread) if side < 0 else (CX + spread)
            if (i + phase) % 3 != 0:
                p.px(x, y, "f", under=True)
            else:
                p.px(x, y, "a", under=True)
            p.px(x + side, y, "a", under=True)
        if i < 7:
            for x in range(CX - 2, CX + 2):
                if (x + i + phase) % 2 == 0:
                    p.px(x, y, "a", under=True)
    # the bow wave: a white moustache either side of the stem, swept aft
    arc = [(5, 0), (6, -1), (7, -2), (8, -3), (9, -5), (10, -7), (10, -9)]
    for side in (-1, 1):
        for j, (dx, dy) in enumerate(arc):
            x = (CX - 1 - dx) if side < 0 else (CX + dx)
            y = tip - fwd * 2 + fwd * dy
            p.px(x, y, "f", under=True)
            p.px(x + side, y, "a", under=True)
            if (j + phase) % 2 == 0:
                p.px(x + 2 * side, y - fwd, "a", under=True)
    for x in range(CX - 3, CX + 3):
        p.px(x, tip + fwd, "f" if (x + phase) % 2 else "a", under=True)
    for x in (CX - 5, CX + 4):
        p.px(x, tip, "a", under=True)


def draw_mast_vertical(p, foot, top):
    p.line([(CX - 1, top), (CX - 1, foot)], "W")
    p.line([(CX, top), (CX, foot)], "w")
    p.px(CX - 1, top - 1, "k")
    p.px(CX, top - 1, "k")


def sail_rows_vertical(full, face):
    """{y: (x0, x1)} of the sail, the yard's row, and the foot by column."""
    yard = 10 if face == "south" else 11
    rows = {}
    if full:
        top, foot = yard + 1, yard + 18
        for y in range(top, foot + 1):
            t = (y - top) / (foot - top)
            amp = 1.6 if face == "south" else 0.8
            bulge = int(round(amp * math.sin(math.pi * t)))
            rows[y] = (CX - 13 - bulge, CX + 12 + bulge)
        extra = {}
        if face == "south":
            for x in range(CX - 10, CX + 10):
                d = 1 - ((x - (CX - 0.5)) / 10.5) ** 2
                extra[x] = foot + int(round(2.5 * d))
        else:
            for x in range(CX - 13, CX + 13):
                d = 1 - ((x - (CX - 0.5)) / 13.0) ** 2
                extra[x] = foot - int(round(2.0 * d))
        return yard, rows, extra
    top, foot = yard + 1, yard + 14
    for y in range(top, foot + 1):
        rows[y] = (CX - 12, CX + 11)
    extra = {}
    for x in range(CX - 12, CX + 12):
        # festoons where the slack sail hangs between brails
        m = (x - CX) % 6
        extra[x] = foot + (1 if m in (2, 3) else 0) - (1 if m == 0 else 0)
    return yard, rows, extra


def draw_sail_vertical(p, full, face):
    yard, rows, foot = sail_rows_vertical(full, face)
    m = np.zeros((N, N), bool)
    for y, (x0, x1) in rows.items():
        m[y, x0:x1 + 1] = True
    last = max(rows)
    for x, fy in foot.items():
        if fy > last:
            m[last:fy + 1, x] = True
        elif fy < last:
            m[fy + 1:last + 1, x] = False
    xs = [x for (x0, x1) in rows.values() for x in (x0, x1)]
    sx0, sx1 = min(xs), max(xs)
    ys = np.where(m.any(axis=1))[0]
    sy0, sy1 = ys.min(), ys.max()
    yy, xx = np.mgrid[0:N, 0:N]
    if full and face == "south":
        # the belly faces the viewer: brightest left of centre
        cx = (sx0 + sx1) / 2 - 2
        d = ((xx - cx) / ((sx1 - sx0) / 2 + 1)) ** 2 + ((yy - (sy0 + sy1) / 2 - 1) / ((sy1 - sy0) / 2 + 2)) ** 2
        lit = d < 0.62
    elif full:
        # the back of a bellied sail: in shade, lit along its left edge
        lit = (xx < sx0 + 7) & (yy > sy0 + 1)
    else:
        lit = ((xx - CX) % 6 < 3)
    p.fill(m, "l")
    p.fill(m & lit, "L")
    for x in range(sx0, sx1 + 1):
        if (x - CX) % 6 == 3:
            for y in np.where(m[:, x])[0]:
                p.px(x, y, "l")
    if full:
        for y in (sy0 + 6, sy0 + 12):
            for x in range(sx0, sx1 + 1):
                if m[y, x] and p.get(x, y) == p.idx("L"):
                    p.px(x, y, "l")
    else:
        for x in range(sx0, sx1 + 1):
            if (x - CX) % 6 == 0:
                for y in np.where(m[:, x])[0]:
                    if y > sy0 + 1:
                        p.px(x, y, "k" if y > sy0 + 4 else "l")
    if full and face == "south":
        p.patch(CX - 5, sy0 + 4, STAR)
    elif full:
        p.patch(CX - 4, sy0 + 5, STAR_BACK)
    else:
        p.patch(CX - 2, sy0 + 6, ["r.", "rr", "Rr", "r.", "R."])
    p.outline(m)
    y0 = sy0 - 1
    for x in range(sx0 - 2, sx1 + 3):
        p.px(x, y0, "W")
        p.px(x, y0 - 1, "k")
    p.px(sx0 - 3, y0, "k")
    p.px(sx1 + 3, y0, "k")
    for x in range(sx0 - 1, sx1 + 2, 2):
        p.px(x, y0, "e")
    for x in range(sx0, sx1 + 1):
        if (x - CX) % 6 == 3:
            p.px(x, y0 + 1, "w")
    return sy1


def frame_vertical(full, face, pose):
    """face 'south' (bow down) or 'north' (bow up)."""
    bow_down = face == "south"
    p = Pic()
    rows, stern, face_y = draw_hull_vertical(p, bow_down)
    if bow_down:
        draw_bow_stern_south(p, stern, face_y)
        tip = face_y - 1 + len(BOW_FACE_SOUTH) - 2 + len(RAM_SOUTH) - 1
    else:
        draw_bow_stern_north(p, stern, face_y)
        tip = face_y - 5
    draw_oars_vertical(p, rows, bow_down, stern, pose)
    draw_wake_vertical(p, rows, bow_down, stern, tip, pose)
    foot = stern + (24 if bow_down else -24)
    if bow_down:
        draw_mast_vertical(p, foot, foot - 6)
        draw_sail_vertical(p, full, face)
    else:
        draw_sail_vertical(p, full, face)
        draw_mast_vertical(p, foot, 9)
        p.patch(CX - 1, 7, ["kk", "OO", "oO"])
    return p.a


# ==========================================================================
# West: the hull runs across the frame, bow to the left
# ==========================================================================

GUNWALE = 43      # near gunwale (top of the black side)
FAR = 37          # far gunwale
WATER = 52        # waterline midships


def side_profile():
    """For each column, (deck_top, side_top, keel) of the hull, bow at x=5."""
    prof = {}
    for x in range(5, 59):
        # the sheer rises toward the stern and a little at the bow
        sheer = 0
        if x < 12:
            sheer = -((12 - x) // 4)
        if x > 46:
            sheer = -((x - 46) * (x - 46)) // 18
        far = FAR + sheer
        near = GUNWALE + sheer
        keel = WATER
        if x < 9:
            keel = WATER - (9 - x) // 2
        if x > 50:
            keel = WATER - ((x - 50) * (x - 50)) // 6
        if keel < near + 2:
            keel = near + 2
        prof[x] = (far, near, keel)
    return prof


def draw_hull_side(p, pose):
    prof = side_profile()
    # shadow on the water under and right of the hull
    for x, (far, near, keel) in prof.items():
        for y in range(keel + 1, keel + 3):
            p.px(x + 1, y, "b", under=True)
    body = np.zeros((N, N), bool)
    for x, (far, near, keel) in prof.items():
        body[far:keel + 1, x] = True
    p.fill(body, "d")
    for x, (far, near, keel) in prof.items():
        # the deck, foreshortened: planks run fore and aft
        for y in range(far + 1, near):
            rel = y - far
            ch = "W"
            if rel == 1:
                ch = "w"
            elif rel == 2:
                ch = "e"
            elif rel == (near - far) - 1:
                ch = "w"
            elif rel == 4:
                ch = "e" if x % 2 == 0 else "W"
            p.px(x, y, ch)
        # the near wale: a lit strake under the gunwale, oar ports below it
        p.px(x, near, "D")
        p.px(x, near + 1, "d")
        p.px(x, keel - 1, "d")
        if near + 3 < keel - 1 and x % 2 == 0:
            p.px(x, near + 3, "D")
    # cross-beams on the deck
    for x in range(14, 50, 6):
        far, near, _ = prof[x]
        for y in range(far + 1, near):
            p.px(x, y, "w")
    # oar ports along the outrigger
    for x in oar_xs_side():
        far, near, keel = prof[x]
        p.px(x, near + 2, "k")
    p.outline(body)
    # the bow: red cheek and the eye on the black side, the stem
    p.patch(4, GUNWALE - 3, [
        "..k..........",
        ".kDk.........",
        ".kdRrrrrk....",
        "kdrrLLLrrd...",
        "kdrLkkLLrd...",
        "kdrrLLLrrd...",
        "kddRrrrrRd...",
        ".kdddddddd...",
        "..kdddddddd..",
    ])
    # the ram at the waterline: three fins, bronze
    p.patch(0, WATER - 5, [
        "....kkk",
        "..kkOOk",
        ".kOOOok",
        "kOoOOOk",
        ".kOOook",
        "..kkook",
        "....kk.",
    ])
    # the stern rises and curls forward into the aphlaston
    p.patch(51, 18, [
        "......kkk...",
        ".....kOOk...",
        "...kk.kdk...",
        "..kOk.kdk...",
        "..kdk.kdDk..",
        "...kdkkddk..",
        "...kddkdDk..",
        "....kdddDk..",
        "....kddddk..",
        ".....kdddk..",
        ".....kdDdk..",
        ".....kddDk..",
        "....kdddDk..",
        "....kdddDk..",
        "...kRdddDk..",
        "...kdOOOdk..",
        "..kdddddDk..",
        "..kddddDk...",
        ".kdddddDk...",
        "kddddddk....",
        "dddddddk....",
        "ddddddk.....",
    ], under=False)


def oar_xs_side():
    return list(range(13, 48, 4))


def draw_oars_side(p, pose, near_side):
    prof = side_profile()
    sweep = SWEEP[pose]
    for i, x in enumerate(oar_xs_side()):
        far, near, keel = prof[x]
        bank = i % 2
        if near_side:
            y0 = near + 3
            length = 12 if bank == 0 else 9
            ty = y0 + length
            tx = x + 1 + sweep * (-4 if bank == 0 else -3)
            if sweep == -1:
                tx = x + 1 + (4 if bank == 0 else 3)
            p.line([(x, y0), (tx, ty - 1)], "W")
            p.px(tx, ty, "e")
            p.px(tx, ty + 1, "e")
            p.px(tx + 1, ty + 1, "w")
            if pose == POSE_A:
                p.px(tx - 1, ty + 2, "f", under=True)
                p.px(tx + 1, ty + 2, "a", under=True)
                p.px(tx + 2, ty + 1, "a", under=True)
        else:
            y0 = far
            length = 6 if bank == 0 else 4
            ty = y0 - length
            tx = x + sweep * (-3 if bank == 0 else -2)
            if sweep == -1:
                tx = x + (3 if bank == 0 else 2)
            p.line([(x, y0), (tx, ty + 1)], "w")
            p.px(tx, ty, "e")


def draw_wake_side(p, pose):
    prof = side_profile()
    if pose == POSE_STAND:
        for (x, y) in ((2, WATER + 3), (9, WATER + 4), (56, WATER + 2), (60, WATER + 3),
                       (30, WATER + 9), (44, WATER + 9)):
            p.px(x, y, "a", under=True)
            p.px(x + 1, y, "a", under=True)
        return
    phase = 0 if pose == POSE_A else 1
    # astern: foam streaming right from the stern
    for i in range(0, 8):
        x = 56 + i
        for j, y in enumerate((WATER - 4 - i // 3, WATER, WATER + 1 + i // 2)):
            on = (i + j + phase) % 3 != 0
            if on:
                p.px(x, y, "f" if j == 1 else "a", under=True)
    # alongside the waterline
    for x, (far, near, keel) in prof.items():
        if 8 < x < 52 and (x + phase) % 4 == 0:
            p.px(x, keel + 3, "a", under=True)
    # the bow wave piled up at the ram
    p.patch(0, WATER - 6, [
        "f......",
        "af.....",
        ".a.....",
    ], under=True)
    for dx, dy in ((1, 2), (2, 3), (3, 3), (5, 4), (7, 4), (9, 3)):
        p.px(dx + phase, WATER + dy, "f" if (dx + phase) % 2 else "a", under=True)


def draw_mast_side(p, foot, top, x=29):
    p.line([(x, top), (x, foot)], "W")
    p.line([(x + 1, top), (x + 1, foot)], "w")
    p.px(x, top - 1, "k")
    p.px(x + 1, top - 1, "k")


def draw_sail_side(p, full):
    m = np.zeros((N, N), bool)
    yard = 7
    if full:
        top, foot = yard + 1, yard + 26
        for y in range(top, foot + 1):
            t = (y - top) / (foot - top)
            bulge = int(round(3.2 * math.sin(math.pi * min(1.0, t * 1.08))))
            x0 = 22 - bulge
            x1 = 35 - int(round(0.8 * math.sin(math.pi * t)))
            m[y, x0:x1 + 1] = True
        # the foot sweeps up toward the leech
        for x in range(28, 37):
            for y in range(foot - (x - 28) // 3, foot + 1):
                m[y, x] = False
    else:
        top, foot = yard + 1, yard + 20
        for y in range(top, foot + 1):
            m[y, 23:35] = True
        for x in range(23, 35):
            drop = 1 if (x % 4) in (1, 2) else 0
            if drop:
                m[foot + 1, x] = True
            if x % 4 == 3:
                m[foot, x] = False
    p.fill(m, "l")
    yy, xx = np.mgrid[0:N, 0:N]
    if full:
        lit = (xx < 30) & (yy > top + 1)
    else:
        lit = (xx % 4) < 2
    p.fill(m & lit, "L")
    # brails and bands
    for x in (26, 31) if full else (25, 29, 33):
        for y in np.where(m[:, x])[0]:
            if full:
                p.px(x, y, "l")
            elif y > top + 2:
                p.px(x, y, "k" if y > top + 5 else "l")
    if full:
        for y in (top + 8, top + 16):
            for x in np.where(m[y])[0]:
                if p.get(x, y) == p.idx("L"):
                    p.px(x, y, "l")
        p.patch(25, top + 6, STAR_SIDE)
    else:
        p.patch(28, top + 8, ["r", "R", "r"])
    p.outline(m)
    # the yard, braced: its forward end a little lower
    for x in range(19, 39):
        y = yard - (1 if x > 30 else 0)
        p.px(x, y, "W")
        p.px(x, y - 1, "k")
        if x % 2:
            p.px(x, y, "e")
    p.px(18, yard, "k")
    p.px(39, yard - 1, "k")
    # the sheet from the clew down to the stern
    if full:
        p.line([(36, top + 22), (47, 36)], "k")


def frame_side(full, pose):
    p = Pic()
    draw_hull_side(p, pose)
    hull = p.a != 0
    far = Pic()
    draw_oars_side(far, pose, near_side=False)
    keep = ~hull & (far.a != 0)
    p.a[keep] = far.a[keep]
    # steering oar from the stern quarter, blade in the water
    p.line([(52, 44), (57, 56)], "w")
    p.patch(56, 55, ["kek", "kek", ".k."])
    draw_wake_side(p, pose)
    near = Pic()
    draw_oars_side(near, pose, near_side=True)
    body = np.zeros((N, N), bool)
    prof = side_profile()
    for x, (f, n, k) in prof.items():
        body[n + 2:k + 1, x] = True
    keep = (near.a != 0) & (~hull | body)
    p.a[keep] = near.a[keep]
    draw_mast_side(p, 40, 4)
    draw_sail_side(p, full)
    return p.a


# ==========================================================================
# Sheets
# ==========================================================================

def sheet(full):
    frames = [
        frame_vertical(full, "south", POSE_STAND),
        frame_vertical(full, "north", POSE_STAND),
        frame_side(full, POSE_STAND),
        frame_vertical(full, "south", POSE_A),
        frame_vertical(full, "south", POSE_B),
        frame_vertical(full, "north", POSE_A),
        frame_vertical(full, "north", POSE_B),
        frame_side(full, POSE_A),
        frame_side(full, POSE_B),
    ]
    return np.hstack(frames)


SHEETS = {"pg_euploia": True, "pg_euploia_slack": False}


def preview(out_dir, sea=None):
    """Both sheets at 3x over a sea background, with the east frames
    (west flipped) appended so all four headings show."""
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for name, full in SHEETS.items():
        a = sheet(full)
        fr = [a[:, i * N:(i + 1) * N] for i in range(9)]
        east = [fr[2][:, ::-1], fr[7][:, ::-1], fr[8][:, ::-1]]
        rows.append(np.hstack(fr + east))
    big = np.vstack(rows)
    rgba = to_rgba(big, PAL)
    if sea is not None:
        bg = Image.open(sea).convert("RGBA")
        tiled = Image.new("RGBA", rgba.size)
        for y in range(0, rgba.size[1], bg.size[1]):
            for x in range(0, rgba.size[0], bg.size[0]):
                tiled.paste(bg, (x, y))
        tiled.alpha_composite(rgba)
        rgba = tiled
    else:
        bg = Image.new("RGBA", rgba.size, (48, 104, 176, 255))
        bg.alpha_composite(rgba)
        rgba = bg
    upscale(rgba, 3).save(os.path.join(out_dir, "euploia_frames.png"))


def main(argv):
    if "--write" in argv:
        os.makedirs(OUT_DIR, exist_ok=True)
        for name, full in SHEETS.items():
            save_indexed(sheet(full), PAL, os.path.join(OUT_DIR, name + ".png"))
        PAL.write_jasc(PAL_PATH)
        print("wrote", ", ".join(SHEETS), "and", os.path.relpath(PAL_PATH, ROOT))
    if "--preview" in argv:
        d = argv[argv.index("--preview") + 1]
        sea = argv[argv.index("--sea") + 1] if "--sea" in argv else None
        preview(d, sea)
        print("preview in", d)


if __name__ == "__main__":
    main(sys.argv[1:])
