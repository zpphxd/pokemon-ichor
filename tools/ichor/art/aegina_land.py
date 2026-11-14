"""The island's landmarks and growth for gTileset_Aegina: Kolona's column and the
ruin of its temple, pistachio trees, Aleppo pines, scrub, and the detour's
monuments: the Temple of Aphaia's Doric front and Zeus's altar on Mount Oros.

Kolona and the altar are cool grey marble, so they stand out against the tawny
hills; Aphaia's temple is golden poros with its pediment painted blue and red, as
the real one was.
"""
from __future__ import annotations

import math
import random

from aegina_ground import straw
from aegina_lib import Layer, Struct, ground, outline_mask
from kalliste_parts import doric_column

SEC = "aegina"
MARBLE = ["m5", "m4", "m2", "m1", "w0"]        # dark -> lit, light from the left
POROS = ["po0", "po1", "po2", "po3", "po4"]


def dry_shadow(B, cx, cy, rx, ry):
    """A soft shadow on the straw (bottom layer, in the dry group)."""
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and B.get(x, y) in ("dg2", "dg3"):
                B.px(x, y, "dg1")


# --------------------------------------------------------------------------
# Kolona
# --------------------------------------------------------------------------

def kolona():
    """The single standing column of the old temple on the headland: Aegina's
    landmark, seen from the sea. A tall weathered Doric column in grey marble
    with its capital still on, standing on two worn blocks of the stylobate."""
    s = Struct("kolona", "Kolona: the standing column", 3, 5, SEC,
               walk=["-T-", "-T-", "-T-", "-T-", ".X."],
               notes="The last standing column of an old temple, on dry grass: its capital "
                     "and shaft (rows 0-3, middle column) are drawn over the player, so they "
                     "can walk behind it; its foot (row 4, middle) is solid. Row 4's outer "
                     "cells are two worn stylobate blocks, walkable: hide the Stardust on one. "
                     "Put dry grass (dry_grass's fill) in the '-' cells.")
    s.skip = {(0, y) for y in range(4)} | {(2, y) for y in range(4)}
    B, T, M = s.B, s.T, s.M
    straw(B, 16, 0, 16, 64, 0)
    straw(B, 0, 64, 48, 16, 1)
    col = Layer(48, 80)
    # the shaft, tapering a little toward the top, with entasis
    top, foot = 6, 74
    for y in range(top, foot + 1):
        t = (y - top) / (foot - top)
        w = int(round(10 + 2 * t + 0.6 * math.sin(t * math.pi)))
        x0 = 24 - w // 2
        doric_column(col, x0, y, w, 1, MARBLE, "ink", capital=False, base_line=False)
    # the capital: echinus and abacus, one corner of the abacus broken away
    col.rect(17, 0, 14, 3, "m1")
    col.hline(17, 30, 0, "ink")
    col.hline(17, 30, 2, "m4")
    col.vline(17, 0, 2, "ink")
    col.vline(30, 0, 2, "ink")
    col.hline(18, 29, 1, "w0")
    col.rect(18, 3, 12, 2, "m2")
    col.hline(18, 29, 3, "m1")
    col.vline(18, 3, 4, "ink")
    col.vline(29, 3, 4, "ink")
    col.px(28, 4, "m4")
    col.hline(19, 28, 5, "m4")
    for (x, y) in ((28, 0), (29, 0), (30, 0), (29, 1), (30, 1), (30, 2)):
        col.px(x, y, None)
    col.px(28, 1, "ink")
    col.px(29, 2, "ink")
    col.px(27, 0, "ink")
    # weathering: a crack, chipped flutes, dark streaks from the rain
    col.line(26, 22, 24, 30, "m4")
    col.line(24, 30, 25, 34, "m4")
    for (x, y) in ((22, 14), (27, 41), (21, 52), (26, 60), (23, 66)):
        col.px(x, y, "m4")
        col.px(x, y + 1, "m5")
    for y in range(8, 70, 9):
        col.px(27, y, "m5")
    # drum joints: faint lines every 14 px
    for y in range(18, 74, 14):
        for x in range(17, 32):
            if col.get(x, y) in ("m2", "m1", "w0"):
                col.px(x, y, "m4" if x > 24 else "m2")
    # rows 0-3 on the top layer (over the player), the foot on the middle layer
    for y in range(80):
        for x in range(48):
            c = col.get(x, y)
            if c:
                (T if y < 64 else M).px(x, y, c)
    # the stylobate: two worn blocks either side of the foot, and the step
    for bx in (0, 32):
        M.rect(bx + 1, 66, 14, 9, "m2")
        M.hline(bx + 1, bx + 14, 66, "w0")
        M.hline(bx + 1, bx + 14, 67, "m1")
        M.rect(bx + 1, 72, 14, 3, "m4")
        M.hline(bx + 1, bx + 14, 75, "ink")
        M.vline(bx, 66, 75, "ink")
        M.vline(bx + 15, 66, 75, "ink")
    M.px(3, 66, None)
    M.px(2, 66, None)
    M.px(1, 66, None)
    M.px(1, 67, "ink")
    M.px(2, 67, "ink")
    for (x, y) in ((6, 69), (11, 70)):
        M.px(x, y, "m3")
    M.a[64:80, 32:48] = M.a[64:80, 0:16][:, ::-1]   # the right block mirrors the left
    # the middle cell's block under the foot
    M.rect(16, 70, 16, 5, "m2")
    M.hline(16, 31, 70, "m1")
    M.hline(16, 31, 75, "ink")
    for y in range(66, 75):
        for x in range(16, 32):
            if col.get(x, y) is None and M.get(x, y) is None and y >= 70:
                M.px(x, y, "m3")
    # the column's long shadow falls east across the right-hand block
    dry_shadow(B, 40, 78, 7, 1.5)
    # the middle cell's bottom must be solid under the column's foot
    return s


