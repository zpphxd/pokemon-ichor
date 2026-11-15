#!/usr/bin/env python3
"""Eleutherai's pieces: the fort's watch-house, Oinoe's house by the empty
temple, and Lysidike's farmhouse among the sheep pens. Registered into
thyrsa_rooms_art.STAMPS on import."""
from thyrsa_rooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, OA  # noqa: F401

# ---- the watch-house ------------------------------------------------------

# arrow_slit: see below


# spear_rack: see below

stamp("shield_club", 1, 1, art=[("bronze", """
.......kk.......
......kzzk......
...kkkkkkkkkk...
..kyyYYYYYYyyk..
.kyyMMMMMMMMyzk.
.kyMMMMMMkkMMzk.
kyyMMMMMkkkkMbzk
kyMMMMMkkkkkMbzk
kyMMMMkkkkkMMbzk
kyMMMkkkkMMMMbzk
kyMMkkkMMMMMMbzk
.kbmkkMMMMMMbzk.
.kzbmmMMMMmbzzk.
..kzzbbbbbbzzk..
...kkkkkkkkkk...
................
""")], note="a hoplite's round shield on its peg, white-faced with the black club of Herakles")

stamp("shield_ring", 1, 1, art=[("bronze", """
.......kk.......
......kzzk......
...kkkkkkkkkk...
..kyyYYYYYYyyk..
.kyYrrrrrrrryzk.
.kyrrrrrrrrrrzk.
kyyrrkkkkkkrrbzk
kyrrrkyYYbkrrbzk
kyrrrkybbzkrrbzk
kyrrrkkkkkkrrbzk
kyrrrrrrrrrrrbzk
.kbrrrrrrrrrbzk.
.kzbrrrrrrrbzzk.
..kzzbbbbbbzzk..
...kkkkkkkkkk...
................
""")], note="a round shield, red with a bronze boss")

stamp("bunk", 1, 2, art=[("wood", """
................
.kkkkkkkkkkkkkk.
.khhhhhhhhhhhlk.
.klkkkkkkkkkkmk.
.klkcccccccCkmk.
.klcccCcccCCkmk.
.klkCCCCCCCCkmk.
.klkyybybbybkmk.
.klkybyybbybkmk.
.klkyybybyybkmk.
.klkkkkkkkkkkmk.
.klRrrrrrrrrRmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klRRRRRRRRRRmk.
.klRrrrrrrrrRmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klRRRRRRRRRRmk.
.klRrrrrrrrrRmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klRRRRRRRRRRmk.
.klRrrrrrrrrRmk.
.klRRRRRRRRRRmk.
.klkkkkkkkkkkmk.
.khhhhhhhhhhhlk.
.kmmmmmmmmmmmdk.
.kkkkkkkkkkkkkk.
.kdk........kdk.
.kkk........kkk.
................
""")], note="a garrison cot: a straw tick, a rolled cloak for a pillow, a red army blanket")


# hearth_chain: see below

stamp("dice_table", 2, 1, art=[("wood", """
................................
................................
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.khhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
.khllhlllllhllllhlllllhlllllllk.
.khlkhkhkhkhlllllllllllcllllldk.
.khlhhhhhhhhllllllllllcCclllldk.
.khlkhkhkhkhlllllcllllllllllldk.
.khlhhhhhhhhllllcCcllllkkkllldk.
.khlkhkhkhkhlllllllllllkRkllldk.
.kmmmmmmmmmmmmmmmmmmmmmmkkmmmdk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
..kmdk....................kmdk..
..kmdk....................kmdk..
..kmdk....................kmdk..
..kkkk....................kkkk..
""")], note="the barrack table, a dice board scratched into it, two knucklebones and a cup")

stamp("bench", 2, 1, art=[("wood", """
................................
................................
................................
................................
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
..khhhhhhhhhhhhhhhhhhhhhhhhhhk..
..klllllllllllllllllllllllllmk..
..kmmmmmmmmmmmmmmmmmmmmmmmmmdk..
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
...kmk....................kmk...
...kmk....................kmk...
...kdk....................kdk...
...kkk....................kkk...
................................
................................
""")], note="a plank bench")

# helmet_shelf: see below

# ---- Oinoe's house ---------------------------------------------------------


