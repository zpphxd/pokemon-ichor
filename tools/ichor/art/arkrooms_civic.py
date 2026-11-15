#!/usr/bin/env python3
"""Arkadia's public rooms and Klymene's upper room: the Asclepeion built against
the outcrop round its spring, the Agora stall round the foot of the town's
biggest cypress, and the old runner's bright room over the racecourse.
Registered into arkrooms_art.STAMPS on import."""
from arkrooms_art import Canvas, stamp, noise

# ---------------------------------------------------------------------------
# The Asclepeion: a mountain one, with a cave spring
# ---------------------------------------------------------------------------


def _counter():
    """4x2: the healer's counter, squared grey limestone under a slab top.
    Row 0: two empty cells (the spring basin stands there), the healer's cell
    (the slab's lip on the top layer) and the slab's end, where a bowl of
    hunters' salve sits. Row 1: the front, all MB_COUNTER, two courses of
    blocks with moss in a joint."""
    mid, top = Canvas(64, 32), Canvas(64, 32)
    for y in range(6, 16):
        for x in range(32, 63):
            if y == 6 or x == 62:
                c = "k"
            elif y == 7:
                c = "9"
            elif y >= 13:
                c = "7" if y < 15 else "k"
            else:
                c = "8" if noise(x, y, 3) > 0.1 else "9"
            (top if x < 48 else mid).put(x, y, c)
    for y in range(16, 31):
        for x in range(1, 63):
            if x in (1, 62) or y in (16, 30):
                c = "k"
            elif y == 23:
                c = "6"
            elif (x + (8 if y > 23 else 0)) % 16 == 0:
                c = "6"
            elif y in (17, 24):
                c = "8"
            else:
                c = "7" if noise(x, y, 4) > 0.08 else "8"
            mid.put(x, y, c)
    for x in range(1, 63):
        mid.put(x, 31, "k" if x in (1, 62) else "6")
    for (x, y) in [(20, 23), (21, 23), (44, 23), (45, 22), (9, 23)]:
        mid.put(x, y, "m")
    mid.put(45, 23, "M")
    # the salve: a little stone bowl with a green paste
    mid.paste(51, 6, """
..kkkk..
.kMMMMk.
k8mMMm8k
k788887k
.k7777k.
..kkkk..
""")
    return mid, top