def ruins():
    """A piece of Kolona's fallen temple: a column drum lying in the grass. On dry
    grass; solid."""
    s = Struct("kolona_ruins", "Fallen column drum", 2, 1, SEC, walk=["XX"],
               notes="Kolona's temple, fallen: a fluted column drum on its side, grey marble "
                     "on dry grass. Solid. Lay it near the column.")
    B, M = s.B, s.M
    straw(B, 0, 0, 32, 16, 0)
    dry_shadow(B, 17, 13, 13, 2)
    # the drum: a fluted cylinder seen from the side, its end face to the left
    for x in range(6, 29):
        for y in range(4, 13):
            c = "m2"
            if y == 4:
                c = "ink"
            elif y == 5:
                c = "w0"
            elif y == 6:
                c = "m1"
            elif y >= 11:
                c = "m4"
            elif y == 12:
                c = "ink"
            if 7 <= y <= 10 and x % 3 == 0:
                c = "m3"
            M.px(x, y, c)
        M.px(x, 13, "ink")
    M.ellipse(2, 4, 10, 13, "ink")
    M.ellipse(3, 5, 9, 12, "m1")
    M.ellipse(5, 7, 7, 10, "m2")
    M.px(5, 6, "w0")
    M.line(14, 6, 18, 11, "m4")
    M.vline(29, 5, 12, "ink")
    return s


# --------------------------------------------------------------------------
# Trees and scrub
# --------------------------------------------------------------------------

def blob_canopy(M, blobs, rng, base="ov2", hi="ov3", lo="ov1", edge="ov0", hi2=None):
    for (cx, cy, r) in blobs:
        M.ellipse(cx - r, cy - r, cx + r, cy + r, lo)
    for (cx, cy, r) in blobs:
        M.ellipse(cx - r + 1, cy - r + 1, cx + r - 2, cy + r - 2, base)
        M.ellipse(cx - r + 2, cy - r + 1, cx - 1, cy - 1, hi)
        if hi2:
            M.ellipse(cx - r + 3, cy - r + 2, cx - r + 4, cy - r + 3, hi2)
    for _ in range(60):
        x, y = rng.randrange(0, M.w), rng.randrange(0, M.h)
        if M.get(x, y) == base:
            M.px(x, y, rng.choice((lo, hi, lo)))
    outline_mask(M, (base, hi, lo, hi2), edge)