def _brooms():
    g = [["."] * 32 for _ in range(32)]

    def put(x, y, c):
        if 0 <= x < 32 and 0 <= y < 32:
            g[y][x] = c
    # four brooms leaning on the wall, each more worn: the newest is longest
    for (bx, top, head) in ((4, 2, 11), (11, 6, 8), (18, 10, 5), (25, 14, 3)):
        for y in range(top, 31 - head):
            put(bx - 1, y, "k")
            put(bx, y, "j")
            put(bx + 1, y, "K")
            put(bx + 2, y, "k")
        put(bx, top - 1, "k")
        put(bx + 1, top - 1, "k")
        hy = 31 - head
        for y in range(hy, 31):
            spread = 1 + (y - hy) * 3 // max(1, head)
            for x in range(bx - spread, bx + 3 + spread):
                c = "J" if (x + y) % 3 else "j"
                if x in (bx - spread, bx + 2 + spread):
                    c = "k"
                put(x, y, c)
        for x in range(bx - 1, bx + 3):
            put(x, hy, "k")
            put(x, hy + 1, "n")
        for x in range(bx - 4, bx + 7):
            if g[30][x] != ".":
                put(x, 30, "K" if g[30][x] != "k" else "k")
        for x in range(bx - 4, bx + 7):
            if g[31 - 1][x] != ".":
                put(x, 31, "k")
    return "\n".join("".join(r) for r in g)


stamp("brooms", 2, 2, art=[("nature", _brooms())],
      note="a row of brooms against the wall, each worn shorter than the last: three hundred years of sweeping")

stamp("broom_stub", 1, 1, art=[("nature", """
.........kk.....
........kjKk....
........kjKk....
.......kjKk.....
.......kjKk.....
......kjKk......
......kjKk......
.....kjKk.......
....kkkkk.......
....knnnk.......
...kJJjJJk......
..kJjJJjJJk.....
..kjJJjJjJk.....
...kkkkkkk......
................
................
""")], note="Oinoe's broom by the door, worn down to a stub")

stamp("garlands", 1, 2, art=[("nature", """
................
................
................
................
................
...k........k...
...K........K...
...K........K...
..kGk......kGk..
.kgvGk....kgVgk.
kgV.gGk..kG..vgk
kG...gk..kg...Gk
kv...Gk..kG...vk
.kg.vk....kgVgk.
.kGgGk....kGgk..
..kkk......kk...
..kpk...........
..kPk...........
...k............
................
................
................
................
................
................
................
................
................
................
................
................
................
""")], note="ivy garlands drying from pegs in the beam")

stamp("god_niche", 1, 2, flat=[("wall", """
................
................
................
................
................
................
................
................
.....kkkkkk.....
....kSSSSSSk....
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
...kSSSSSSSSk...
..kwwwwwwwwwwk..
..kppppppppppk..
...kssssssssk...
""")], art=[("clay", """
................
................
................
................
................
................
................
................
................
................
......kkkk......
.....kmllmk.....
.....klkklk.....
....kdlhhlk.....
.....kmkkmdk....
......kmlmk.....
.....kdmmmdk....
.....kmllmdk....
.....kdlmmdk....
......kkkkk.....
................
................
""")], note="a niche with a little clay copy of the god's old image: a cheerful face like a happy dog")

stamp("loom_ivy", 2, 3, art=recolor(recolor(OA.STAMPS["loom"]["img"], "wood",
                                            {"u": "o", "U": "h"}), "wood", {"r": "o", "R": "d"}),
      note="Oinoe's loom: a band of ivy leaves half-woven on the warp")

stamp("pallet", 2, 1, art=[("wood", """
................................
................................
................................
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.kcccCkyybybbybybyybybbybyybbyk.
.kccCCkybyybbybyyybybybyybybybk.
.kcCCCkuuuuuuuuuuuuuuuuuuuuuuuk.
.kCCCkUuuuuUuuuuuUuuuuuUuuuuuuk.
.kkkkkuuuuuuuuuuuuuuuuuuuuuuuuk.
.kmmmkkkkkkkkkkkkkkkkkkkkkkkkkk.
.kddmmmmmmmmmmmmmmmmmmmmmmmmmdk.
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
................................
................................
................................
................................
""")], note="a low straw pallet under a blue wool blanket")

# ---- Lysidike's house ------------------------------------------------------

