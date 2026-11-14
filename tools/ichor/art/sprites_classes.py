"""Trainer front pics for the Phase 1 slice's trainer classes.

Shepherd, Harvester, Goatherd, Hoplite, Augur and the two Acolytes of Hestia.
Each is a 64x64, 16-color Gen 3 trainer pic in a 3/4 view facing the player's
side (screen left), lit from the top left. See design/phase1/SPRITES_classes.md.

Usage: python3 tools/ichor/art/sprites_classes.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when
          no NAME is given, the contact sheet design/phase1/img/sprites_classes.png.
--preview writes the 3x battle-background contact sheet (Brendan and the
          cast for scale), 6x singles and pixel grids to DIR.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview, bresenham)
from PIL import Image  # noqa: E402
import numpy as np  # noqa: E402

INK = (32, 24, 24)
FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")

# Shared skin ramps (light, mid, dark). Sun-browned islanders run darker.
SKIN_TAN = [("skin_l", (248, 200, 152)), ("skin_m", (216, 144, 96)), ("skin_d", (160, 96, 64))]
SKIN_SUN = [("skin_l", (232, 176, 120)), ("skin_m", (192, 120, 72)), ("skin_d", (136, 80, 48))]
SKIN_FAIR = [("skin_l", (248, 216, 184)), ("skin_m", (224, 168, 128)), ("skin_d", (176, 112, 80))]


def skin_mat(outline):
    return Mat(["skin_d", "skin_m", "skin_l"], outline=outline, cuts=[0.5, 0.86])


def texture(f, arr, pids, ramp, anchors, motif):
    """Stamps a motif (list of dx, dy) at each anchor, one ramp step darker,
    on pixels of the given parts that are still a ramp color (not outline)."""
    idx = [f.pal[n] for n in ramp]
    pm = np.isin(f.pid, list(pids))
    for ax, ay in anchors:
        for dx, dy in motif:
            x, y = ax + dx, ay + dy
            if 0 <= x < f.w and 0 <= y < f.h and pm[y, x] and arr[y, x] in idx[1:]:
                arr[y, x] = idx[idx.index(arr[y, x]) - 1]


def render(f):
    """Fig.render, with any f.textures stamped before the hand-drawn detail."""
    post, f.post = f.post, []
    arr = f.render()
    for args in getattr(f, "textures", []):
        texture(f, arr, *args)
    for op in post:
        if op[0] == "px":
            _, x, y, c = op
            arr[y, x] = 0 if c == "_" else f.pal[c]
        elif op[0] == "line":
            for (x0, y0), (x1, y1) in zip(op[1], op[1][1:]):
                for x, y in bresenham(x0, y0, x1, y1):
                    arr[y, x] = f.pal[op[2]]
        elif op[0] == "patch":
            _, x0, y0, rows, legend = op
            for j, row in enumerate(rows):
                for i, ch in enumerate(row):
                    if ch not in ". ":
                        c = legend[ch]
                        arr[y0 + j, x0 + i] = 0 if c == "_" else f.pal[c]
    f.post = post
    return arr


def pole(f, top, bottom, mat, **kw):
    """A 3 px pole (outline, wood, outline) from top to bottom, any slope."""
    (x0, y0), (x1, y1) = top, bottom
    spans = []
    for y in range(y0, y1 + 1):
        xc = int(round(x0 + (x1 - x0) * (y - y0) / max(y1 - y0, 1)))
        spans.append((xc - 1, xc + 1))
    return f.spans(y0, spans, mat, **kw)


def stagger(x0, y0, x1, y1, sx, sy):
    pts = []
    for j, y in enumerate(range(y0, y1 + 1, sy)):
        for x in range(x0 + (sx // 2 if j % 2 else 0), x1 + 1, sx):
            pts.append((x, y))
    return pts


# --------------------------------------------------------------------------
# Shepherd (male): felt pilos cap, sheepskin over a short tunic, crook
# --------------------------------------------------------------------------

def shepherd():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("lea", (96, 56, 40)),
        ("felt_l", (224, 176, 104)), ("felt_m", (176, 120, 64)), ("felt_d", (112, 72, 40)),
        ("wool_l", (248, 248, 232)), ("wool_m", (224, 216, 184)), ("wool_d", (168, 152, 120)),
        ("blue_l", (112, 168, 224)), ("blue_m", (48, 104, 176)), ("blue_d", (24, 56, 120)),
        ("hair", (64, 40, 32)),
    ])
    skin = skin_mat("lea")
    wood = Mat(["felt_d", "felt_m", "felt_l"], outline="ink", wx=1.0, wy=0.0, cuts=[0.3, 0.7])
    wool = Mat(["wool_d", "wool_m", "wool_l"], outline="felt_d", wx=0.7, wy=0.4, cuts=[0.45, 0.8])
    tunic = Mat(["blue_d", "blue_m", "blue_l"], wx=0.85, wy=0.3, cuts=[0.25, 0.7])
    lea = Mat(["lea"])
    f = Fig(pal)

    # crook shaft, planted at his right side (the hook is drawn by hand below)
    f.rect(19, 5, 21, 61, wood, group=50)
    # sheepskin hanging down his back, shaggy hem
    back = f.poly([(29, 23), (42, 22), (47, 27), (49, 34), (50, 41), (48, 44), (46, 42), (44, 45), (42, 42),
                   (40, 44), (38, 41)], wool, group=60, bias=0.25)
    f.rect(31, 20, 36, 25, skin, group=400)
    # legs: weight on the far leg, near knee relaxed
    f.poly([(27, 44), (31, 44), (31, 50), (30, 57), (27, 57), (27, 50)], skin, group=100)
    f.poly([(34, 44), (38, 44), (39, 50), (40, 57), (37, 57), (35, 50)], skin, group=101)
    f.poly([(25, 57), (31, 57), (31, 61), (24, 61)], lea)
    f.poly([(36, 57), (41, 57), (43, 61), (36, 61)], lea)
    # short tunic, belted with a cord
    body = f.poly([(27, 24), (39, 24), (41, 33), (43, 45), (35, 46), (25, 45), (26, 33)], tunic)
    f.rect(24, 34, 44, 35, lea, clip=body, noline=True)
    f.shade_poly([(33, 36), (34, 36), (36, 45), (35, 45)], 0.5)
    f.shade_poly([(29, 37), (30, 37), (29, 45), (28, 45)], 0.4)
    f.shade_poly([(38, 36), (39, 36), (41, 45), (40, 45)], 0.4)
    f.shade_poly([(26, 33), (29, 33), (28, 45), (25, 45)], -0.3)
    # sheepskin mantle over the shoulders, open at the neck, scalloped fleece hem
    mantle = f.poly([(24, 25), (28, 23), (31, 23), (32, 26), (35, 26), (36, 23), (39, 23), (43, 25), (46, 28),
                     (45, 31), (43, 30), (41, 32), (39, 30), (37, 32), (35, 30), (33, 32), (31, 30), (29, 32),
                     (27, 30), (24, 30)], wool, group=70)
    # near arm (his right) gripping the crook
    f.thick_line([(25, 27), (22, 31), (21, 33)], 4, skin, group=200)
    # far arm raised in a wave
    f.thick_line([(43, 27), (47, 23), (48, 17)], 4, skin, group=300)

    # fleece curls
    f.textures = [((back, mantle), ["wool_d", "wool_m", "wool_l"], stagger(23, 24, 50, 44, 5, 4),
                   [(0, 0), (1, 1), (2, 0)])]
    # fist around the crook
    f.patch(17, 31, [
        ".bbbb.",
        "bLLLMb",
        "bLbLMb",
        "bLLMMb",
        ".bbbb.",
    ], {"b": "lea", "L": "skin_l", "M": "skin_m"})
    # sandal straps and knees
    f.line([(27, 54), (30, 54)], "lea")
    f.line([(37, 54), (39, 54)], "lea")
    f.line([(27, 51), (30, 52)], "lea")
    f.line([(36, 51), (39, 52)], "lea")
    f.pxs([(28, 48), (36, 48)], "skin_m")
    # knot of the sheepskin's forelegs at his chest
    f.patch(31, 27, [
        ".kkk.",
        "kWmWk",
        "kmWdk",
        ".kdk.",
        "..k..",
    ], {"k": "felt_d", "W": "wool_l", "m": "wool_m", "d": "wool_d"})
    # crook hook
    f.patch(11, 0, [
        "...kkkkk...",
        "..kFFFFfk..",
        ".kFkkkkkfk.",
        "kFk.....kFk",
        "kFk.....kFk",
        "kfk.....kfk",
        ".k......kfk",
    ], {"k": "ink", "F": "felt_l", "f": "felt_m"})
    # waving hand, palm out
    f.patch(45, 10, [
        ".k.k...",
        "kLkLkk.",
        "kLkLkLk",
        "kLLLLLk",
        "kLLLLMk",
        ".kLLMkb",
        "..kMMb.",
        "..bMb..",
    ], {"k": "lea", "L": "skin_l", "M": "skin_m", "b": "lea"})
    # head: felt pilos tilted back, a grin
    f.patch(25, 1, [
        "........kkkk......",
        "......kkFFffkk....",
        ".....kFFFFffffk...",
        "....kFFFFfffffdk..",
        "....kFFFfffffffdk.",
        "...kFFFffffffffdk.",
        "...kFFfffffffffddk",
        "..kFFfffffffffffdk",
        "..kFffffffffffffdk",
        "..kddddddddddddddk",
        "..kfFfffffffffdddk",
        "..kkkkkkkkkkkkkkHk",
        "..bDDDMMMMMMMDbHHk",
        "..bLHHLLLHHHLMbHHk",
        "..bLWkLLLkWLMDMbHk",
        ".bLLWkLLLkWLMDMbHk",
        ".bLLLLLLLLLMMMbHk.",
        "bLLLLDLLLLMMMMbHk.",
        ".bLLDDLLLMMMMbHk..",
        "..bLbLLLbMMMbk....",
        "..bLLbbbMMMbk.....",
        "...bbLLLMMbk......",
        ".....bbbbbk.......",
    ], {"k": "ink", "F": "felt_l", "f": "felt_m", "d": "felt_d", "H": "hair", "b": "lea",
        "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "wool_l"})
    return f, pal


# --------------------------------------------------------------------------
# Harvester (female): olive-picker, headscarf, apron, a basket of olives
# --------------------------------------------------------------------------

def harvester():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("brown", (88, 48, 32)),
        ("ter_l", (232, 120, 80)), ("ter_m", (184, 72, 48)), ("ter_d", (88, 40, 64)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 184, 152)),
        ("ol_l", (168, 184, 120)), ("ol_m", (112, 128, 56)), ("ol_d", (56, 72, 32)),
        ("wick_l", (224, 184, 104)), ("wick_d", (160, 112, 56)),
    ])
    skin = skin_mat("brown")
    dress = Mat(["ol_d", "ol_m", "ol_l"], wx=0.85, wy=0.2, cuts=[0.3, 0.75])
    apron = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.62])
    scarf = Mat(["ter_d", "ter_m", "ter_l"], cuts=[0.3, 0.7])
    wicker = Mat(["brown", "wick_d", "wick_l"], outline="brown", wx=0.7, wy=0.5, cuts=[0.45, 0.8])
    lea = Mat(["brown"])
    f = Fig(pal)

    # long olive-green dress, the hem swinging a little toward her raised arm
    body = f.poly([(26, 24), (38, 24), (41, 32), (42, 40), (44, 50), (46, 58), (20, 58), (21, 50), (23, 40),
                   (24, 32)], dress)
    for x in (27, 33, 40):
        f.shade_poly([(x, 44), (x + 1, 44), (x + 1 + (x - 33) // 4, 57), (x + (x - 33) // 4, 57)], 0.45)
    f.poly([(23, 58), (28, 58), (28, 61), (22, 61)], lea)
    f.poly([(35, 58), (40, 58), (41, 61), (35, 61)], lea)
    # linen apron tied with a terracotta sash
    f.poly([(25, 32), (37, 32), (38, 42), (39, 52), (35, 53), (27, 53), (23, 52), (24, 42)], apron)
    f.shade_poly([(30, 38), (31, 38), (31, 52), (30, 52)], 0.4)
    f.shade_poly([(35, 40), (36, 40), (37, 52), (36, 52)], 0.4)
    f.rect(22, 31, 42, 32, scarf, clip=body, noline=True)
    f.rect(29, 20, 34, 26, skin, group=400)
    # near arm (her right) raised, holding up an olive sprig
    f.thick_line([(26, 26), (21, 30)], 5, skin, group=200)
    f.thick_line([(21, 30), (18, 23)], 4, skin, group=200)
    f.poly([(24, 24), (28, 24), (28, 28), (25, 29), (23, 27)], dress, group=210)
    # far arm hanging to the basket rim
    f.thick_line([(39, 26), (41, 30), (42, 34)], 4, skin, group=300)
    # wicker basket on her left hip
    bask = f.poly([(35, 36), (55, 36), (54, 41), (52, 45), (48, 47), (42, 47), (38, 45), (36, 41)], wicker, group=500)

    # basket weave
    f.textures = [((bask,), ["brown", "wick_d", "wick_l"], stagger(36, 37, 55, 47, 4, 2), [(0, 0), (1, 0)])]
    # heap of black and green olives above the rim, two leaves poking out
    heap = [list("." * 21) for _ in range(9)]
    rows = {0: (0, -1), 1: (0, -1), 2: (6, 13), 3: (4, 15), 4: (2, 17), 5: (1, 18), 6: (1, 19), 7: (0, 20)}
    for r, (a, b) in rows.items():
        for c in range(a, b + 1):
            heap[r][c] = "k"
    olives = [(7, 2, "d"), (11, 2, "g"), (4, 4, "g"), (8, 4, "d"), (12, 4, "d"), (15, 4, "g"),
              (2, 6, "d"), (6, 6, "d"), (10, 6, "g"), (14, 6, "d"), (17, 6, "d")]
    for c, r, kind in olives:
        hi, body = ("T", "d") if kind == "d" else ("G", "g")
        for dc, dr, ch in ((0, 0, hi), (1, 0, body), (2, 0, body), (0, 1, body), (1, 1, body), (2, 1, body)):
            if heap[r + dr][c + dc] == "k":
                heap[r + dr][c + dc] = ch
    for c, r in ((9, 0), (10, 1), (13, 0), (12, 1)):
        heap[r][c] = "G"
    for c, r in ((8, 0), (9, 1), (11, 1), (10, 0), (12, 0), (13, 1), (14, 0)):
        if heap[r][c] == ".":
            heap[r][c] = "k"
    heap[8] = list("bWWWWWWWWWWWWWWWWWwwb")
    f.patch(35, 27, ["".join(r) for r in heap] + ["bwwwwwwwwwwwwwwwwwwbb"],
            {"k": "ink", "d": "ter_d", "T": "lin_l", "g": "ol_m", "G": "ol_l", "b": "brown",
             "W": "wick_l", "w": "wick_d"})
    # hand over the rim
    f.patch(40, 33, [
        ".bbbb.",
        "bLLLLb",
        "bLMLMb",
        "bMMMMb",
        ".bbbb.",
    ], {"b": "brown", "L": "skin_l", "M": "skin_m"})
    # olive sprig in her raised hand: a twig, slim silver leaves, two olives
    f.patch(8, 6, [
        "..kk.........",
        ".kGGk........",
        "kGGgk...kk...",
        ".kkkbk.kGGk..",
        "....kbkGgk...",
        "..kk.kbkk....",
        ".kGGkkbk.kk..",
        "kGGgkkbkkGGk.",
        ".kkk.kbkGgk..",
        "....kTdbkk...",
        "...kTddkbk...",
        "...kdddkbk...",
        "....kkk.kbk..",
        ".........kbk.",
        ".........kbk.",
    ], {"k": "ink", "G": "ol_l", "g": "ol_m", "b": "brown", "d": "ter_d", "T": "lin_l"})
    f.patch(15, 19, [
        ".bbbb.",
        "bLLLLb",
        "bLbLMb",
        "bLLMMb",
        ".bbbb.",
    ], {"b": "brown", "L": "skin_l", "M": "skin_m"})
    # head: terracotta headscarf knotted at the nape, a few loose strands
    f.patch(24, 5, [
        ".....kkkkkkk.......",
        "...kkTTTTTttkk.....",
        "..kTTTTTTtttttk....",
        ".kTTTTTTtttttttk...",
        ".kTTTTTttttttttdk..",
        "kTTTTTtttttttttddk.",
        "kTTTTtttttttttdddk.",
        "ktttttttttttdddddk.",
        "kbHHbbbbbbbbkddTtk.",
        ".bHLLLLLLLLMbdTTtdk",
        ".bkkkLLLkkkMMbdtdk.",
        ".bLWkLLLkWLMDMbdk..",
        "bLLLLLLLLLLMDMbtk..",
        "bLLLLDLLLLMMMbtdTk.",
        ".bLLDDLLLMMMMbdTtk.",
        ".bLLLLLLMMMMbkdtdk.",
        "..bLLtttLMMbk.ktk..",
        "...bLLLMMMbk...kk..",
        "....bbbbbbk........",
    ], {"k": "ink", "T": "ter_l", "t": "ter_m", "d": "ter_d", "b": "brown", "H": "brown",
        "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "lin_l"})
    return f, pal


# --------------------------------------------------------------------------
# Goatherd (male): rough goat-hair cloak, syrinx at his lips, a goat-bell.
# Komatas, the goatherd the bees fed in Theocritus, so one bee follows him.
# --------------------------------------------------------------------------

def goatherd():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (64, 40, 32)),
        ("gh_l", (152, 128, 104)), ("gh_m", (104, 88, 72)), ("gh_d", (64, 56, 48)),
        ("oat_l", (232, 216, 176)), ("oat_m", (208, 184, 136)), ("oat_d", (160, 128, 88)),
        ("gold_l", (240, 192, 64)), ("gold_d", (184, 120, 40)),
        ("brown", (96, 56, 40)),
        ("cord", (184, 88, 48)),
    ])
    skin = skin_mat("brown")
    goat = Mat(["gh_d", "gh_m", "gh_l"], outline="ink", wx=0.75, wy=0.35, cuts=[0.4, 0.75])
    tunic = Mat(["oat_d", "oat_m", "oat_l"], outline="brown", wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    lea = Mat(["brown"])
    f = Fig(pal)

    # shaggy goat-hair cloak down his back, ragged hem
    back = f.poly([(33, 22), (42, 22), (47, 27), (49, 36), (50, 46), (49, 50), (47, 48), (45, 51), (43, 48),
                   (41, 51), (39, 47), (37, 49)], goat, group=60)
    # legs planted wide, wrapped in leather thongs
    f.poly([(26, 44), (31, 44), (30, 50), (28, 57), (24, 57), (25, 50)], skin, group=100)
    f.poly([(35, 44), (39, 44), (41, 50), (43, 57), (39, 57), (37, 50)], skin, group=101)
    f.poly([(22, 57), (29, 57), (29, 61), (21, 61)], lea)
    f.poly([(38, 57), (44, 57), (46, 61), (38, 61)], lea)
    f.rect(29, 20, 35, 25, skin, group=400)
    # coarse undyed tunic, rope belt, ragged hem
    body = f.poly([(26, 24), (39, 24), (41, 33), (43, 46), (36, 47), (24, 46), (25, 33)], tunic)
    f.rect(23, 34, 44, 35, lea, clip=body, noline=True)
    f.shade_poly([(31, 37), (32, 37), (32, 46), (31, 46)], 0.45)
    f.shade_poly([(37, 37), (38, 37), (40, 46), (39, 46)], 0.45)
    f.shade_poly([(25, 36), (28, 36), (27, 46), (24, 46)], -0.3)
    # the cloak thrown over his far shoulder
    front = f.poly([(35, 23), (41, 22), (45, 26), (45, 32), (42, 37), (40, 34), (38, 35), (37, 30)], goat, group=70)
    # near arm raised, holding the pipes to his lips
    f.thick_line([(27, 25), (21, 31)], 5, skin, group=200)
    f.thick_line([(21, 31), (25, 25)], 4, skin, group=201)

    # goat-hair: long strands
    f.textures = [((back, front), ["gh_d", "gh_m", "gh_l"], stagger(33, 23, 50, 50, 3, 4), [(0, 0), (0, 1), (1, 2)])]
    # ragged tunic hem and leg thongs
    f.erase_px([(27, 46), (33, 47), (40, 46)])
    f.pxs([(27, 45), (33, 46), (40, 45)], "brown")
    for y in (49, 52, 55):
        f.line([(25, y), (30, y + 1)], "brown")
        f.line([(38, y), (42, y + 1)], "brown")
    # bronze goat-bell hanging from his rope belt
    f.patch(29, 35, [
        "...k...",
        "..kkk..",
        ".kGGgk.",
        ".kGggk.",
        "kGGggdk",
        "kGgggdk",
        "kkkkkkk",
        "...g...",
    ], {"k": "ink", "G": "gold_l", "g": "gold_d", "d": "brown"})
    # one bee, for the goatherd the bees fed
    f.patch(47, 9, [
        "..WW.",
        ".kGkG",
        "..kk.",
    ], {"k": "ink", "G": "gold_l", "W": "oat_l"})
    # head: wild dark curls going gray, a full beard
    f.patch(24, 3, [
        "....kk.kkk.kk......",
        "..kkhhkhhHkkhhk....",
        ".khHHhkHgHHkhHHk...",
        ".kHhhHHhhHhhHhHHk..",
        "khHHHhHHHHhHHHhHk..",
        "kHgHHHhhHHHhhHHHHk.",
        "khHHHhHHHhHHHhHHHk.",
        "kHHhLLLLLLHhhHHhHHk",
        "khHLLLLLLLLMHHhHHHk",
        ".kHLHHHLLHHHMbhHHHk",
        ".kLLWkLLLkWMMDbHhHk",
        ".bLLWkLLLkWMDDbhHk.",
        "bLLLLLLLLLMMDbHhHk.",
        "bLLLDLLLLMMMbhHHk..",
        ".bhHDHHhHHhHHhHHk..",
        ".khHhHHhHHHhHHHk...",
        ".kHHhHhHHhHHhHHk...",
        "..khHHHhHHhHHk.....",
        "...kHhHHhHHHk......",
        "....kkHhHHkk.......",
        "......kkkk.........",
    ], {"k": "ink", "H": "hair", "h": "brown", "g": "gh_l", "b": "brown", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "W": "oat_l"})
    # the syrinx: reeds bound with a red cord, longest on the left
    f.patch(17, 18, [
        "kkkkkkkkkkkkk",
        "kWkWkWkWkWkWk",
        "kcccccccccccc",
        "kWkWkWkWkWkWk",
        "kWkWkWkWkWkk.",
        "kWkWkWkWkk...",
        "kWkWkWkk.....",
        "kWkWkk.......",
        "kmkk.........",
        "kk...........",
    ], {"k": "ink", "W": "oat_l", "m": "oat_m", "c": "cord"})
    # fingers on the reeds
    f.patch(23, 22, [
        ".bbbb.",
        "bLLLLb",
        "bLbLMb",
        "bLLMMb",
        ".bbbb.",
    ], {"b": "brown", "L": "skin_l", "M": "skin_m"})
    return f, pal


# --------------------------------------------------------------------------
# Hoplite (male): bronze crested helmet pushed up, hoplon with a painted
# Lakonian lambda, spear. Agis is a Lakonian youth, so he shares Kleon's crimson.
# --------------------------------------------------------------------------

def hoplite():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("brown", (104, 56, 40)),
        ("hair", (48, 32, 32)),
        ("cr_l", (216, 72, 64)), ("cr_m", (168, 40, 48)), ("cr_d", (104, 24, 40)),
        ("br_l", (248, 216, 120)), ("br_m", (216, 160, 64)), ("br_d", (144, 88, 40)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 176, 144)),
        ("wood", (176, 120, 72)),
    ])
    skin = skin_mat("brown")
    bronze = Mat(["br_d", "br_m", "br_l"], cuts=[0.35, 0.72])
    crimson = Mat(["cr_d", "cr_m", "cr_l"], wx=0.85, wy=0.2, cuts=[0.25, 0.65])
    linen = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.6])
    wood = Mat(["br_d", "wood"], cuts=[0.75])
    lea = Mat(["brown"])
    f = Fig(pal)

    # crimson cloak behind his shoulders
    f.poly([(23, 24), (40, 23), (44, 30), (46, 44), (40, 47), (24, 47), (19, 42), (21, 30)], crimson, bias=0.3)
    # spear held low and forward, butt behind his near leg
    pole(f, (8, 7), (29, 56), wood, group=50)
    # legs: a wide, ready stance, bronze greaves on the shins
    f.poly([(25, 45), (30, 45), (29, 51), (27, 57), (23, 57), (24, 51)], skin, group=100)
    f.poly([(35, 45), (39, 45), (41, 51), (43, 57), (39, 57), (37, 51)], skin, group=101)
    f.poly([(23, 50), (29, 50), (28, 57), (23, 57)], bronze, group=110)
    f.poly([(37, 50), (41, 50), (43, 57), (39, 57)], bronze, group=111)
    f.poly([(21, 57), (28, 57), (28, 61), (20, 61)], lea)
    f.poly([(38, 57), (44, 57), (46, 61), (38, 61)], lea)
    # crimson chiton skirt under white linen strips (pteruges)
    f.poly([(24, 39), (41, 39), (43, 47), (22, 47)], crimson)
    # linen corselet with shoulder flaps
    f.poly([(25, 23), (39, 23), (41, 33), (41, 41), (25, 41), (24, 33)], linen)
    f.rect(23, 38, 42, 39, bronze, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # near arm (his right) grips the spear at his chest
    f.poly([(23, 23), (28, 23), (28, 28), (24, 29)], linen, group=210)
    f.thick_line([(25, 27), (22, 34)], 5, skin, group=200)
    f.thick_line([(22, 34), (19, 31)], 4, skin, group=200)
    # the hoplon on his far arm: bronze rim, crimson face, painted lambda
    rim = f.ellipse((29, 25, 54, 50), bronze, group=600)
    f.ellipse((31, 27, 52, 48), crimson, group=610, clip=rim, noline=True)
    f.shade_poly([(31, 27), (40, 27), (33, 36), (31, 40)], -0.35)

    # pteruges strips
    for x in (25, 28, 31):
        f.line([(x, 40), (x - 1, 46)], "lin_l")
        f.line([(x + 1, 40), (x, 46)], "lin_d")
    # greave ridges and sandal straps
    f.line([(25, 51), (25, 56)], "br_l")
    f.line([(39, 51), (40, 56)], "br_l")
    # shield rim: a hot highlight at the top left, the dark edge low right
    f.line([(33, 27), (37, 26)], "br_l")
    f.line([(30, 33), (31, 30)], "br_l")
    # the lambda, Lakonia's mark
    f.patch(35, 30, [
        "......kk.......",
        ".....kGGk......",
        ".....kGYk......",
        "....kGYkYk.....",
        "....kGYkYk.....",
        "...kGYk.kYk....",
        "...kGYk.kYk....",
        "..kGYk...kYk...",
        "..kGYk...kYk...",
        ".kGYk.....kYk..",
        ".kGYk.....kYk..",
        "kGYk.......kYk.",
        "kkk.........kk.",
    ], {"k": "cr_d", "G": "br_l", "Y": "br_m"})
    # spearhead, a bronze leaf blade, and the hand around the shaft
    f.patch(5, 0, [
        "..k...",
        ".kGk..",
        ".kGYk.",
        ".kGYk.",
        "..kGYk",
        "..kGYk",
        "...kYk",
        "...kkk",
    ], {"k": "ink", "G": "br_l", "Y": "br_m"})
    f.patch(16, 28, [
        ".bbbb.",
        "bLLLLb",
        "bLbLMb",
        "bLLMMb",
        ".bbbb.",
    ], {"b": "brown", "L": "skin_l", "M": "skin_m"})
    # head: Corinthian helmet pushed up on his crown, crimson crest streaming back
    f.patch(22, 0, [
        ".....kkkkkkk............",
        "...kkRRRRRRrkkk.........",
        "..kRRRRRrrrrrrrkk.......",
        "..kRRrrrrrrrrrrrrkk.....",
        "...kkkkkkkkkkkrrrrrk....",
        ".....kGGGYYYYYkkrrrrk...",
        "....kGGYYYYYYYYYkrrrrk..",
        "...kGGYYYYYYYYYyyrrrrk..",
        ".kkGYYYYYYYYYYYyyykrrrk.",
        "kGkkkYYYYYYYYYYyyykrrk..",
        "kYYYkYYYYYYYYYyyyyykrk..",
        ".kkkkkkkkkkkkkkkkkkkHk..",
        "...bLLLLLLLLMHHHHHk.....",
        "...bLHHHLLHHHMbHHk......",
        "...bLWkLLLkWMDMbHk......",
        "..bLLWkLLLkWMDMbHk......",
        "..bLLLLLLLLMMMbHk.......",
        ".bLLLLDLLLMMMbHk........",
        "..bLLDDLLMMMbk..........",
        "..bLLLbbbMMbk...........",
        "...bLLLLMMbk............",
        "....bbbbbbk.............",
    ], {"k": "ink", "R": "cr_l", "r": "cr_m", "G": "br_l", "Y": "br_m", "y": "br_d", "H": "hair",
        "b": "brown", "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "lin_l"})
    return f, pal


# --------------------------------------------------------------------------
# Augur (male): a bird-watching seer. Staff, an indigo robe with a black-figure
# frieze of birds at the hem, a crow feather in his fillet; he points at the sky.
# --------------------------------------------------------------------------

def augur():
    pal = Palette([
        ("ink", INK),
        *SKIN_FAIR,
        ("brown", (96, 56, 40)),
        ("gray_l", (240, 240, 232)), ("gray_d", (176, 168, 160)),
        ("ind_l", (96, 104, 176)), ("ind_m", (56, 64, 128)), ("ind_d", (32, 32, 80)),
        ("ter_l", (224, 136, 88)), ("ter_d", (176, 88, 48)),
        ("wood", (160, 112, 72)),
        ("gold", (240, 192, 64)),
    ])
    skin = skin_mat("brown")
    robe = Mat(["ind_d", "ind_m", "ind_l"], wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    wood = Mat(["brown", "wood"], cuts=[0.7])
    frieze = Mat(["ter_d", "ter_l"], wx=1.0, wy=0.0, cuts=[0.75])
    lea = Mat(["brown"])
    f = Fig(pal)

    # staff in his far hand, planted beside him
    pole(f, (47, 6), (46, 61), wood, group=50)
    # long robe to the ankles
    body = f.poly([(25, 23), (39, 23), (42, 32), (44, 44), (46, 58), (20, 58), (22, 44), (23, 32)], robe)
    f.poly([(23, 58), (28, 58), (28, 61), (22, 61)], lea)
    f.poly([(35, 58), (40, 58), (41, 61), (35, 61)], lea)
    # himation folds: wrapped from the far shoulder across to the near hip
    for x in (28, 34, 40):
        f.shade_poly([(x, 36), (x + 1, 36), (x + 2 + (x - 33) // 4, 50), (x + 1 + (x - 33) // 4, 50)], 0.45)
    f.shade_poly([(25, 30), (27, 30), (25, 50), (23, 50)], -0.3)
    # himation slung from the far shoulder to the near hip
    f.shade_poly([(36, 24), (42, 26), (26, 46), (23, 44)], 0.3)
    # black-figure frieze of birds around the hem
    f.rect(18, 49, 48, 56, frieze, clip=body, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # far arm forward, hand on the staff
    f.thick_line([(39, 25), (43, 30), (45, 31)], 5, robe, group=300)
    # near arm raised to the sky, the wide sleeve hanging from it
    f.poly([(24, 23), (30, 25), (27, 31), (22, 33), (18, 29), (16, 20), (19, 16), (22, 20)], robe, group=200)
    f.thick_line([(18, 18), (16, 11)], 4, skin, group=210)

    # the frieze: borders and birds in flight
    f.line([(19, 49), (47, 49)], "ink")
    f.line([(19, 56), (47, 56)], "ink")
    f.patch(20, 51, [
        "kk...kk..kk...kk..kk...kk",
        ".kk.kk....kk.kk....kk.kk.",
        "..kkk......kkk......kkk..",
        "...k........k........k...",
    ], {"k": "ink"})
    # sleeve hem and the edge of the himation
    f.line([(16, 28), (21, 32)], "ind_l")
    f.line([(40, 26), (24, 45)], "ind_l")
    # hand on the staff
    f.patch(43, 28, [
        ".bbbb.",
        "bLLLLb",
        "bLbLMb",
        "bLLMMb",
        ".bbbb.",
    ], {"b": "brown", "L": "skin_l", "M": "skin_m"})
    # staff head: a knot of wood
    f.patch(45, 3, [
        ".kkk.",
        "kWwWk",
        "kwWwk",
        ".kwk.",
    ], {"k": "ink", "W": "wood", "w": "brown"})
    # pointing hand, index finger to the birds
    f.patch(12, 3, [
        "..k....",
        ".kLk...",
        ".kLk...",
        ".kLkk..",
        "kLLLLk.",
        "kLLLMk.",
        "kLLMMk.",
        ".kMMk..",
        "..kk...",
    ], {"k": "brown", "L": "skin_l", "M": "skin_m"})
    # head tilted up to the sky: white hair and beard, gold fillet, crow feather
    f.patch(22, 1, [
        ".................kk.",
        "................kIk.",
        "...............kIik.",
        "......kkkkk...kIik..",
        "....kkGGGGgkk.kIik..",
        "...kGGGGGGGggkkIk...",
        "..kGGGGGGGGgggkIk...",
        "..kYYYYYYYYYYYYYk...",
        ".kLLLLLLLLLLMgggk...",
        ".bLgggLLLggggMbgk...",
        ".bLkkLLLLkkMMDbgk...",
        "bLLGGLLLLGGMDMbgk...",
        "bLLLLLLLLLMMDbggk...",
        "bLLLDLLLLMMMbgggk...",
        "kGGGDGGGGGGGgggk....",
        "kGGGkkkGGGGgggk.....",
        "kGGGGGGGGGggggk.....",
        ".kGGGGGGGGgggk......",
        "..kGGGGGgggk........",
        "...kkGGgkk..........",
        ".....kk.............",
    ], {"k": "ink", "I": "ink", "i": "ind_m", "G": "gray_l", "g": "gray_d", "Y": "gold", "b": "brown",
        "L": "skin_l", "M": "skin_m", "D": "skin_d"})
    return f, pal


CLASSES = {
    "shepherd": shepherd,
    "harvester": harvester,
    "goatherd": goatherd,
    "hoplite": hoplite,
    "augur": augur,
}


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

def load_pic(path):
    im = Image.open(path)
    a = np.array(im)
    rgba = im.convert("RGBA")
    px = rgba.load()
    for y, x in zip(*np.nonzero(a == 0)):
        px[int(x), int(y)] = (0, 0, 0, 0)
    return rgba


def battle_tile(im):
    tile = battle_bg().crop((240 - 96, 40, 240, 112)).copy()
    tile.alpha_composite(im, (16, 4))
    return tile


def sheet(images, cols=None):
    tiles = [battle_tile(im) for im in images]
    cols = cols or len(tiles)
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGBA", (96 * cols, 72 * rows))
    for i, t in enumerate(tiles):
        out.alpha_composite(t, (96 * (i % cols), 72 * (i // cols)))
    return out


SHEET = os.path.join(ROOT, "design/phase1/img/sprites_classes.png")


def contact_sheet(figs):
    """3x: Brendan and the cast for scale on the top row, then the classes."""
    refs = [load_pic(os.path.join(FRONT, n + ".png")) for n in
            ("brendan", "kleon", "hierophant_ione", "titan_grunt", "professor_daphne")]
    news = [to_rgba(arr, pal) for arr, pal in figs.values()]
    cols = max(len(refs), 4)
    pad = [Image.new("RGBA", (64, 64))] * (-len(refs) % cols)
    return upscale(sheet(refs + pad + news, cols=cols), 3)


def preview(figs, pv):
    os.makedirs(pv, exist_ok=True)
    contact_sheet(figs).save(os.path.join(pv, "classes.png"))
    for name, (arr, pal) in figs.items():
        upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
        grid_preview(to_rgba(arr, pal), 12, 4, 0, 60, 64).save(os.path.join(pv, name + "_grid.png"))


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in CLASSES]
    figs = {}
    for name, fn in CLASSES.items():
        if only and name not in only:
            continue
        f, pal = fn()
        arr = render(f)
        palette_report(arr, pal, name)
        figs[name] = (arr, pal)
        if write:
            save_indexed(arr, pal, os.path.join(FRONT, name + ".png"))
    if write and not only:
        contact_sheet(figs).save(SHEET)
    if pv:
        preview(figs, pv)


if __name__ == "__main__":
    main()