def pistachio():
    """A pistachio: low and spreading, several grey stems, a round crown of
    yellow-green leaves hung with clusters of rose-red nuts. On aethos grass."""
    s = Struct("pistachio", "Pistachio tree", 2, 2, SEC, walk=["XX", "XX"],
               notes="Aegina's pistachio, on aethos grass: a low, spreading tree with a round "
                     "pale-green crown hung with rose-red clusters of nuts, on several grey "
                     "stems. Solid. Plant them in loose rows for an orchard.")
    ground(s, "grass")
    M = s.M
    rng = random.Random(21)
    M.ellipse(4, 23, 30, 31, "gr1")              # shadow
    # stems from one root, splaying
    for (x0, x1) in ((15, 9), (16, 16), (17, 24)):
        M.line(x0, 29, x1, 16, "tk1")
        M.line(x0 + 1, 29, x1 + 1, 16, "tk0")
    M.line(14, 29, 8, 17, "tk2")
    M.hline(12, 20, 29, "tk0")
    M.hline(13, 19, 30, "ink")
    blob_canopy(M, [(8, 10, 7), (16, 7, 7), (24, 10, 7), (12, 15, 6), (21, 15, 6), (16, 12, 6)],
                rng, base="ov3", hi="ov4", lo="ov2", edge="ov1")
    # clusters of nuts, hanging under the leaves
    for (x, y) in ((6, 12), (12, 8), (19, 6), (25, 12), (15, 16), (22, 17), (9, 17)):
        M.blit([" p", "pP", "Pp"], {"p": "pk0", "P": "pk1"}, x, y)
    return s


def pine():
    """An Aleppo pine: a leaning red-grey trunk and an airy crown in tiers of bright
    needles, taller and lighter than aethos's umbrella pine. On aethos grass."""
    s = Struct("pine", "Aleppo pine", 2, 3, SEC, walk=["TT", "XX", "XX"],
               notes="A tall Aleppo pine on aethos grass, leaning a little east. Its top row is "
                     "drawn over the player (walk behind it); the rest is solid. Mix with "
                     "aethos's umbrella pine (0x01E) and cypress for the hills.")
    ground(s, "grass")
    T, M = s.T, s.M
    rng = random.Random(7)
    full = Layer(32, 48)
    full.ellipse(5, 41, 29, 47, "gr1")           # shadow
    # trunk: leaning, forking into two leaders
    for y in range(14, 46):
        x = 13 + (46 - y) // 6
        full.px(x, y, "tk0")
        full.px(x + 1, y, "tk1")
        full.px(x + 2, y, "tk2" if y % 5 else "tk1")
        full.px(x + 3, y, "tk0")
    full.line(16, 22, 9, 14, "tk1")
    full.line(17, 22, 10, 14, "tk0")
    full.line(17, 18, 23, 9, "tk1")
    full.line(18, 18, 24, 9, "tk0")
    full.hline(12, 18, 46, "ink")
    full.line(18, 30, 8, 23, "tk1")               # a low branch to the west
    full.line(19, 34, 25, 28, "tk1")              # and a shorter one east
    # crown: flat-bottomed tiers of needles, clumped, lit on top
    tiers = [(11, 6, 8, 4), (23, 4, 7, 4), (17, 11, 9, 4), (7, 15, 6, 3), (25, 15, 6, 3),
             (16, 2, 6, 3), (7, 23, 5, 3), (26, 27, 4, 2)]
    for (cx, cy, rx, ry) in tiers:
        full.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, "ov1")
    for (cx, cy, rx, ry) in tiers:
        full.ellipse(cx - rx + 1, cy - ry, cx + rx - 1, cy + ry - 2, "ov2")
        full.ellipse(cx - rx + 2, cy - ry, cx + rx - 3, cy - ry + 1, "ov3")
    for _ in range(70):
        x, y = rng.randrange(0, 32), rng.randrange(0, 22)
        if full.get(x, y) == "ov2":
            full.px(x, y, rng.choice(("ov1", "ov3", "ov1", "ov0")))
    outline_mask(full, ("ov1", "ov2", "ov3"), "ov0")
    for y in range(48):
        for x in range(32):
            c = full.get(x, y)
            if c:
                (T if y < 16 else M).px(x, y, c)
    return s