def _pen():
    """The lambing pen, 3x3 in a corner: wattle hurdles on the west and south
    (and the back one against the wall), clean straw, a lamb asleep in it.
    The weave and the straw repeat every 8 px, so the pen costs few tiles."""
    W, H = 48, 48
    g = [["."] * W for _ in range(H)]

    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            g[y][x] = c
    STRAW = ["JjJJJJjJ", "JJJjJJJJ", "jJJJKJJj", "JJjJJJJJ", "JJJJjJKJ", "JKJJJJJJ", "JJJjJJjJ", "jJJJJJJJ"]
    for y in range(12, 36):
        for x in range(6, W):
            put(x, y, STRAW[y % 8][x % 8])
    # hurdles: horizontal withies woven between uprights every 8 px
    WEAVE = ["kjKjjKjk", "kJjJJjJk", "kKjKKjKk", "kjJjjJjk"]

    def hurdle_h(y0, x0, x1):
        for y in range(y0, y0 + 8):
            for x in range(x0, x1):
                if x % 8 == 0:
                    c = "k" if y in (y0, y0 + 7) else "K"
                elif y in (y0, y0 + 7):
                    c = "k"
                else:
                    c = WEAVE[(y - y0 + x // 8) % 4][x % 8]
                put(x, y, c)
        for x in range(x0, x1, 8):           # the uprights' tops
            put(x, y0 - 2, "k")
            put(x, y0 - 1, "j")

    def hurdle_v(x0, y0, y1):
        for y in range(y0, y1):
            for x in range(x0, x0 + 5):
                if x in (x0, x0 + 4):
                    c = "k"
                elif y % 8 == 0:
                    c = "K"
                else:
                    c = "j" if (y // 2 + x) % 2 else "J"
                put(x, y, c)
    hurdle_h(4, 0, W)           # the back hurdle, against the wall
    hurdle_v(1, 4, 44)          # the west side
    hurdle_h(36, 0, W)          # the south side, toward the room
    # the lamb, curled asleep with its nose tucked in
    LAMB = ["....kkkkkkk.....",
            "..kkwwwnwwwkk...",
            ".kwwwnwwwwnwwk..",
            "kwnwwwwwwwwwwwk.",
            "kwwwwnwwwnwwkkkk",
            "kwnwwwwwwwwkwwwk",
            "kwwwwwwnwwkwkwwk",
            ".kwwnwwwwwkwwwnk",
            "..kkwwwwwkkkkkk.",
            "....kkkkk......."]
    for dy, row in enumerate(LAMB):
        for dx, c in enumerate(row):
            if c != ".":
                put(20 + dx, 19 + dy, c)
    return "\n".join("".join(r) for r in g)


stamp("pen", 3, 3, art=[("nature", _pen())],
      note="the lambing pen: wattle hurdles, clean straw, and a lamb asleep in it")

stamp("cheese_shelf", 2, 1, art=[("wood", """
................................
................................
..kkkkk...kkkkkk....kkkkk.......
.kcccCCk.kccccCCk..kcccCCk..kkk.
.kcCcCCk.kcccCcCk..kcCcCCk.kcCk.
.kccCCCk.kcCcccCk..kccCcCk.kccCk
.kCCCCdk.kCcCCCCdk.kCCCCdk.kCCdk
..kkkkk...kkkkkkk...kkkkk...kkk.
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
..kdk......................kdk..
...kk......................kk...
................................
................................
""")], note="a board of new cheeses, drying on the wall")

_COT_FRAME = """
................
.kkkkkkkkkkkkkk.
.khhhhhhhhhhhlk.
.klkkkkkkkkkkmk.
.klkcccccccCkmk.
.klcccCcccCCkmk.
.klkCCCCCCCCkmk.
.klkkkkkkkkkkmk.
"""

stamp("cot_lyre", 1, 2, art=[("wood", """
................
.kkkkkkkkkkkkkk.
.khhhhhhhhhhhlk.
.klkkkkkkkkkkmk.
.klkcccccccCkmk.
.klcccCcccCCkmk.
.klkCCCCCCCCkmk.
.klkkkkkkkkkkmk.
.klUuuuuUuuuuUmk
.klukkkkuuuuuumk
.klkylhykuuuuumk
.kkydlldykuuuumk
.kkyddddykUuuumk
.kkydlldykuuuumk
.klkyddykuuuuumk
.kluckkcuuuuuumk
.kluucycuuuuuumk
.klUuucycuuuuUmk
.kluuuukykuuuumk
.kluuuuukkuuuumk
.kluuuuuuuuuuumk
.klUuuuuUuuuuUmk
.kluuuuuuuuuuumk
.kluuuuuuuuuuumk
.klkkkkkkkkkkkmk
.khhhhhhhhhhhlk.
.kmmmmmmmmmmmdk.
.kkkkkkkkkkkkkk.
.kdk........kdk.
.kkk........kkk.
................
................
""")], note="Amphis's cot, a tortoiseshell lyre on the blanket")

stamp("cot_weights", 1, 2, art=[("wood", """
................
.kkkkkkkkkkkkkk.
.khhhhhhhhhhhlk.
.klkkkkkkkkkkmk.
.klkcccccccCkmk.
.klcccCcccCCkmk.
.klkCCCCCCCCkmk.
.klkkkkkkkkkkmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klrkkkrrrkkkmk.
.klkdddkrkdddkk.
.klkdzdkkkdzdkk.
.klkdddkzkdddkk.
.klrkkkrrrkkkmk.
.klrrrrrrrrrrmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klrrrrrrrrrrmk.
.klRrrrrrrrrRmk.
.klrrrrrrrrrrmk.
.klrrrrrrrrrrmk.
.klRRRRRRRRRRmk.
.klkkkkkkkkkkmk.
.khhhhhhhhhhhlk.
.kmmmmmmmmmmmdk.
.kkkkkkkkkkkkkk.
kkcCcCcCcCcCcCkk
kcCcCcCcCcCcCcCk
.kkkkkkkkkkkkkk.
................
................
""")], note="Zetes's cot: lead jumping-weights on the blanket, a wrestling mat rolled under it")

stamp("fleece", 2, 1, art=[("nature", """
................................
................................
.....kkkkkkk.......kkkkkkkk.....
...kkwwnwwwwkkkkkkkwwwnwwwwkk...
..kwwwwwwnwwwwwnwwwwwwwwwnwwwk..
.kwwnwwwwwwwnwwwwwnwwwwwwwwwwwk.
.kwwwwwnwwwwwwwwwwwwwnwwwwnwwwk.
kwwnwwwwwwnwwwwnwwwwwwwwwwwwnwwk
kwwwwwnwwwwwwwwwwwnwwwwnwwwwwwwk
kwnwwwwwwwwnwwwwwwwwwwwwwwnwwwwk
.kwwwwnwwwwwwwwnwwwwwnwwwwwwwwk.
.kwwnwwwwwnwwwwwwwwwwwwwwnwwwwk.
..kwwwwwwwwwwnwwwwnwwwwwwwwwwk..
...kkwwnwwwkkkkkkkkwwwwnwwkkk...
.....kkkkkk........kkkkkkk......
................................
""")], walk={(0, 0), (1, 0)}, note="a sheepskin on the floor")

stamp("milk_pails", 1, 1, art=[("nature", """
................
................
................
...kkkkk........
..kKjjjKk.......
..kwwwwwk..kkkk.
..kKwwwKk.kKjjKk
..kjjjjjk.kwwwwk
..kKjjjKk.kKjjKk
..kjjjjjk.kjjjjk
..kKKKKKk.kKKKKk
...kkkkk...kkkk.
................
................
................
................
""")], note="two wooden pails of the morning's milk")


# ---- the watch-house, second drafts ---------------------------------------

def _canvas(w, h):
    return [["."] * w for _ in range(h)]


def _put(g, x, y, c):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = c


def _text(g):
    return "\n".join("".join(r) for r in g)


def _slit():
    g = _canvas(16, 32)
    # a deep embrasure splaying inward, narrowing to a slit of daylight
    for y in range(5, 27):
        t = min(y - 5, 26 - y, 2)
        half = 3 + t // 2
        for x in range(8 - half - 1, 8 + half + 1):
            d = min(x - (8 - half - 1), (8 + half) - x)
            c = "k" if d == 0 else "1" if d <= 2 else "2"
            _put(g, x, y, c)
    for y in range(7, 25):
        _put(g, 7, y, "6")
        _put(g, 8, y, "5")
    for y in (15, 16, 17):                      # the road's green hills
        _put(g, 7, y, "M")
        _put(g, 8, y, "m")
    for x in range(3, 13):                      # the sill
        _put(g, x, 27, "k")
        _put(g, x, 28, "5" if 3 < x < 12 else "k")
        _put(g, x, 29, "3" if 3 < x < 12 else "k")
        _put(g, x, 30, "k")
    return _text(g)


stamp("arrow_slit", 1, 2, art=[("stone", _slit())],
      note="an arrow slit through the fort wall: a sliver of daylight and the road's green hills")


def _spear_rack():
    g = _canvas(32, 48)
    for i, sx in enumerate((5, 12, 19, 26)):
        top = 2 + (i % 2) * 3
        head = ["..k..", ".kyk.", ".kcbk", "kycbk", "kyybk", "kyybk", "kyybk", ".kbk.", ".kzk.", "..k.."]
        for dy, row in enumerate(head):
            for dx, c in enumerate(row):
                if c != ".":
                    _put(g, sx - 2 + dx, top + dy, c)
        for y in range(top + 10, 44):
            _put(g, sx - 1, y, "k")
            _put(g, sx, y, "l" if (y + i) % 9 else "h")
            _put(g, sx + 1, y, "k")
        for y in (44, 45):
            _put(g, sx - 1, y, "k")
            _put(g, sx, y, "z")
            _put(g, sx + 1, y, "k")
        _put(g, sx, 46, "k")
    # the upper rail, pegged into the wall, with a notch round each shaft
    for x in range(1, 31):
        for (y, c) in ((22, "k"), (23, "h"), (24, "l"), (25, "m"), (26, "k")):
            if g[y][x] in ".":
                _put(g, x, y, c)
    for sx in (5, 12, 19, 26):
        _put(g, sx - 1, 23, "k")
        _put(g, sx + 1, 23, "k")
    # the base: a heavy plank with holes for the butts, on two feet
    for x in range(1, 31):
        for (y, c) in ((40, "k"), (41, "h"), (42, "l"), (43, "m"), (44, "d"), (45, "k")):
            if g[y][x] == "." or y in (40, 45):
                if not (g[y][x] in "lhz" and y not in (40,)):
                    _put(g, x, y, c)
    for sx in (5, 12, 19, 26):
        _put(g, sx, 41, "k")
        _put(g, sx, 42, "d")
    for (x0) in (2, 27):
        for y in range(46, 48):
            for x in range(x0, x0 + 3):
                _put(g, x, y, "k" if y == 47 or x in (x0, x0 + 2) else "d")
    return _text(g)


stamp("spear_rack", 2, 3, art=[("wood", _spear_rack())],
      note="a rack of four hoplite spears: leaf-shaped bronze heads, ash shafts, butt-spikes")


def _soot_strip():
    """The lower half of a soot plume, for a hearth set against the wall."""
    BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    TONES = [".", "t", "S", "s", "a"]
    g = _canvas(32, 16)
    for y in range(16):
        for x in range(32):
            hw = 13 - y * 0.45
            ragged = ((x * 37 + y * 23) % 7) / 14.0
            across = max(0.0, 1.0 - abs(x - 15.5) / (hw + ragged))
            d = across ** 0.7 * (1.0 - y / 22) * 4.0
            level = int(d)
            if (d - level) * 16 > BAYER[y % 4][x % 4]:
                level += 1
            g[y][x] = TONES[max(0, min(level, 4))]
    return g


def _hearth_chain():
    g = _canvas(32, 48)
    soot = _soot_strip()
    for y in range(16):
        g[y] = list(soot[y])
    # the chain, from the beam to the cauldron's bail
    for y in range(0, 22):
        if y % 4 in (0, 2):
            _put(g, 15, y, "k"); _put(g, 16, y, "k")
        elif y % 4 == 1:
            _put(g, 14, y, "k"); _put(g, 15, y, "S"); _put(g, 16, y, "S"); _put(g, 17, y, "k")
        else:
            _put(g, 14, y, "k"); _put(g, 15, y, "t"); _put(g, 16, y, "t"); _put(g, 17, y, "k")
    # the raised hearth: a stone platform with a fire bed, seen from above
    for y in range(24, 46):
        for x in range(1, 31):
            edge = x in (1, 30) or y in (24, 45)
            if edge:
                c = "k"
            elif y >= 38:                       # front face, coursed stone
                c = "s" if y in (41, 44) else ("t" if y == 38 else "S")
                if y in (39, 40, 42, 43) and (x + (0 if y < 41 else 4)) % 8 == 0:
                    c = "s"
            elif x in (2, 29) or y in (25, 37):
                c = "t"
            else:
                c = "a"                         # the fire bed: ash and coals
            _put(g, x, y, c)
    for (x, y) in [(5, 33), (9, 35), (22, 34), (26, 32), (7, 29), (24, 28)]:
        _put(g, x, y, "s")
    for (x, y, c) in [(4, 30, "f"), (5, 30, "F"), (6, 31, "f"), (25, 30, "F"), (26, 31, "f"),
                      (24, 31, "f"), (8, 34, "f"), (23, 35, "f"), (10, 36, "F"), (21, 36, "F")]:
        _put(g, x, y, c)
    # flames licking up round the cauldron
    for (x, y, c) in [(6, 27, "F"), (6, 26, "Y"), (5, 28, "f"), (7, 28, "F"), (25, 27, "F"), (25, 26, "Y"),
                      (24, 28, "F"), (26, 28, "f"), (11, 34, "Y"), (12, 34, "F"), (20, 34, "Y"), (19, 34, "F"),
                      (13, 35, "f"), (18, 35, "f"), (15, 36, "F"), (16, 36, "Y"), (14, 36, "f"), (17, 36, "f")]:
        _put(g, x, y, c)
    # the cauldron: a wide bronze bowl of barley soup, hung over the fire
    cx, cy = 15.5, 26.0
    for y in range(18, 35):
        for x in range(4, 28):
            dx, dy = (x - cx) / 11.5, (y - cy) / 8.0
            if dy < 0:
                r = dx * dx + (dy * 1.6) ** 2
            else:
                r = dx * dx + (dy * 1.0) ** 2
            if r > 1.0:
                continue
            rim = dx * dx + ((y - 21.5) / 3.6) ** 2
            if y <= 25 and rim <= 1.0:
                inner = dx * dx * 1.25 + ((y - 21.5) / 2.6) ** 2
                if inner <= 1.0:
                    c = "h" if (x + y) % 9 else "l"     # soup, a bubble or two
                elif rim > 0.82:
                    c = "k"
                else:
                    c = "n" if y < 21 else "b"
            elif r > 0.86:
                c = "k"
            else:
                c = "b" if dx < 0.3 and dy < 0.5 else "d"
                if dx < -0.55 and dy < 0.4:
                    c = "n"
            _put(g, x, y, c)
    for (x, y) in [(10, 22), (21, 23), (15, 21)]:
        _put(g, x, y, "c")
    _put(g, 15, 18, "k"); _put(g, 16, 18, "k")
    return _text(g)


stamp("hearth_chain", 2, 3, art=[("clay", _hearth_chain())],
      note="the garrison hearth: barley soup in a bronze cauldron on a chain from the beam, soot up the wall")

stamp("helmet_shelf", 2, 1, art=[("bronze", """
....rrrr........................
...rrfrrr.......................
...kkkkkk...........kkkkk.......
..kyYYYyyk.........kyYYyyk......
.kyYyyyyybk.......kyYyyyybk.....
.kyyyyyyybk.......kyyyyyybk.....
kyyyykkkbbzk.....kyyykkkbzk.....
kyyyk...kbzk.....kyyk...kzk.....
kybbk..kbbzk.....kybk..kbzk.....
.kbbzk.kbzk.......kbzk.kzk......
..kzzk..kk.........kzk..k.......
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kYyyyyyyyyyyyyyyyyyyyyyyyyyyyyyk
kzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
...kzk....................kzk...
""")], note="a shelf of bronze Corinthian helmets, the captain's with its red crest")


# ---- pass 2 (render critique): bigger garlands, cages, a grape basket ------

def _wreath(g, cx, cy, r, berries):
    import math as _m
    for a in range(0, 360, 12):
        t = _m.radians(a)
        x, y = int(round(cx + r * _m.cos(t))), int(round(cy + r * _m.sin(t)))
        for (dx, dy, c) in ((0, 0, "g"), (1, 0, "G"), (0, 1, "v" if a < 180 else "G")):
            if 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                g[y + dy][x + dx] = c
    for a in range(0, 360, 45):
        t = _m.radians(a + 20)
        x, y = int(round(cx + (r + 1) * _m.cos(t))), int(round(cy + (r + 1) * _m.sin(t)))
        if 0 <= y < len(g) and 0 <= x < len(g[0]):
            g[y][x] = "V"
    for (bx, by) in berries:
        g[by][bx] = "p"


def _garlands():
    g = [["."] * 16 for _ in range(32)]
    for y in range(4, 9):                       # the cord from the beam
        g[y][7] = "K"
        g[y][8] = "k"
    _wreath(g, 7.5, 14.0, 5.0, [(5, 18), (10, 18)])
    _wreath(g, 7.5, 25.0, 4.0, [(6, 28)])
    for y in (20, 21):
        g[y][7] = "K"
    return "\n".join("".join(r) for r in g)


del STAMPS["garlands"]
stamp("garlands", 1, 2, art=[("nature", _garlands())],
      note="ivy wreaths drying, one under another, hung from the beam")
