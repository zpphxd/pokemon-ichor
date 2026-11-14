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


CLASSES = {
    "shepherd": shepherd,
    "harvester": harvester,
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