def scrub():
    """Phrygana: thorny cushions of spiny burnet and a tuft of thyme, on dry grass."""
    s = Struct("scrub", "Dry scrub: thorn cushions and thyme", 2, 1, SEC, walk=["XX"],
               notes="Low thorny scrub on dry grass: two grey-green cushions of spiny burnet "
                     "and a purple-flowered tuft of thyme. Solid. For the dry hills, the town's "
                     "edges and the detour's forced bands.")
    B, M = s.B, s.M
    straw(B, 0, 0, 32, 16, 0)
    for x in range(32):
        for y in range(16):
            if B.get(x, y) in ("dg1", "dg3"):
                B.px(x, y, "dg2")
    rng = random.Random(33)
    for (cx, rx, ry, top) in ((8, 7, 5, 4),):
        dry_shadow(B, cx + 2, top + ry * 2 + 1, rx, 2)
        M.ellipse(cx - rx, top, cx + rx, top + ry * 2, "ov1")
        M.ellipse(cx - rx + 1, top, cx + rx - 2, top + ry * 2 - 2, "ov2")
        M.ellipse(cx - rx + 2, top, cx, top + ry - 1, "ov3")
        for _ in range(18):                      # thorny texture
            x, y = cx + rng.randint(-rx + 1, rx - 1), top + rng.randint(1, ry * 2 - 1)
            if M.get(x, y) in ("ov2", "ov3"):
                M.px(x, y, rng.choice(("ov1", "tk1", "ov4")))
        outline_mask(M, ("ov1", "ov2", "ov3", "tk1", "ov4"), "ov0")
    # the second cushion is the first one mirrored (shared tiles), in flower: thyme
    # (rose is the nearest hue the grove holds)
    M.a[:, 16:32] = M.a[:, 0:16][:, ::-1]
    B.a[:, 16:32] = B.a[:, 0:16][:, ::-1]
    for (x, y) in ((20, 6), (25, 5), (27, 9), (22, 10)):
        M.px(x, y, "pk1")
    return s


# --------------------------------------------------------------------------
# The detour's monuments
# --------------------------------------------------------------------------

