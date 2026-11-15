"""Kemet's monuments: the White Walls of Memphis and their gate, the pylon of the
precinct of Proteus, obelisks, the alabaster sphinx, Thoth's ibis pillar (the
Egyptian herm), painted steles (signs), Naukratis's Hellenion (a Greek temple,
altar and votive kouros in an Egyptian town), and pyramids for the desert edge.
"""
from __future__ import annotations

import math

import numpy as np

import kemet_lib as L
from kemet_lib import Layer, Struct, finish, mirror_half


def outline(cnv, region=None, below=None):
    a = cnv.a[..., 3] > 0
    pad = np.pad(a, 1)
    ring = ~a & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(ring)):
        if below is None or y < below:
            cnv.px(x, y, "ink")


def split(s, cnv, top_rows=(), layer_mid=None):
    """Copy a canvas into the struct: rows in top_rows go on the top layer, the rest
    on the middle layer (or `layer_mid`)."""
    mid = layer_mid or s.M
    for y in range(cnv.h):
        for x in range(cnv.w):
            if cnv.a[y, x, 3]:
                (s.T if y // 16 in top_rows else mid).a[y, x] = cnv.a[y, x]


def limestone(Ly, x0, y0, w, h, ox=0, oy=0, lit="ls4", body="ls3", joint="ls2", course=8):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x - ox, y - oy
            row = Y // course
            bx, by = (X + (8 if row % 2 else 0)) % 16, Y % course
            c = body
            if by == course - 1 or bx == 15:
                c = joint
            elif by == 0:
                c = lit
            Ly.px(x, y, c)


# --------------------------------------------------------------------------
# The White Walls
# --------------------------------------------------------------------------

def walls():
    """Memphis's White Walls. A wall is a line of tops (one cell thick) with a face
    in the cell south of every top whose own south is not wall. Tops come in all 16
    joins (which of n, s, w, e continue the wall); faces by whether the face runs on
    west and east."""
    joins = [(n, s_, w, e) for n in (0, 1) for s_ in (0, 1) for w in (0, 1) for e in (0, 1)]
    s = Struct("wall", "The White Walls", 8, 3, walk=["X" * 8] * 3, ground="none",
               notes="Memphis's whitewashed limestone walls. Tops: part `top_NSWE` with a 1 "
                     "for each side the wall continues (top_0011 runs west-east). Faces go "
                     "south of a top with no wall below: face_WE (face_11 runs on both "
                     "sides). Solid.")
    B = s.B
    for i, (n, s_, w, e) in enumerate(joins):
        cx, cy = i % 8, i // 8
        ox, oy = cx * 16, cy * 16
        # the wall's top: pale coping blocks, rounded merlons along the edges that end
        for y in range(16):
            for x in range(16):
                bx, by = x % 8, y % 8
                B.px(ox + x, oy + y, "ls3" if (bx == 7 or by == 7) else "w0" if by == 0 else "ls4")
        if not n:
            B.hline(ox, ox + 15, oy, "ink")
            B.hline(ox, ox + 15, oy + 1, "w0")
        if not w:
            B.vline(ox, oy, oy + 15, "ink")
            B.vline(ox + 1, oy, oy + 15, "w0")
        if not e:
            B.vline(ox + 15, oy, oy + 15, "ink")
            B.vline(ox + 14, oy, oy + 15, "ls2")
        if not s_:
            B.hline(ox, ox + 15, oy + 15, "ls2")
        s.names["top_%d%d%d%d" % (n, s_, w, e)] = (cx, cy)
    for j, (w, e) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
        cx, cy = j, 2
        ox, oy = cx * 16, cy * 16
        # the face: whitewash over limestone courses, a dark plinth at the foot
        for y in range(16):
            for x in range(16):
                X, Y = x, y
                row = Y // 5
                bx = (X + (8 if row % 2 else 0)) % 16
                c = "ls3"
                if Y % 5 == 4 or bx == 15:
                    c = "ls2"
                elif Y % 5 == 0:
                    c = "w0" if row == 0 else "ls4"
                B.px(ox + x, oy + y, c)
        B.hline(ox, ox + 15, oy, "ls4")
        for x in range(16):
            B.px(ox + x, oy + 13, "ls1")
            B.px(ox + x, oy + 14, "ls0" if x % 2 else "ls1")
            B.px(ox + x, oy + 15, "ink")
        if not w:
            B.vline(ox, oy, oy + 15, "ink")
            B.vline(ox + 1, oy, oy + 14, "w0")
        if not e:
            B.vline(ox + 15, oy, oy + 15, "ink")
            B.vline(ox + 14, oy, oy + 14, "ls1")
        s.names["face_%d%d" % (w, e)] = (cx, cy)
    # a face with a painted lotus band (for the gate's flanks), and a weep-hole drain
    ox, oy = 4 * 16, 32
    B.a[oy:oy + 16, ox:ox + 16] = B.a[oy:oy + 16, 3 * 16:3 * 16 + 16]
    for x in range(16):
        B.px(ox + x, oy + 5, "ls1")
        B.px(ox + x, oy + 6, "ls2" if x % 4 else "ls1")
    s.names["face_band"] = (4, 2)
    ox = 5 * 16
    B.a[oy:oy + 16, ox:ox + 16] = B.a[oy:oy + 16, 3 * 16:3 * 16 + 16]
    B.rect(ox + 6, oy + 9, 4, 3, "ink")
    B.hline(ox + 6, ox + 9, oy + 12, "ls1")
    s.names["face_drain"] = (5, 2)
    return finish(s)


def wall_gate():
    """A gate through the White Walls: two towers with flagstaffs and a lintel the
    road passes under."""
    s = Struct("wall_gate", "Gate in the White Walls", 4, 3,
               walk=["XTTX", "XTTX", "X..X"], notes="A gate through the walls: the road "
               "runs north-south through its middle two columns, under the lintel (drawn "
               "over the player). The towers are solid. Lay wall tops and faces either side.")
    s.ground_rows(["naan", "naan", "naan"])
    cnv = Layer(64, 48)
    for tx in (0, 48):
        limestone(cnv, tx, 0, 16, 48, ox=tx, lit="w0", body="ls4", joint="ls3")
        cnv.vline(tx, 0, 47, "ink")
        cnv.vline(tx + 15, 0, 47, "ink")
        cnv.hline(tx, tx + 15, 0, "ink")
        # cavetto cornice
        cnv.hline(tx + 1, tx + 14, 1, "w0")
        cnv.hline(tx + 1, tx + 14, 3, "ls2")
        # flagstaff in its niche
        cnv.rect(tx + 6, 6, 4, 38, "ls1")
        cnv.vline(tx + 7, 2, 43, "g0")
        cnv.blit(["rr", "rrr", "rr "], {"r": "g1"}, tx + 8, 4)
        for y in range(44, 48):
            cnv.hline(tx + 1, tx + 14, y, "ls1" if y < 47 else "ink")
    # the lintel and the passage's shadow
    for y in range(0, 12):
        for x in range(16, 48):
            cnv.px(x, y, "ls4" if y > 2 else "w0")
    cnv.hline(16, 47, 0, "ink")
    cnv.hline(16, 47, 11, "ink")
    cnv.hline(16, 47, 4, "ls2")
    # a winged sun on the lintel
    cnv.blit(["gggg kk gggg", " ggggkgkgggg ", "   ggkkgg  "], {"g": "g0", "k": "g1"}, 26, 5)
    for y in range(12, 22):
        for x in range(16, 48):
            if y < 14 or x in (16, 47):
                cnv.px(x, y, "ls0")
    split(s, cnv, top_rows=(0, 1))
    # the towers' cells are drawn ground ("none"): move their art to the bottom
    for cy in range(3):
        for cx in (0, 3):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for Ly in (s.T, s.M):
                m = Ly.a[sl][..., 3] > 0
                s.B.a[sl][m] = Ly.a[sl][m]
                Ly.a[sl] = 0
    return finish(s)


# --------------------------------------------------------------------------
# The pylon of the precinct of Proteus
# --------------------------------------------------------------------------

def pylon():
    """Two battered towers with a cornice, painted reliefs and flagstaffs, the gate
    between them under a winged sun. 7x5, symmetric about its middle."""
    s = Struct("pylon", "Pylon of the precinct of Proteus", 7, 5,
               walk=["XXXXXXX"] * 4 + ["XXXDXXX"], ground="none",
               notes="The pylon gate of Pharaoh Proteus's precinct (batch 2's hall). Door at "
                     "part `door`. Symmetric: the right half is the left flipped.")
    s.set_ground("grass", [(0, 0), (6, 0)])
    cnv = Layer(112, 80)
    # the left tower: x 0..47 at the base, battered inward toward the top
    for y in range(4, 80):
        t = (y - 4) / 76
        inset = round(6 * (1 - t))
        x0, x1 = inset, 47
        for x in range(x0, x1 + 1):
            X, Y = x, y
            row = Y // 4
            bx = (X + (4 if row % 2 else 0)) % 8
            c = "ls3"
            if Y % 4 == 3 or bx == 7:
                c = "ls2"
            elif Y % 4 == 0:
                c = "ls4"
            if x == x0:
                c = "ink"
            elif x == x0 + 1:
                c = "w0"
            cnv.px(x, y, c)
    # cornice (cavetto) and torus moulding on top
    for x in range(0, 50):
        cnv.px(x, 3, "ink")
        cnv.px(x, 4, "w0")
        cnv.px(x, 5, "ls3")
        cnv.px(x, 6, "ls2")
        cnv.px(x, 7, "ls1")
        cnv.px(x, 8, "ink")
    for x in range(6, 50, 3):
        cnv.px(x, 6, "lp1")
        cnv.px(x + 1, 6, "rd1")
    # the relief panel: Pharaoh smiting, in paint
    px0, py0 = 16, 16
    for y in range(py0, py0 + 32):
        for x in range(px0, px0 + 24):
            cnv.px(x, y, "ls3")
    cnv.hline(px0, px0 + 23, py0, "ls1")
    cnv.hline(px0, px0 + 23, py0 + 31, "ls1")
    fig = [
        "        rr        ",
        "       rwwr       ",
        "       rwwr  y    ",
        "  y     ss   y    ",
        "  yy   ssss y     ",
        "   yy sswwssy     ",
        "    ysswwwws      ",
        "      swwws       ",
        "      swwws       ",
        "      wwwww       ",
        "      wwwww       ",
        "     ww   ww      ",
        "     w     w      ",
        "    ss     ss     ",
    ]
    cnv.blit(fig, {"r": "rd0", "w": "w0", "s": "skn", "y": "yo0"}, px0 - 2, py0 + 4)
    # a kneeling enemy and a column of glyphs
    cnv.blit(["  ss ", " smms", "  mm ", " mmm ", "mm mm"], {"s": "skn", "m": "mg0"}, px0 + 13, py0 + 13)
    for i, gy in enumerate(range(py0 + 3, py0 + 29, 5)):
        g = [["kk", "k "], [" k", "kk"], ["kk", "kk"], ["k ", "kk"], ["kk", " k"]][i % 5]
        cnv.blit(g, {"k": "lp0" if i % 2 else "ink"}, px0 + 20, gy)
    # flagstaffs in the niches by the gate, with red pennants
    for fx in (42,):
        cnv.rect(fx, 12, 4, 66, "ls1")
        cnv.vline(fx + 1, 0, 76, "g1")
        cnv.blit(["rrr", "rrrr", "rrr "], {"r": "rd1"}, fx + 2, 1)
    # the gateway: lintel with a winged sun, the doors in shadow
    gx0, gx1 = 48, 63
    for y in range(10, 80):
        for x in range(gx0, gx1 + 1):
            cnv.px(x, y, "ls3")
    for x in range(gx0, gx1 + 1):
        cnv.px(x, 10, "ink")
        cnv.px(x, 11, "w0")
    cnv.blit(["gggg  gggg", " ggg11ggg ", "   g11g   "], {"g": "g1", "1": "rd1"}, gx0 + 3, 14)
    for y in range(28, 80):
        for x in range(gx0 + 3, gx1 - 2):
            cnv.px(x, y, "ls0")
    cnv.vline(gx0 + 2, 28, 79, "ink")
    cnv.vline(gx1 - 2, 28, 79, "ink")
    cnv.hline(gx0 + 2, gx1 - 2, 27, "ink")
    # bronze-studded doors, closed
    for y in range(30, 78, 4):
        cnv.px(gx0 + 5, y, "g0")
        cnv.px(gx1 - 5, y, "g0")
    cnv.vline(56, 29, 79, "ink")
    # the plinth
    for x in range(0, 112):
        cnv.px(x, 78, "ls1")
        cnv.px(x, 79, "ink")
    # mirror the left half onto the right
    mirror_half(cnv, 0, 112, 0, 80)
    # sky above the battered corners is grass (the cells (0,0) and (6,0))
    # the top row: on the grass corners the art goes on the middle layer
    for y in range(80):
        for x in range(112):
            if cnv.a[y, x, 3]:
                cx = x // 16
                if y < 16 and cx in (0, 6):
                    s.M.a[y, x] = cnv.a[y, x]
                else:
                    s.B.a[y, x] = cnv.a[y, x]
    # fill the drawn cells' holes (the battered edge in row 0 is on grass, so fine)
    for cy in range(5):
        for cx in range(7):
            if (cx, cy) in s.borrowed:
                continue
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            m = s.B.a[sl][..., 3] == 0
            if m.any():
                s.B.a[sl][m] = (*L.C["ls3"], 255)
    s.names["door"] = (3, 4)
    return finish(s)


# --------------------------------------------------------------------------
# Obelisk, sphinx, ibis pillar, steles
# --------------------------------------------------------------------------

def obelisk(ground, key):
    s = Struct(key, f"Obelisk ({ground})", 1, 3, walk=["T", "T", "X"], ground=ground,
               notes="A granite-pink limestone needle with a gilt pyramidion; hieroglyphs run "
                     "down its face. The upper two rows are drawn over the player.")
    cnv = Layer(16, 48)
    cnv.blit(["   k   ", "  kgk  ", " kgg1k ", "kgg111k"], {"k": "ink", "g": "g1", "1": "g0"}, 4, 0)
    for y in range(4, 42):
        t = (y - 4) / 38
        half = 3 + round(t * 1.2)
        for x in range(8 - half, 8 + half):
            c = "ls4" if x < 8 - half + 2 else "ls3" if x < 8 + half - 2 else "ls2"
            if x == 8 - half or x == 8 + half - 1:
                c = "ink"
            cnv.px(x, y, c)
    for i, y in enumerate(range(7, 39, 5)):
        g = [["kk", "k."], [".k", "kk"], ["kk", "kk"], ["k.", "kk"], ["kk", ".k"], ["k.", ".k"]][i % 6]
        cnv.blit(g, {"k": "ls1"}, 7, y)
    for y in range(42, 47):
        cnv.hline(3, 12, y, "ls3" if y < 46 else "ls1")
    cnv.hline(3, 12, 41, "ink")
    cnv.vline(2, 41, 46, "ink")
    cnv.vline(13, 41, 46, "ink")
    cnv.hline(2, 13, 47, "ink")
    split(s, cnv, top_rows=(0, 1))
    return finish(s)


def sphinx():
    s = Struct("sphinx", "The alabaster sphinx of Memphis", 3, 2, walk=["XXX", "XXX"],
               notes="A recumbent lion with Pharaoh's face and the striped nemes, facing west, "
                     "on its plinth.")
    s.ground_rows(["ggg", "nnn"])
    cnv = Layer(48, 32)
    # plinth
    for y in range(22, 32):
        for x in range(1, 47):
            cnv.px(x, y, "ls3" if y < 30 else "ls1")
    cnv.hline(1, 46, 22, "w0")
    cnv.hline(0, 47, 21, "ink")
    cnv.vline(0, 21, 31, "ink")
    cnv.vline(47, 21, 31, "ink")
    for x in range(4, 44, 8):
        cnv.vline(x, 24, 29, "ls2")
    # body: haunch at the right, forepaws out to the left
    body = [
        "                   aaaaaaaaaaaa     ",
        "                 aawwwwwwwwwwwwaa   ",
        "               aawwwwwwwwwwwwwwwwa  ",
        "              awwwwwwwwwwwwwwwwwwwa ",
        "             awwwwwwwwwwwwwwwwwwwwwa",
        "            awwwwwwwwwwwwwwwwwwwwwwa",
        "aaaaaaaaaaaawwwwwwwwwwwwwwwwwwwwwwwa",
        "awwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwaa",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  ",
    ]
    cnv.blit(body, {"a": "ls2", "w": "ls4"}, 8, 13)
    # head with nemes, facing left
    head = [
        "    kkkkkk   ",
        "   kbybybyk  ",
        "  kbybybybyk ",
        "  kysssbybyk ",
        "  kssesbybk  ",
        "  ksssssbyk  ",
        "  kssssbybk  ",
        "  kkssbybyk  ",
        "    kbybyk   ",
        "    kbybyk   ",
    ]
    cnv.blit(head, {"k": "ink", "b": "lp0", "y": "yo1", "s": "ls3", "e": "ink"}, 8, 3)
    outline(cnv, below=21)
    for y in range(32):
        for x in range(48):
            if cnv.a[y, x, 3]:
                (s.M if y < 16 else s.B).a[y, x] = cnv.a[y, x]
    for cx in range(3):
        sl = np.s_[16:32, cx * 16:cx * 16 + 16]
        m = s.B.a[sl][..., 3] == 0
        if m.any():
            s.B.a[sl][m] = (*L.C["ls3"], 255)
    return finish(s)


def ibis_pillar(ground, key):
    s = Struct(key, f"Thoth's ibis pillar ({ground})", 1, 2, walk=["T", "X"], ground=ground,
               notes="The Egyptian herm: a painted pillar with Thoth's ibis on top, the "
                     "waystone where Greeks anoint their Hermes. The bird is drawn over the "
                     "player.")
    cnv = Layer(16, 32)
    cnv.blit([
        "    kk      ",
        "   kwwk     ",
        "   kkwwk    ",
        "  k  kwwwk  ",
        " k    kwwwwk",
        "k     kwkkwk",
        "       kk kk",
        "       k  k ",
    ], {"k": "ink", "w": "w0"}, 2, 4)
    cnv.hline(3, 12, 12, "ink")
    cnv.hline(4, 11, 13, "g1")
    cnv.hline(4, 11, 14, "yo0")
    for y in range(15, 30):
        for x in range(5, 11):
            c = "ls3" if x > 5 else "w0"
            if x == 10:
                c = "ls2"
            cnv.px(x, y, c)
        cnv.px(4, y, "ink")
        cnv.px(11, y, "ink")
    for (y, c) in ((17, "lp1"), (18, "lp1"), (22, "rd1"), (26, "mg1"), (27, "mg1")):
        cnv.hline(5, 10, y, c)
    cnv.blit(["k.", ".k"], {"k": "ink"}, 7, 20)
    cnv.blit([".k", "k."], {"k": "ink"}, 7, 24)
    cnv.hline(3, 12, 30, "ls1")
    cnv.hline(3, 12, 31, "ink")
    split(s, cnv, top_rows=(0,))
    return finish(s)


def stele(ground, key):
    s = Struct(key, f"Painted stele ({ground})", 1, 1, walk=["X"], ground=ground,
               notes="A round-topped stele with a winged sun and a few lines of hieroglyphs: "
                     "Kemet's signpost (a bg event reads it).")
    cnv = Layer(16, 16)
    cnv.blit([
        "    kkkkkk    ",
        "  kk233333kk  ",
        " k2gg2222gg3k ",
        " k2223223333k ",
        " k2kk2k2kk23k ",
        " k2222222223k ",
        " k2k2kk2k223k ",
        " k2222222223k ",
        " k2kk2k2kkk3k ",
        " k2222222223k ",
        " k1111111111k ",
        " kkkkkkkkkkkk ",
    ], {"k": "ink", "2": "w0", "3": "ls3", "1": "ls2", "g": "lp1"}, 1, 2)
    cnv.px(7, 4, "rd1")
    cnv.px(8, 4, "rd1")
    for y in range(16):
        for x in range(16):
            if cnv.a[y, x, 3]:
                s.M.a[y, x] = cnv.a[y, x]
    return finish(s)


# --------------------------------------------------------------------------
# The Hellenion
# --------------------------------------------------------------------------

def hellenion():
    """The Hellenion of Naukratis: the shrine nine Greek cities built together. An
    Ionic temple front, its pediment painted, its porch open to the god's statue."""
    s = Struct("hellenion", "The Hellenion's temple", 5, 4, walk=["XXXXX"] * 4, ground="none",
               notes="Greek gods in an Egyptian town: Ionic columns, a painted pediment, the "
                     "porch open on Apollo's bronze statue. No door (a bg event reads it). "
                     "Symmetric.")
    s.set_ground("grass", [(x, 0) for x in range(5)])
    cnv = Layer(80, 64)
    # pediment
    for y in range(2, 18):
        t = (y - 2) / 15
        half = round(4 + t * 35)
        for x in range(40 - half, 40 + half):
            cnv.px(x, y, "b1" if 2 < t * 15 else "m1")
        cnv.px(40 - half, y, "ink")
        cnv.px(40 - half + 1, y, "w0")
    for x in range(1, 79):
        cnv.px(x, 18, "ink")
        cnv.px(x, 19, "w0")
        cnv.px(x, 20, "m2")
    # akroteria and the painted gods in the gable
    cnv.blit([" g ", "ggg", " g "], {"g": "g1"}, 38, 0)
    cnv.blit([" rr  rr ", "rrrrrrrr", " r gg r "], {"r": "rd", "g": "g0"}, 30, 9)
    # entablature: architrave and a frieze of red and blue
    for y in range(21, 27):
        for x in range(2, 78):
            c = "m1" if y < 23 else ("rd" if (x // 4) % 2 else "b0") if y < 25 else "m2"
            cnv.px(x, y, c)
    cnv.hline(2, 77, 27, "ink")
    # porch: dark cella with Apollo's statue, four Ionic columns
    for y in range(28, 56):
        for x in range(4, 76):
            cnv.px(x, y, "m4" if y < 30 else "m3" if x % 8 == 0 else "m4")
    cnv.blit(["  gg  ", " gkkg ", "  gg  ", " gggg ", "g gg g", "  gg  ", " g  g ", " g  g "],
             {"g": "g0", "k": "ink"}, 37, 36)
    for cx in (12, 28, 52, 68):
        for y in range(30, 56):
            for x in range(cx - 2, cx + 3):
                c = "w0" if x == cx - 1 else "m1" if x <= cx else "m2"
                if x in (cx - 2, cx + 2):
                    c = "ink"
                cnv.px(x, y, c)
        cnv.blit(["kkkkkkkkk", "kwkmmmkwk", " kk   kk "], {"k": "ink", "w": "w0", "m": "m1"}, cx - 4, 28)
    # steps
    for i, y in enumerate(range(56, 64)):
        for x in range(0, 80):
            cnv.px(x, y, "w0" if i % 3 == 0 else "m1" if i % 3 == 1 else "m2")
    cnv.hline(0, 79, 63, "ink")
    mirror_half(cnv, 0, 80, 0, 64)
    # the gable stands on the meadow (row 0 borrows aethos's grass); below it the
    # cells are opaque
    for y in range(16, 64):
        for x in range(80):
            if not cnv.a[y, x, 3]:
                cnv.px(x, y, "m2")
    for y in range(64):
        for x in range(80):
            if cnv.a[y, x, 3]:
                (s.M if y < 16 else s.B).a[y, x] = cnv.a[y, x]
    return finish(s)


def hellenion_gable_grass():
    """The same temple, its gable on the meadow (row 0 on borrowed grass)."""
    return None


def altar():
    s = Struct("altar_greek", "Greek altar", 2, 1, walk=["XX"], ground="grass",
               notes="A marble altar with volutes, fire on it: the Hellenion's.")
    cnv = Layer(32, 16)
    cnv.rect(3, 6, 26, 9, "m1")
    cnv.hline(3, 28, 6, "w0")
    cnv.hline(3, 28, 14, "m3")
    for x in (3, 28):
        cnv.vline(x, 4, 15, "ink")
    cnv.hline(2, 29, 15, "ink")
    cnv.blit(["kk", "kw"], {"k": "ink", "w": "w0"}, 2, 4)
    cnv.blit(["kk", "wk"], {"k": "ink", "w": "w0"}, 28, 4)
    cnv.hline(4, 27, 5, "ink")
    for x in range(6, 26, 4):
        cnv.px(x, 10, "rd")
    cnv.blit(["   r    ", "  rgr r ", " rgggrgr", "rgg1ggr ", " rrrrrr "], {"r": "rd", "g": "g1", "1": "w0"}, 12, 0)
    for y in range(16):
        for x in range(32):
            if cnv.a[y, x, 3]:
                s.M.a[y, x] = cnv.a[y, x]
    return finish(s)


def kouros():
    s = Struct("kouros", "Votive kouros", 1, 2, walk=["T", "X"], ground="grass",
               notes="A marble youth, a Samian sailor's thank-offering: drawn over the player.")
    cnv = Layer(16, 32)
    cnv.blit([
        "   kkk   ",
        "  kmmmk  ",
        "  kwmmk  ",
        "   kmk   ",
        "  kwmmk  ",
        " kwwmmmk ",
        " kwkmmkmk",
        " kwkmmkmk",
        "  kwmmk  ",
        "  kwmmk  ",
        "  kw km  ",
        "  kw km  ",
        "  kw km  ",
        "  kw km  ",
        " kww kmm ",
    ], {"k": "ink", "m": "m2", "w": "w0"}, 3, 6)
    cnv.rect(2, 21, 12, 8, "m1")
    cnv.hline(2, 13, 21, "w0")
    cnv.hline(1, 14, 29, "ink")
    cnv.vline(1, 20, 29, "ink")
    cnv.vline(14, 20, 29, "ink")
    cnv.hline(1, 14, 20, "ink")
    split(s, cnv, top_rows=(0,))
    return finish(s)


# --------------------------------------------------------------------------
# Pyramids
# --------------------------------------------------------------------------

def pyramid(w, h, key, title):
    """A pyramid on the sand: lit west face, shaded east face, a gilt cap."""
    walk = ["T" * w] + ["X" * w] * (h - 1)
    s = Struct(key, title, w, h, walk=walk, ground="sand",
               notes="Cased in polished Tura limestone, capped in electrum. The top row is "
                     "drawn over the player. Stands on aethos's sand.")
    W, H = w * 16, h * 16
    cnv = Layer(W, H)
    apex = (W // 2, 2)
    base = H - 2
    for y in range(apex[1], base + 1):
        t = (y - apex[1]) / (base - apex[1])
        half = round(t * (W // 2 - 1))
        for x in range(W // 2 - half, W // 2 + half):
            west = x < W // 2
            c = ("w0" if (x % 8, y % 8) == (2, 1) else "ls4") if west else \
                ("ls1" if (x % 8, y % 8) == (5, 5) else "ls2")
            if y % 4 == 3:
                c = "ls3" if west else "ls1"
            cnv.px(x, y, c)
        cnv.px(W // 2 - half, y, "ink")
        cnv.px(W // 2 + half - 1, y, "ink")
    capr = max(3, w)
    for y in range(apex[1], apex[1] + capr):
        t = (y - apex[1]) / ((base - apex[1]) or 1)
        half = round(t * (W // 2 - 1))
        for x in range(W // 2 - half, W // 2 + half):
            cnv.px(x, y, "g1" if x < W // 2 else "g0")
    cnv.hline(0, W - 1, base + 1, "ink")
    cnv.px(W // 2 - 1, apex[1] - 1, "ink")
    cnv.px(W // 2, apex[1] - 1, "ink")
    split(s, cnv, top_rows=(0,))
    return finish(s)


def build():
    # ordered for the sheet's shelf packing: tall pieces share shelves
    return [walls(),
            pylon(), obelisk("path", "obelisk"),
            hellenion(), sphinx(),
            wall_gate(), obelisk("grass", "obelisk_grass"), obelisk("sand", "obelisk_sand"),
            ibis_pillar("grass", "ibis_pillar"), ibis_pillar("path", "ibis_pillar_path"),
            stele("grass", "stele"), stele("path", "stele_path"), stele("sand", "stele_sand"),
            stele("mud", "stele_mud"), altar(),
            pyramid(5, 4, "pyramid", "Pyramid")]