_m, _t = _counter()
stamp("ark_counter", 4, 2, art=[("rock", _m)], top=[("rock", _t)], walk={(2, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER", (3, 1): "MB_COUNTER"},
      note="the healer's counter, squared limestone under a slab, a bowl of hunters' salve at its end")


def _spring_basin():
    """2x2: where the spring comes out of the rock. Upper cell (on the wall): a
    cleft in the outcrop and the water running down out of it. Lower cell: a
    basin cut in one block, brimming, spilling west into the channel. The
    party's balls are set on its water. Bronze palette (water and marble)."""
    c = Canvas(32, 32)
    # the cleft
    for y in range(2, 18):
        w = 2 + (y - 2) // 5
        for x in range(15 - w, 17 + w):
            c.put(x, y, "k" if abs(x - 15.5) > w - 0.5 else "z")
    for y in range(5, 22):
        c.put(15, y, "U" if y % 3 else "a")
        c.put(16, y, "u" if y % 4 else "U")
    c.put(14, 12, "a")
    c.put(17, 15, "a")
    # the basin
    for y in range(16, 31):
        for x in range(1, 31):
            dx, dy = (x - 15.5) / 14.5, (y - 23.5) / 7.5
            r = dx * dx + dy * dy
            if r > 1.0:
                continue
            ri = ((x - 15.5) / 11.5) ** 2 + ((y - 22.5) / 4.6) ** 2
            if r > 0.84:
                c.put(x, y, "k")
            elif ri <= 1.0:
                c.put(x, y, "u" if ri > 0.72 else ("U" if (x * 3 + y * 5) % 11 else "a"))
            elif y > 26:
                c.put(x, y, "n" if r > 0.55 else "m")
            else:
                c.put(x, y, "M")
    # the lip worn where it spills west
    for y in range(21, 25):
        c.put(1, y, "U")
        c.put(2, y, "u")
        c.put(0, y, "U")
    c.put(12, 21, "a")
    c.put(19, 23, "a")
    return c


stamp("spring_basin", 2, 2, art=[("bronze", _spring_basin())],
      note="the spring, out of a cleft in the rock into a basin cut from one block, spilling west")


def _channel(kind):
    """1x1, walkable: the stone channel that carries the spring across the floor
    to the grating. kind: v, h, ne (from north to east), nw, se, sw, or grate."""
    c = Canvas(16, 16)
    N = kind in ("v", "ne", "nw")
    S = kind in ("v", "se", "sw")
    E = kind in ("h", "ne", "se")
    W = kind in ("h", "nw", "sw", "grate")

    def inside(x, y):
        core = 4 <= x <= 11 and 4 <= y <= 11
        return core or (N and 4 <= x <= 11 and y < 4) or (S and 4 <= x <= 11 and y > 11) or \
            (E and x > 11 and 4 <= y <= 11) or (W and x < 4 and 4 <= y <= 11)

    def edge(x, y):
        return inside(x, y) is False and any(inside(x + dx, y + dy) for dx in (-2, -1, 0, 1, 2)
                                             for dy in (-2, -1, 0, 1, 2) if abs(dx) + abs(dy) <= 2)
    for y in range(16):
        for x in range(16):
            if inside(x, y):
                c.put(x, y, "U" if (x * 5 + y * 3) % 9 else "a")
                if (x + y) % 7 == 0:
                    c.put(x, y, "u")
            elif edge(x, y):
                near = any(inside(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                c.put(x, y, "n" if near else "m")
    if kind == "grate":
        for y in range(3, 13):
            for x in range(3, 13):
                if (x % 3 == 0 or y % 3 == 0) and c.get(x, y) != ".":
                    c.put(x, y, "k")
        c.put(6, 8, "z")
    return c


for _k in ("v", "h", "ne", "nw", "se", "sw", "grate"):
    stamp(f"channel_{_k}", 1, 1, art=[("bronze", _channel(_k))], walk={(0, 0)},
          note=f"the spring's stone channel across the floor ({_k})")


def _pithos_niche():
    """1x2 on the outcrop: a dry niche cut back into the rock for the Pithos.
    The recess is flat rock; the great jar oikia's pithos, in front."""
    c = Canvas(16, 32)                       # below the beam's 8 px band, all rock
    for y in range(8, 32):
        for x in range(1, 15):
            if y < 11:
                r = ((x - 7.5) / 6.5) ** 2 + ((y - 11) / 3.0) ** 2
                if r > 1.0:
                    continue
            c.put(x, y, "6" if x < 3 or y < 11 else "e")
    c.vline(0, 11, 31, "9")
    c.vline(15, 11, 31, "6")
    for y in range(9, 12):
        c.put(1, y, "9")
    return c


stamp("pithos_niche", 1, 2, flat=[("rock", _pithos_niche())],
      note="a dry niche cut back into the rock, where the Pithos stands")


def _rod_relief():
    """1x1 on the outcrop: the rod of Asclepius cut shallow into the rock, the
    serpent picked out in moss. The heal's glow lights it."""
    c = Canvas(16, 16)
    c.vline(7, 1, 15, "6")
    c.vline(8, 1, 15, "9")
    for y in range(3, 14):
        import math
        x = int(round(7.5 + 3 * math.sin((y - 3) / 10 * math.pi * 2.0)))
        c.put(x, y, "M")
        c.put(x + 1, y, "m")
    c.put(9, 2, "M")
    c.put(10, 2, "k")
    return c


stamp("rod_relief", 1, 1, flat=[("rock", _rod_relief())],
      note="the rod of Asclepius cut into the rock, its serpent picked out in moss")


def _herb_bundles(seed):
    """1x1 under the beam: hunters' herbs hung to dry from pegs: yarrow,
    sage, a twist of bark."""
    c = Canvas(16, 16)
    for i, bx in enumerate((2, 7, 12) if seed == 0 else (3, 10)):
        c.put(bx + 1, 0, "K")
        c.put(bx + 1, 1, "n")
        tones = ["G", "g", "v"] if (i + seed) % 2 == 0 else ["g", "v", "V"]
        length = 9 + ((i + seed) * 3) % 4
        for y in range(2, 2 + length):
            half = 1 + (y - 2) // 3
            for x in range(bx + 1 - half, bx + 2 + half):
                if noise(x, y, seed + i) < 0.8:
                    c.put(x, y, tones[(x + y) % 3])
        c.put(bx + 1, 2, "k")
        if (i + seed) % 3 == 1:
            for y in range(4, 4 + length - 2, 3):
                c.put(bx, y, "w")
    return c


stamp("herbs_a", 1, 1, art=[("nature", _herb_bundles(0))], note="hunters' herbs drying under the beam")
stamp("herbs_b", 1, 1, art=[("nature", _herb_bundles(1))], note="more herbs drying under the beam")


def _pallet(blanket):
    """2x1: a patient's straw pallet on a low frame, a blanket thrown back."""
    c = Canvas(32, 16)
    c.box(0, 4, 31, 13, "l")
    c.rect(1, 5, 30, 11, "C")
    for x in range(2, 30, 3):
        c.put(x, 7, "c")
        c.put(x + 1, 9, "c")
    main, dark = {"red": ("r", "R"), "blue": ("U", "u")}[blanket]
    c.rect(13, 5, 30, 11, main)
    for x in range(14, 30, 2):
        c.put(x, 8, dark)
    c.box(1, 5, 7, 10, "c")
    c.hline(2, 6, 6, "C")
    c.hline(0, 31, 13, "d")
    c.put(1, 14, "k")
    c.put(30, 14, "k")
    return c


def _votive_table():
    """2x1: a table of thank-offerings left by the healed: clay arms, a leg,
    a pair of eyes, a hand, each the part the god mended. Clay palette."""
    c = Canvas(32, 16)
    c.box(0, 4, 31, 12, "l")
    c.hline(1, 30, 5, "h")
    c.box(0, 12, 31, 14, "d")
    for x in (2, 29):
        c.put(x, 15, "k")
    c.paste(2, 3, """
.kk...........kk.......kk.kk.
kmmk.........khhk.....kmkkmk.
kmmkkkkkk....kmmk.....kmmmmk.
kmmmmmmmmk...kmmk......kmmk..
.kkkkkkkk....kmmk.......kk...
.............kmmkk...........
.............kmmmmk..........
..............kkkk...........
""")
    c.paste(21, 4, """
kkkkkkk
kcakcak
kkkkkkk
""")
    return c


stamp("votive_table", 2, 1, art=[("clay", _votive_table())],
      note="clay thank-offerings from the healed: an arm, a leg, a pair of eyes, a hand")


def _rug(colors, w, h):
    """w x h, walkable: a woven rug, a border, a meander down the middle."""
    main, border, line = colors
    W, H = w * 16, h * 16
    c = Canvas(W, H)
    c.rect(1, 2, W - 2, H - 3, main)
    for x in range(1, W - 1):
        c.put(x, 2, "k")
        c.put(x, H - 3, "k")
        c.put(x, 3, border)
        c.put(x, H - 4, border)
    for y in range(2, H - 2):
        c.put(1, y, "k")
        c.put(W - 2, y, "k")
        c.put(2, y, border)
        c.put(W - 3, y, border)
    mid = H // 2
    for x in range(6, W - 6):
        k = (x - 6) % 8
        dy = [0, -2, -2, -2, 0, 2, 2, 2][k]
        c.put(x, mid + dy, line)
    for x in range(3, W - 3, 2):                     # fringe
        c.put(x, 1, border)
        c.put(x, H - 2, border)
    return c


stamp("rug_red", 3, 2, art=[("wood", _rug(("r", "y", "R"), 3, 2))],
      walk={(x, y) for x in range(3) for y in range(2)}, note="a woven red rug with a meander")


def _strigil():
    """1x1 on the wall: a runner's strigil and oil flask on a peg."""
    c = Canvas(16, 16)
    c.put(7, 1, "k")
    c.hline(4, 10, 2, "z")
    for y in range(3, 14):
        c.put(5, y, "b")
        c.put(6, y, "y")
    c.put(6, 13, "k")
    c.put(7, 14, "b")
    c.put(8, 14, "y")
    c.put(9, 13, "b")
    c.ellipse(11, 9, 2.5, 3, "y", "k")
    c.put(10, 8, "Y")
    c.vline(11, 4, 6, "z")
    return c


stamp("strigil", 1, 1, art=[("bronze", _strigil())], note="a runner's bronze strigil and oil flask on a peg")


stamp("pallet_red", 2, 1, art=[("wood", _pallet("red"))], note="a patient's pallet, a red blanket thrown back")
stamp("pallet_blue", 2, 1, art=[("wood", _pallet("blue"))], note="a patient's pallet, a blue blanket")

# ---------------------------------------------------------------------------
# The Agora stall, round the foot of the great cypress
# ---------------------------------------------------------------------------


def _trunk():
    """2x4: the great cypress's trunk, rising through the stall. The lower two
    cells are its foot, buttressed and wrapped in a ring of shelves (pots and
    bundles for sale); the upper two are on the top layer, the bark going up
    out of sight. Wall palette: the cypress heartwood reds and the beams."""
    mid, top = Canvas(32, 64), Canvas(32, 64)
    for y in range(0, 64):
        tgt = top if y < 32 else mid
        spread = 0 if y < 40 else (y - 40) // 4
        x0, x1 = 7 - spread, 24 + spread
        for x in range(max(0, x0), min(32, x1 + 1)):
            if x in (x0, x1):
                c = "k"
            else:
                # fibrous bark: long vertical strands, lit on the left
                strand = (x * 3 + (y // 5)) % 7
                c = "r" if x < x0 + 4 else ("D" if x > x1 - 4 else ("R" if strand else "D"))
                if strand == 3 and x < x1 - 3:
                    c = "o" if x < x0 + 6 else "r"
            tgt.put(x, y, c)
    # the ring of shelves round the foot, two tiers
    for (y0, depth) in ((37, 6), (48, 6)):
        mid.box(1, y0, 30, y0 + depth, "2")
        mid.hline(2, 29, y0 + 1, "3")
        mid.hline(2, 29, y0 + depth - 1, "1")
    # goods: jars, bundles, little pots
    mid.paste(3, 32, """
.kk...kkk...........kk...kkk..
kppk.kooK..........kbbk.krrRk.
kpwk.kooK..........kBbk.krrRk.
kppk.kkkk..........kbbk.kRRRk.
.kk.................kk..kkkkk.
""".replace("K", "k"))
    mid.paste(2, 44, """
.kkk..kk..kkk.........kkk.kk..
krrRkkwpkkoo3k.......kbBbkppk.
kRRRkkppkkoo3k.......kbbbkspk.
.kkk..kk..kkk.........kkk.kk..
""")
    mid.paste(4, 56, """
..kkk..kkk.........kkk..kk...
.kwppkkrrRk.......kooo3kbbk..
.kpppkkRRRk.......ko333kbBk..
..kkk..kkk.........kkk..kk...
""")
    mid.hline(0, 31, 63, "k")
    return mid, top


_m, _t = _trunk()
stamp("cypress_trunk", 2, 4, art=[("wall", _m)], top=[("wall", _t)], walk={(0, 0), (1, 0), (0, 1), (1, 1)},
      note="the great cypress's trunk, rising through the stall, a ring of shelves round its foot")


def _roots():
    """2x1, flat on packed earth: the cypress's roots running out from under
    the shelves into the floor."""
    c = Canvas(32, 16)
    for (x0, dx, n) in [(6, -1, 6), (12, 0, 9), (19, 1, 8), (25, 1, 6)]:
        for t in range(n):
            x = x0 + dx * t // 2
            y = t
            c.put(x, y, "j")
            c.put(x + 1, y, "g")
    return c


stamp("roots", 2, 1, flat=[("floor", _roots())], walk={(0, 0), (1, 0)},
      note="the great cypress's roots, running out into the floor")


def _boughs(seed):
    """1x1, top layer: the cypress's boughs over the stall, dark sprays."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            n = noise(x, y, seed)
            depth = 12 - abs(x - 7.5) * 0.4 + noise(x, 0, seed + 3) * 3
            if y < depth and n < 0.88:
                c.put(x, y, "G" if n < 0.4 else ("g" if n < 0.75 else "v"))
    for x in range(16):
        if c.get(x, 0) != ".":
            c.put(x, 0, "G")
    return c


def _net(seed):
    """1x1, top layer: a hunting net looped from the boughs."""
    c = _boughs(seed)
    for x in range(0, 16):
        sag = 6 + int(4 * (1 - ((x - 7.5) / 8) ** 2))
        for y in range(4, sag + 1):
            if (x + y) % 3 == 0 or y == sag:
                c.put(x, y, "n" if y == sag else "j")
    for x in (3, 8, 13):
        c.put(x, 6 + int(4 * (1 - ((x - 7.5) / 8) ** 2)) + 1, "K")
    return c


for _i in range(3):
    stamp(f"boughs_{_i}", 1, 1, top=[("nature", _boughs(_i + 20))], walk={(0, 0)},
          note="the cypress's boughs overhead")
stamp("net_a", 1, 1, top=[("nature", _net(30))], walk={(0, 0)}, note="a hunting net hung from the boughs")
stamp("net_b", 1, 1, top=[("nature", _net(31))], walk={(0, 0)}, note="a hunting net hung from the boughs")


def _shop_counter():
    """3x2: the stall's counter, cypress planks, and on it clay jars of
    moon-cakes for the goddess and a cake out on a cloth. Row 0's middle cell
    is where the stallkeeper stands (the counter's back edge there is on the
    top layer); row 1 is the front, all MB_COUNTER."""
    mid, top = Canvas(48, 32), Canvas(48, 32)
    for y in range(12, 32):
        for x in range(48):
            if y < 22:
                c = "k" if (x in (0, 47) or y == 12) else ("h" if y == 13 else ("m" if y == 21 else "l"))
            else:
                c = "k" if (x in (0, 47) or y == 31) else ("l" if y == 22 else ("d" if x % 6 == 1 else "m"))
            (top if (16 <= x < 32 and y < 16) else mid).put(x, y, c)
    # jars of moon-cakes at the two ends, a cake out on a cloth by the keeper
    for jx in (0, 7, 37):
        mid.paste(jx, 3, """
..kkkk..
.kCccCk.
kcccccck
kCCCCCCk
kcrrrrck
kCCCCCCk
kcccccck
.kCCCCk.
..kkkk..
""")
    mid.rect(17, 16, 26, 20, "c")
    mid.ellipse(21.5, 18, 3, 1.6, "y", "b")
    mid.put(21, 17, "c")
    return mid, top


_m, _t = _shop_counter()
stamp("shop_counter", 3, 2, art=[("wood", _m)], top=[("wood", _t)], walk={(1, 0)},
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER"},
      note="the stall's counter, jars of moon-cakes for the goddess on it")


def _canopy(w, h, gap, seed):
    """w x h cells on the top layer: the great cypress's boughs, the stall's
    roof, a dark mass that thins downward into hanging sprays, with hunting
    nets looped under it. `gap` is the range of columns (in cells) the trunk
    rises through, left clear."""
    W, H = w * 16, h * 16
    c = Canvas(W, H)
    import math
    for x in range(W):
        depth = 13 + 6 * math.sin(x / 11.0 + seed) + 4 * noise(x // 3, 1, seed)
        if x % 7 == 3:
            depth += 6                                   # a hanging spray
        for y in range(H):
            if y > depth:
                continue
            n = noise(x, y, seed)
            edge = depth - y < 3
            if edge and n > 0.55:
                continue
            c.put(x, y, "G" if y < depth * 0.45 or n < 0.3 else ("g" if n < 0.8 else "v"))
            if edge and n < 0.15:
                c.put(x, y, "V")
    # nets: rope loops from spray to spray, a mesh of knots, cork floats
    for (x0, x1) in ((4, 30), (72, 106)):
        if x1 > W:
            continue
        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            sag = int(18 + 7 * math.sin(t * math.pi))
            for y in range(sag - 5, sag + 1):
                if 0 <= y < H and ((x + y) % 4 == 0 or y == sag):
                    c.put(x, y, "n" if y == sag else "j")
            if (x - x0) % 8 == 4:
                c.put(x, sag + 1, "J")
                c.put(x, sag + 2, "K")
    g0, g1 = gap
    for y in range(H):
        for x in range(g0 * 16, g1 * 16):
            c.put(x, y, ".")
    return c


stamp("canopy", 7, 2, top=[("nature", _canopy(7, 2, (2, 4), 3))],
      walk={(x, y) for x in range(7) for y in range(2)},
      note="the great cypress's boughs over the stall, nets looped under them")


def _trunk_shelf(side):
    """1x2: a stepped shelf built against the trunk's side, with bundles of
    arrows' shafts, a coil of rope, snares and a pot of glue."""
    c = Canvas(16, 32)
    for (y0, d) in ((12, 4), (22, 4)):
        c.box(0, y0, 15, y0 + d, "m")
        c.hline(1, 14, y0 + 1, "l")
    c.vline(0 if side == "l" else 15, 10, 31, "d")
    c.paste(2, 4, """
.kk..kkkk..
kjjk.knnnk.
kjjk.knknk.
kjjk.knnnk.
""".replace("j", "h").replace("n", "c"))
    c.paste(3, 16, """
kkk..kk...
krRk.kuk..
kRRk.kUk..
.kk..kk...
""")
    c.hline(0, 15, 31, "k")
    return c


stamp("trunk_shelf_l", 1, 2, art=[("wood", _trunk_shelf("l"))], note="a shelf built against the trunk")
stamp("trunk_shelf_r", 1, 2, art=[("wood", _trunk_shelf("r"))], note="a shelf built against the trunk")


def _fur_table():
    """2x1: a table of furs for sale, a fox's and a hare's, folded."""
    c = Canvas(32, 16)
    c.box(0, 3, 31, 11, "l")
    c.hline(1, 30, 4, "h")
    c.box(0, 11, 31, 13, "d")
    for x in (2, 29):
        c.vline(x, 13, 15, "k")
    c.ellipse(9, 7, 7, 3, "r", "k")
    c.hline(5, 12, 6, "h")
    c.ellipse(22, 7, 7, 3, "C", "k")
    c.hline(18, 25, 6, "c")
    c.put(28, 9, "R")
    return c


stamp("fur_table", 2, 1, art=[("wood", _fur_table())], note="a table of furs: a fox's and a hare's")


def _arrow_rack():
    """2x2 on the wall: a rack of arrows (for display: they don't fly) and a
    bow, the arrows fletched in three colors."""
    c = Canvas(32, 32)
    c.box(2, 4, 29, 7, "m")
    c.hline(3, 28, 5, "l")
    c.box(2, 24, 29, 27, "m")
    c.hline(3, 28, 25, "l")
    for i, x in enumerate(range(5, 28, 3)):
        for y in range(1, 30):
            if 4 <= y <= 7 or 24 <= y <= 27:
                continue
            c.put(x, y, "h")
        c.put(x, 0, "k")
        c.put(x, 1, "z")
        f = ["r", "c", "u"][i % 3]
        for y in (28, 29, 30):
            c.put(x - 1, y, f)
            c.put(x + 1, y, f)
    return c


stamp("arrow_rack", 2, 2, art=[("wood", _arrow_rack())],
      note="a rack of arrows for display; the stallkeeper's husband made them, and they don't fly")


def _bow():
    """1x2 on the wall: a hunting bow, unstrung, on two pegs."""
    c = Canvas(16, 32)
    import math
    for y in range(2, 30):
        x = int(round(5 + 4 * math.sin((y - 2) / 28 * math.pi)))
        c.put(x, y, "m")
        c.put(x + 1, y, "d")
    c.vline(5, 2, 29, "C")
    c.box(9, 8, 12, 10, "d")
    c.box(9, 21, 12, 23, "d")
    return c


stamp("bow", 1, 2, art=[("wood", _bow())], note="a hunting bow on two pegs")


def _hide():
    """2x2 on the wall: a red deer's hide stretched on a frame of poles."""
    c = Canvas(32, 32)
    for y in range(3, 30):
        for x in range(4, 28):
            nx, ny = (x - 15.5) / 11.5, (y - 16) / 13
            if nx * nx + ny * ny > 1.0 and not (abs(nx) > 0.6 and abs(ny) > 0.6 and abs(nx) < 1.1):
                continue
            c.put(x, y, "l" if noise(x, y, 7) > 0.15 else "m")
    for (x, y) in [(10, 10), (20, 12), (14, 20), (18, 7), (11, 22), (21, 21)]:
        c.put(x, y, "c")
        c.put(x + 1, y, "C")
    c.vline(15, 6, 26, "m")
    for x0 in (2, 29):
        c.vline(x0, 1, 31, "d")
    c.hline(2, 29, 1, "d")
    c.hline(2, 29, 30, "d")
    for (x, y) in [(4, 3), (27, 3), (4, 29), (27, 29), (15, 2), (15, 29)]:
        c.put(x, y, "k")
    return c


stamp("deer_hide", 2, 2, art=[("wood", _hide())], note="a red deer's hide stretched on poles")


def _baskets():
    """1x1: two baskets of chestnuts and acorns for sale."""
    c = Canvas(16, 16)
    for (cx, cy, fill) in ((4.5, 10, "d"), (11, 11, "K")):
        c.ellipse(cx, cy, 4, 4, "j", "k")
        c.ellipse(cx, cy - 2, 3, 1.5, fill)
        for x in range(int(cx - 2), int(cx + 3)):
            if (x * 7) % 3 == 0:
                c.put(x, int(cy - 2), "m" if fill == "d" else "J")
    return c


stamp("nut_baskets", 1, 1, art=[("nature", _baskets())], note="baskets of chestnuts and acorns")

# ---------------------------------------------------------------------------
# Klymene's upper room over the racecourse
# ---------------------------------------------------------------------------


def _track_window():
    """2x2 on the wall: a wide window over the racecourse at dusk. Seen from
    above it: the evening sky, a row of cypresses on the far side, and the
    straight flat track crossing the whole view, the stone starting line
    pale across it and a runner coming."""
    c = Canvas(32, 32)
    for y in range(4, 28):
        for x in range(2, 30):
            c.put(x, y, "a" if y < 8 else ("B" if y < 11 else "b"))
    for (x0, hgt) in [(4, 9), (9, 7), (14, 10), (20, 8), (25, 9)]:   # cypresses, dark against dusk
        for y in range(16 - hgt, 17):
            half = min((y - (16 - hgt)) // 2, 2)
            for x in range(x0 - half, x0 + half + 1):
                c.put(x, y, "D" if x <= x0 else "k")
    for y in range(16, 28):
        for x in range(2, 30):
            if y < 18:
                c.put(x, y, "2")                     # the far bank
            elif y < 25:
                c.put(x, y, "o" if (x * 3 + y) % 9 else "3")   # the track, packed earth
            else:
                c.put(x, y, "1")                     # the near bank, in shadow
    for y in range(18, 25):                          # the starting line
        c.put(22, y, "w")
        c.put(23, y, "p")
    c.paste(9, 18, """
.k.
kRk
.R.
k.k
""")                                                 # a runner, coming
    # the frame: lintel, mullion, sill, the blue shutters folded back
    c.hline(1, 30, 3, "k")
    c.hline(1, 30, 2, "1")
    c.vline(16, 4, 27, "2")
    c.vline(1, 3, 28, "k")
    c.vline(30, 3, 28, "k")
    c.hline(1, 30, 28, "3")
    c.hline(1, 30, 29, "2")
    c.hline(1, 30, 30, "1")
    for x in (0, 31):
        c.vline(x, 4, 27, "b")
    return c


stamp("track_window", 2, 2, art=[("wall", _track_window())],
      note="a wide window over the racecourse: the track running away between the cypresses")


def _window_bench():
    """2x1: the bench under the window where she watches the runners, a
    cushion at one end."""
    c = Canvas(32, 16)
    c.box(0, 4, 31, 10, "l")
    c.hline(1, 30, 5, "h")
    c.box(0, 10, 31, 13, "m")
    for x in (2, 3, 28, 29):
        c.vline(x, 13, 15, "d")
    c.box(18, 3, 29, 9, "r")
    c.hline(19, 28, 4, "c")
    c.hline(19, 28, 8, "R")
    return c


stamp("window_bench", 2, 1, art=[("wood", _window_bench())], note="the bench under the window, a red cushion on it")


SANDAL = """
.kkk.
kllhk
kmllk
kmldk
kmmmk
kmlmk
kdmdk
.kkk.
"""


def _sandals(pairs, tags):
    """1x1 on the wall: old running sandals hung in pairs from a peg by their
    straps, soles out, a date scratched on a tag by each pair."""
    c = Canvas(16, 16)
    for i in range(pairs):
        x0 = 0 + i * 8 if pairs == 2 else 3
        c.put(x0 + 4, 0, "k")
        c.put(x0 + 3, 1, "d")
        c.put(x0 + 5, 1, "d")
        c.put(x0 + 2, 2, "d")
        c.put(x0 + 6, 2, "d")
        c.paste(x0, 3, SANDAL)
        c.paste(x0 + 4, 4, SANDAL)
        if tags:
            c.put(x0 + 1, 12, "k")
            c.put(x0 + 1, 13, "c")
            c.put(x0 + 2, 13, "c")
            c.put(x0 + 1, 14, "C")
            c.put(x0 + 2, 14, "c")
    return c


stamp("sandals_2", 1, 1, art=[("wood", _sandals(2, True))], note="running sandals hung in pairs, each pair tagged")
stamp("sandals_1", 1, 1, art=[("wood", _sandals(1, True))], note="a pair of running sandals, tagged with a date")


def _ribbon():
    """1x2 on the wall: a victor's ribbon on a nail, its red gone pale pink,
    its long ends trailing."""
    c = Canvas(16, 32)
    c.put(7, 2, "k")
    c.ellipse(7.5, 6, 4, 3, "C", "k")
    c.ellipse(7.5, 6, 2, 1.2, ".")
    for y in range(8, 29):
        c.put(5 - (y - 8) // 8, y, "C" if y % 5 else "r")
        c.put(6 - (y - 8) // 8, y, "c")
        c.put(10 + (y - 8) // 10, y, "c" if y % 4 else "r")
        c.put(9 + (y - 8) // 10, y, "C")
    return c


stamp("ribbon", 1, 2, art=[("wood", _ribbon())], note="a victor's ribbon gone pale, its ends trailing")


def _apple_shelf():
    """2x1 on the wall: a shelf and on it three wooden apples painted gold.
    Bronze palette: the shelf is its dark golds."""
    c = Canvas(32, 16)
    c.box(1, 11, 30, 13, "b")
    c.hline(2, 29, 12, "y")
    c.put(4, 14, "k")
    c.put(27, 14, "k")
    c.put(4, 15, "z")
    c.put(27, 15, "z")
    for ax in (5, 13, 21):
        c.paste(ax, 3, """
...z..
..kzk.
.kyYyk
kyYYyb
kyyyyb
kbyybk
.kbbk.
""")
    return c


stamp("apple_shelf", 2, 1, art=[("bronze", _apple_shelf())],
      note="a shelf with three wooden apples painted gold")


def _stair_down():
    """2x1, flat: the stair down to the street door, its well in the boards,
    a rail along its west side. Both cells are the exit."""
    c = Canvas(32, 16)
    for y in range(16):
        for x in range(32):
            if x in (0, 31):
                c.put(x, y, "k")
            elif x in (1, 2):
                c.put(x, y, "m" if x == 1 else "l")
            else:
                step = y // 4
                c.put(x, y, ["h", "l", "m", "d"][step] if y % 4 else "k")
    return c


stamp("stair_down", 2, 1, flat=[("wood", _stair_down())], walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"},
      note="the stair down to the street; both cells are the exit")


def _rail_post():
    """1x1: the stair's rail post and the rail running down beside the well."""
    c = Canvas(16, 16)
    c.box(4, 2, 8, 15, "l")
    c.vline(5, 3, 14, "h")
    c.vline(7, 3, 14, "m")
    c.box(3, 0, 9, 3, "m")
    c.hline(4, 8, 1, "h")
    return c


stamp("stair_rail", 1, 1, art=[("wood", _rail_post())], note="the stair's rail post")