def aphaia_temple():
    """The Temple of Aphaia: a hexastyle Doric front in golden poros, its pediment
    painted blue with the heroes of Troy round Athena, a red-and-blue frieze, six
    columns before a dark doorway (the one who isn't seen), and three steps."""
    W, Hh = 6, 5
    s = Struct("temple_aphaia", "Temple of Aphaia, Doric front", W, Hh, SEC,
               walk=["XXXXXX", "XXXXXX", "XXXXXX", "XXXXXX", "......"],
               notes="Aphaia's temple on its pine-crowned hill: six Doric columns in golden "
                     "poros under a terracotta roof, the pediment painted blue with Athena "
                     "among the heroes of Troy, triglyphs in blue and metopes picked out in "
                     "red, and a dark, empty doorway. Row 4 is the steps, walkable. No door: "
                     "the priestess stands on the steps. Frame it with pines.")
    B = s.B
    w, h = W * 16, Hh * 16
    cx = w / 2 - 0.5
    # --- the roof seen from above: terracotta falling away from the ridge to the
    # raking cornice, cover tiles in ridges, courses every 5 px
    apex, corn = 7, 21                            # the pediment's apex and its floor

    def rake(x):
        return int(round(apex + (corn - apex) * abs(x - cx) / cx))
    for x in range(w):
        for y in range(0, rake(x)):
            c = "tc1"
            m = x % 4
            if m == 0:
                c = "po3" if x < cx else "po2"     # cover tiles catch the sun
            elif m == 1:
                c = "rd"
            if y % 4 == 3:
                c = "rd"
            B.px(x, y, c)
    B.hline(0, w - 1, 0, "ink")
    B.vline(int(cx), 0, apex - 1, "po4")          # the ridge
    B.vline(int(cx) + 1, 0, apex - 1, "po1")
    # --- the pediment: raking cornice, blue tympanum
    for x in range(w):
        t = rake(x)
        B.px(x, t - 1, "ink")
        B.px(x, t, "po4")
        B.px(x, t + 1, "po2")
        for y in range(t + 2, corn + 2):
            B.px(x, y, "b1")
    # acroteria: a palmette at the apex, griffins' wings at the corners
    B.blit(["  k  ", " kpk ", "kpppk", " kpk "], {"k": "ink", "p": "po4"}, int(cx) - 2, 1)
    for x0 in (1, w - 5):
        B.blit([" kk ", "kppk", "kpk "], {"k": "ink", "p": "po4"}, x0, corn - 4)
    # figures in the tympanum, light poros on the blue: Athena in the middle with
    # spear and shield, warriors lunging out to either side, archers kneeling, and
    # the fallen in the angles
    floor = corn + 1
    B.blit(["  k  k", " kpk k", "  p  k", " pppkk", "kppp k", "kppp k", " ppp k", " p p k",
            " p p k", " p p k"], {"k": "po4", "p": "po3"}, int(cx) - 2, floor - 9)
    figs = ((9, ["  kk ", " kpk ", "kppp ", " pp p", " p  p", "p   p"]),
            (17, [" kk  ", "kpkpk", " ppp ", "pp  p", "p   p"]),
            (26, ["  kk", " kpp", "ppp ", "pp p"]),
            (35, ["kkpp", "pppp"]))
    for side in (-1, 1):
        for dx, fig in figs:
            rows = fig if side > 0 else [r[::-1] for r in fig]
            x0 = int(cx) + side * dx - (len(rows[0]) // 2)
            B.blit(rows, {"k": "po4", "p": "po3"}, x0, floor - len(rows) + 1)
    # The roof and pediment are mirrored about the middle, Athena's cell aside, so
    # the right half's tiles are the left half's flipped (Porytiles stores them once).
    B.a[:corn + 2, 56:96] = B.a[:corn + 2, 0:40][:, ::-1]
    # --- the cornice, the triglyph frieze, the architrave
    ey = corn + 2
    B.hline(0, w - 1, ey, "po4")
    B.hline(0, w - 1, ey + 1, "po2")
    B.hline(0, w - 1, ey + 2, "ink")
    for x in range(w):                            # the frieze
        m = (x + 4) % 8
        c = ("b0" if m != 1 else "b1") if m < 3 else "po3"
        for y in range(ey + 3, ey + 8):
            B.px(x, y, c)
        if 4 <= m <= 6:
            B.px(x, ey + 5, "rd")                  # painted metopes
    B.hline(0, w - 1, ey + 8, "rd")
    B.rect(0, ey + 9, w, 3, "po3")
    B.hline(0, w - 1, ey + 9, "po4")
    B.hline(0, w - 1, ey + 11, "po1")
    # --- the colonnade before the dark cella
    cy0 = ey + 12
    steps_y = 64
    B.rect(0, cy0, w, steps_y - cy0, "dk")
    B.hline(0, w - 1, cy0, "sk")
    B.hline(0, w - 1, cy0 + 1, "sk")
    # the doorway: darker still, framed in poros, nobody in it
    dx0 = int(cx) - 6
    B.rect(dx0, cy0 + 6, 14, steps_y - cy0 - 6, "ink")
    B.vline(dx0 - 1, cy0 + 5, steps_y - 1, "po2")
    B.vline(dx0 + 14, cy0 + 5, steps_y - 1, "po1")
    B.hline(dx0 - 1, dx0 + 14, cy0 + 5, "po3")
    # one column to a cell, each at the same place in its cell, so all six share
    # their tiles
    for i in range(6):
        doric_column(B, 16 * i + 3, cy0, 10, steps_y - cy0, POROS, "ink")
    # --- three steps
    yy = steps_y
    for k, (tr, ri) in enumerate((("po4", "po2"), ("po3", "po1"), ("po3", "po1"))):
        B.rect(0, yy, w, 2, tr)
        B.rect(0, yy + 2, w, 3, ri)
        B.hline(0, w - 1, yy + 4, "po0")
        yy += 5
    B.rect(0, yy, w, h - yy, "po0")
    B.vline(0, 0, h - 1, "ink")
    B.vline(w - 1, 0, h - 1, "ink")
    return s


def zeus_altar():
    """Zeus's altar on the summit of Mount Oros: a long marble altar heaped with
    grey ash and the last embers, a gilded thunderbolt on its face, on a broad
    stepped base. On dry grass."""
    s = Struct("altar_zeus", "Altar of Zeus on Mount Oros", 2, 2, SEC, walk=["XX", "XX"],
               notes="The summit altar: a long marble altar heaped with ash, embers still "
                     "glowing, a gilded thunderbolt on its face, on a stepped base. On dry "
                     "grass; solid. Its bg event goes on the bottom row.")
    B, M = s.B, s.M
    straw(B, 0, 0, 32, 32, 1)
    dry_shadow(B, 19, 29, 14, 2.5)
    # stepped base
    M.rect(1, 24, 30, 5, "m2")
    M.hline(1, 30, 24, "w0")
    M.hline(1, 30, 28, "m4")
    M.hline(1, 30, 29, "ink")
    M.vline(0, 24, 29, "ink")
    M.vline(31, 24, 29, "ink")
    # the altar block
    M.rect(4, 9, 24, 15, "m2")
    M.vline(5, 10, 23, "m1")
    M.vline(26, 10, 23, "m4")
    M.hline(4, 27, 9, "m1")
    M.rect(3, 6, 26, 4, "m1")                     # its crowning moulding
    M.hline(3, 28, 6, "w0")
    M.hline(3, 28, 9, "m3")
    for (x0, y0, x1, y1) in ((3, 5, 28, 5), (2, 6, 2, 9), (29, 6, 29, 9), (3, 23, 28, 23)):
        M.line(x0, y0, x1, y1, "ink")
    M.vline(3, 10, 23, "ink")
    M.vline(28, 10, 23, "ink")
    # the altar is symmetric: mirror its left half (shared tiles), then the ash,
    # the embers and the bolt go on top
    M.a[:, 16:32] = M.a[:, 0:16][:, ::-1]
    # ash heaped on top, embers in it
    for x in range(5, 27):
        hgt = int(round(3.5 * math.sin(math.pi * (x - 5) / 22)))
        for y in range(5 - hgt, 6):
            M.px(x, y, "m4" if y > 5 - hgt else "m3")
        M.px(x, 5 - hgt - 1, "m5")
    for (x, y, c) in ((11, 3, "fl"), (12, 3, "fc"), (17, 2, "fl"), (18, 3, "fl"), (21, 4, "fc"),
                      (14, 4, "fl")):
        M.px(x, y, c)
    # the thunderbolt, gilded, on the altar's face
    bolt = ["   GG", "  Gg ", " GG  ", "GGGGG", "  gG ", " gG  ", "gG   "]
    M.blit(bolt, {"G": "g1", "g": "g0"}, 13, 12)
    M.blit(["k", "k"], {"k": "br"}, 12, 18)
    # garlands of laurel in relief either side
    for x0 in (7, 21):
        for (dx, dy) in ((0, 0), (1, 1), (2, 2), (3, 2), (4, 1), (5, 0)):
            M.px(x0 + dx, 13 + dy, "m4")
    return s


def build():
    return [kolona(), ruins(), pistachio(), pine(), scrub(), aphaia_temple(), zeus_altar()]
