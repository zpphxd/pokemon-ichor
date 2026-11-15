"""The megaron tileset's furniture: every stamp megaron draws itself.

megaron_art.py holds the palettes, floors, walls and rug, and calls
define_pieces() with its own namespace, so the pieces here use its grid(),
stamp() and drawing helpers. Grouped by the room that first needed them;
most are shared by several rooms.
"""
import math


def define_pieces(ns):
    grid, stamp, recolor = ns["grid"], ns["stamp"], ns["recolor"]
    canvas, text, put, hline, vline, rect = (ns[k] for k in ("canvas", "text", "put", "hline", "vline", "rect"))
    paste, mirror, outline, hflip = ns["paste"], ns["mirror"], ns["outline"], ns["hflip"]
    O = ns["O"]
    np = ns["np"]

    def ellipse(g, cx, cy, rx, ry, c, only=None):
        """Fill an ellipse centered between pixels (cx, cy are pixel-edge coords)."""
        for y in range(len(g)):
            for x in range(len(g[0])):
                dx = (x + 0.5 - cx) / rx
                dy = (y + 0.5 - cy) / ry
                if dx * dx + dy * dy <= 1.0 and (only is None or g[y][x] in only):
                    g[y][x] = c

    def sym(g):
        """Mirror the left half of a canvas onto its right half."""
        W = len(g[0])
        for row in g:
            for x in range(W // 2):
                row[W - 1 - x] = row[x]
        return g

    # =======================================================================
    # Every room
    # =======================================================================

    stamp("mat", "nature", """
................
................
................
.kkkkkkkkkkkkkk.
.kJJJJJJJJJJJJk.
.kjKjjKjjKjjKjk.
.kKjjKjKKjKjjKk.
.kjjKjKjjKjKjjk.
.kjKjjKjjKjjKjk.
.kKjjKjKKjKjjKk.
.kjjKjKjjKjKjjk.
.kKKKKKKKKKKKKk.
.kkkkkkkkkkkkkk.
................
................
................
""", 1, 1, walk={(0, 0)}, behavior={(0, 0): "MB_SOUTH_ARROW_WARP"},
          note="the threshold mat: a reed mat at the door, a south-arrow warp")

    # The Minoan column the Trojans and Mycenaeans built: a cushion capital,
    # a red shaft wider at the top than the foot, a dark base. The capital
    # and shaft are drawn over walkers; only the base cell is solid.
    def column_art():
        g = canvas(16, 48)
        rect(g, 1, 1, 14, 3, "d")                        # abacus
        hline(g, 1, 14, 1, "m")
        for y, hw in zip(range(4, 9), (7, 7, 6, 6, 5)):   # cushion
            hline(g, 8 - hw, 7 + hw, y, "d")
            hline(g, 8 - hw, 8 - hw + 2, y, "m")
        hline(g, 3, 12, 9, "y")                          # bronze ring
        hline(g, 3, 4, 9, "b")
        for y in range(10, 42):
            hw = 5 if y < 22 else 4
            hline(g, 8 - hw, 7 + hw, y, "r")
            put(g, 8 - hw, y, "h" if y % 6 else "r")
            put(g, 9 - hw, y, "r")
            hline(g, 6 + hw, 7 + hw, y, "R")
        rect(g, 2, 42, 13, 44, "d")                      # base
        hline(g, 2, 13, 42, "m")
        rect(g, 1, 45, 14, 46, "d")
        g = outline(g)
        sym(g)
        art = [row[:] for row in g]
        top = [row[:] for row in g]
        for y in range(48):
            for x in range(16):
                if y < 32:
                    art[y][x] = "."
                else:
                    top[y][x] = "."
        return grid("wood", text(art), 16, 48), grid("wood", text(top), 16, 48)

    _col, _coltop = column_art()
    stamp("column", "wood", _col, 1, 3, top=_coltop, walk={(0, 0), (0, 1)},
          note="a Minoan column: red shaft tapering to its foot, black cushion capital; drawn over walkers but its base")

    # A counter shared by every Asclepeion and Agora: a cedar slab on a
    # painted front, red with linen roundels. Talk across it (MB_COUNTER).
    def counter(left, right):
        g = canvas(16, 16)
        rect(g, 0, 2, 15, 15, "m")
        hline(g, 0, 15, 2, "k")
        hline(g, 0, 15, 3, "h")
        hline(g, 0, 15, 4, "l")
        hline(g, 0, 15, 5, "d")
        rect(g, 0, 7, 15, 12, "r")
        hline(g, 0, 15, 7, "R")
        hline(g, 0, 15, 12, "R")
        for x in (3, 11):
            for (dx, dy) in ((0, 9), (1, 9), (-1, 10), (2, 10), (0, 10), (1, 10), (0, 11), (1, 11)):
                put(g, x + dx, dy, "c" if dy != 11 else "C")
            put(g, x, 9, "c")
        hline(g, 0, 15, 13, "d")
        hline(g, 0, 15, 15, "k")
        if left:
            vline(g, 0, 2, 15, "k")
            vline(g, 1, 3, 14, "l")
        if right:
            vline(g, 15, 2, 15, "k")
            vline(g, 14, 3, 14, "d")
        return grid("wood", text(g))

    for name, l, r in (("counter_l", True, False), ("counter_m", False, False), ("counter_r", False, True)):
        stamp(name, "wood", counter(l, r), 1, 1, behavior={(0, 0): "MB_COUNTER"},
              note="the counter: a cedar slab on a painted front; talk across it")

    # =======================================================================
    # The Asclepeions
    # =======================================================================

    # The sacred spring: a marble basin fed by a bronze lion's-head spout in
    # the wall. Where the heal animation sets the party's balls (the healer's
    # x-2..x-1, y-1..y), the balls land on its water.
    def basin_art():
        g = canvas(32, 32)
        lion = [  # a bronze lion's mask, the water from its mouth (left half)
            "....zzz.",
            "..zzbbbz",
            ".zbyyybb",
            "zbyYyyyb",
            "zbykyyyb",
            "zbyyyybb",
            ".zbyzzzz",
            "..zbzkkk",
            "...zzk..",
        ]
        for j, line in enumerate(lion):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, 8 + i, 1 + j, c)
        sym(g)
        g = outline(g)
        for y in range(10, 17):                          # the stream
            put(g, 15, y, "a"); put(g, 16, y, "U")
        ellipse(g, 16, 22, 15, 8, "M")                   # rim
        ellipse(g, 16, 22, 13, 6, "u")                   # water
        ellipse(g, 16, 21, 11, 4, "U", only="u")
        for (x, y) in ((9, 20), (10, 20), (21, 22), (22, 22), (14, 18), (17, 18)):
            put(g, x, y, "a")
        for y in range(23, 31):                          # bowl front, fluted
            for x in range(4, 28):
                if abs(x + 0.5 - 16) <= 12 - (y - 23) * 0.7 and g[y][x] == ".":
                    g[y][x] = "m" if x % 3 else "n"
        for x in range(4, 28):
            if g[30][x] != ".":
                g[30][x] = "n"
        g = outline(g)
        sym(g)
        return text(g)

    stamp("basin", "bronze", basin_art(), 2, 2,
          note="the sacred spring: a marble basin under a bronze lion's-head spout")

    stamp("rod", "wall", """
................
................
................
.....kkkkkk.....
....kooooook....
....koRRRRok....
....koRRwRok....
....koRowoRk....
....koRwoRok....
....koRowRok....
....koRRwoRk....
....koRowRok....
....koRwoRok....
....koRRwoRk....
....koRowRok....
....koRwoRok....
....koRRwoRk....
....koRowRok....
....koRwoRok....
....koRRwRok....
....koRRwRok....
....koRRwRok....
....koRRwRok....
....koRwwwok....
....koRRRRok....
....kooooook....
.....kkkkkk.....
................
................
................
................
................
""", 1, 2, note="a painted panel: the rod of Asclepius, a gold snake round a white staff")

    # The Pithos: the great storage jar of the Asclepeion (the PC).
    def great_pithos_art():
        g = canvas(32, 32)
        prof = [6, 7, 7, 9, 11, 12, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 12, 12, 11, 10, 9, 8, 7]
        for i, hw in enumerate(prof):
            y = 3 + i
            for x in range(16 - hw, 16):
                rel = (x - (16 - hw)) / max(1, hw)
                put(g, x, y, "h" if rel < 0.18 and 5 < i < 20 else "l" if rel < 0.45 else "m")
        for y in (9, 15, 21):                            # rope bands
            for x in range(1, 16):
                if g[y][x] != ".":
                    put(g, x, y, "d" if x % 2 else "m")
        rect(g, 10, 1, 15, 3, "S")                       # stone lid
        hline(g, 10, 15, 1, "t")
        rect(g, 13, 0, 15, 2, "f")                       # wax seal
        put(g, 14, 0, "F")
        g = outline(g)
        sym(g)
        for y in range(3, 29):                           # shadow side
            for x in range(16, 32):
                if g[y][x] == "l":
                    g[y][x] = "m"
                elif g[y][x] == "h":
                    g[y][x] = "l"
                elif g[y][x] == "m" and x > 24:
                    g[y][x] = "d"
        return text(g)

    stamp("great_pithos", "clay", great_pithos_art(), 2, 2,
          note="the Pithos: a great storage jar with rope bands and a wax seal (the PC)")

    # Sestos's harbor Asclepeion looks out on the strait.
    def sea_window_art():
        g = canvas(32, 32)
        rect(g, 2, 3, 29, 28, "p")                       # stone frame
        for y in range(3, 29):
            put(g, 2, y, "w"); put(g, 29, y, "S")
        hline(g, 2, 29, 3, "w")
        hline(g, 2, 29, 28, "S")
        rect(g, 5, 6, 26, 25, "a")                       # sky
        for x in range(5, 27):                           # the arch's corners
            for y in range(6, 9):
                if (x < 5 + (9 - y) * 1.5) or (x > 26 - (9 - y) * 1.5):
                    put(g, x, y, "p")
        rect(g, 5, 16, 26, 17, "o")                      # the far shore (Asia)
        for (x0, x1, y) in ((6, 11, 15), (8, 10, 14), (17, 24, 15), (19, 22, 14), (20, 21, 13)):
            hline(g, x0, x1, y, "R")
        rect(g, 5, 18, 26, 25, "b")                      # the strait
        for (x, y) in ((7, 19), (8, 19), (15, 21), (16, 21), (22, 20), (23, 20), (11, 23), (12, 23), (20, 24), (25, 22)):
            put(g, x, y, "w")
        for y in range(18, 26, 2):
            for x in range(5, 27):
                if g[y][x] == "b" and (x + y) % 5 == 0:
                    put(g, x, y, "B")
        vline(g, 14, 10, 18, "k")                        # a sail on the strait
        for y in range(10, 17):
            hline(g, 15, 15 + (y - 9) // 2, y, "w")
        hline(g, 12, 17, 18, "D")
        vline(g, 16, 6, 25, "S")                         # the mullion
        hline(g, 5, 26, 25, "S")
        rect(g, 4, 28, 27, 30, "s")                      # the sill
        hline(g, 4, 27, 28, "w")
        for y in range(2, 31):
            for x in range(1, 31):
                if g[y][x] != "." and (g[y - 1][x] == "." or g[y + 1][x] == "." or g[y][x - 1] == "." or g[y][x + 1] == "."):
                    pass
        g = outline(g)
        return text(g)

    stamp("sea_window", "wall", sea_window_art(), 2, 2,
          note="a broad window on the Hellespont: Asia's shore across the strait, a sail")

    # =======================================================================
    # The Agoras
    # =======================================================================

    stamp("goods", "wood", """
................................
..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..
..kdmmmmmmmmmmmmmmmmmmmmmmmmdk..
..kdk.kkk..kkkk...kkk...kkk.dk..
..kd.kyybk.kbyyk.kyybk.kbbzkdk..
..kd.kybzk.kbyzk.kybbk.kbzzkdk..
..kd.kbbzk.kzzzk.kbbzk.kkkkkdk..
..kd..kzk...kkk...kzk.......dk..
..kd.kbbzk.......kbbbk..kk..dk..
..kd.kkkkk.......kkkkk.kyyk.dk..
..kdkkkkkkkkkkkkkkkkkkkkkkkkdk..
..kdhhhhhhhhhhhhhhhhhhhhhhhhdk..
..kdlllllllllllllllllllllllldk..
..kdkkkkkkkkkkkkkkkkkkkkkkkkdk..
..kd..kkkk..kkkk...kkkkkk...dk..
..kd.kccCk.krrRk..kuuuuUk...dk..
..kd.kcCCk.krRRk..kuuUuUk...dk..
..kd.kCCCk.kkkkk..kuUuUuk.k.dk..
..kd.kkkkkkkkkkk..kkkkkkkkck.dk.
..kd..kccccCCCk...kcccCCCCk.dk..
..kd..kcCCCCCCk...kCCCCCCCk.dk..
..kd..kkkkkkkkk...kkkkkkkkk.dk..
..kdkkkkkkkkkkkkkkkkkkkkkkkkdk..
..kdhhhhhhhhhhhhhhhhhhhhhhhhdk..
..kdlllllllllllllllllllllllldk..
..kdkkkkkkkkkkkkkkkkkkkkkkkkdk..
..kdk......................kdk..
..kdk......................kdk..
..kkk......................kkk..
................................
................................
................................
""", 2, 2, note="a stall's shelves: bronze cups and flasks, bales of linen, red and blue boxes")

    def bolts_art():
        g = canvas(32, 32)
        rect(g, 2, 1, 29, 29, "n")                      # the cupboard
        rect(g, 4, 3, 27, 27, "k")
        bolts = [("R", "r"), ("i", "u"), ("o", "y"), ("p", "P"), ("C", "c"), ("R", "r"), ("u", "U"), ("p", "P")]
        k = 0
        for shelf_y in (3, 15):
            x = 4
            for _ in range(4):
                dark, lit = bolts[k % len(bolts)]
                k += 1
                for layer in range(3):
                    y0 = shelf_y + 1 + layer * 4
                    rect(g, x, y0, x + 5, y0 + 2, dark)
                    hline(g, x, x + 5, y0, lit)
                    put(g, x + 5, y0 + 1, "k")
                x += 6
            hline(g, 4, 27, shelf_y + 12, "C")
        hline(g, 2, 29, 1, "c")
        g = outline(g)
        return text(g)

    stamp("cloth_bolts", "cloth", bolts_art(), 2, 2,
          note="a cupboard of folded cloth: madder, indigo, saffron, purple and bleached linen")

    stamp("rope", "nature", """
................
................
................
................
.....kkkkkk.....
...kknnnnnnkk...
..knnKkkkkKnnk..
.knKkknnnnkkKnk.
.knKknkkkknKKnk.
.knKknkKKknKnnk.
.knKkknnnnkkKnk.
..knnKkkkkKnnk..
...kknnnnnnkk...
.....kkkkkk.....
................
................
""", 1, 1, note="a coil of rope")

    # =======================================================================
    # Hero's tower
    # =======================================================================

    def slit_art(ribbon):
        g = canvas(16, 32)
        rect(g, 4, 4, 11, 29, "S")                       # the splay
        rect(g, 5, 4, 10, 29, "s")
        rect(g, 6, 6, 9, 27, "a")                        # sky through the slit
        vline(g, 6, 6, 27, "B")
        hline(g, 6, 9, 6, "k")
        hline(g, 4, 11, 29, "w")
        for y in range(4, 30):
            put(g, 3, y, "k"); put(g, 12, y, "k")
        hline(g, 3, 12, 3, "k")
        if ribbon:   # a red ribbon tied to the bar, streaming into the room
            pts = [(9, 8), (10, 9), (10, 10), (11, 11), (12, 12), (12, 13), (13, 14), (13, 15),
                   (14, 16), (14, 17), (13, 18), (14, 19)]
            for i, (x, y) in enumerate(pts):
                put(g, x, y, "r" if i % 3 else "R")
                put(g, x - 1, y + 1, "D" if i % 2 else "R")
            hline(g, 6, 9, 8, "D")
        return text(g)

    stamp("slit", "wall", slit_art(False), 1, 2, note="an arrow slit in the tower wall, sky beyond")

    stamp("draught", "wall", """
................
................
..ww............
....wwww........
........ww......
..........w.....
....ww.....w....
......www..w....
.........ww.....
................
..www...........
.....wwwww......
..........ww....
............w...
................
................
""", 1, 1, walk={(0, 0)}, note="the draught's breath on the floor, in front of a draughty slit; walkable")
    stamp("slit_draught", "wall", slit_art(True), 1, 2,
          note="a draughty slit: a red ribbon on its bar streams into the room. A carried flame dies in front of it")

    def stair_art():
        g = canvas(16, 32)
        rect(g, 0, 0, 15, 31, "S")
        rect(g, 1, 0, 14, 9, "k")                        # the dark stairwell
        for i, y in enumerate(range(10, 32, 4)):         # treads, coming up out of the dark
            lit = "s" if i < 1 else "p"
            hline(g, 2, 13, y, "w" if i > 0 else "S")
            hline(g, 2, 13, y + 1, lit)
            hline(g, 2, 13, y + 2, lit)
            hline(g, 2, 13, y + 3, "S" if i > 0 else "k")
        for y in range(0, 32):
            put(g, 1, y, "k"); put(g, 14, y, "k")
            put(g, 0, y, "s"); put(g, 15, y, "S")
        for y in range(4, 10, 3):                        # faint treads in the dark
            hline(g, 3, 12, y, "1")
        return text(g)

    stamp("stair", "wall", stair_art(), 1, 2, walk={(0, 0), (0, 1)},
          note="stone stairs climbing north into the wall to the floor above")

    def great_lamp_art(lit):
        g = canvas(32, 32)
        ellipse(g, 16, 9, 10, 8, "z")                    # the bronze reflector
        ellipse(g, 16, 9, 8, 6, "b" if not lit else "Y")
        ellipse(g, 16, 9, 5, 4, "y" if not lit else "e")
        if lit:
            for (x, y) in ((15, 3), (16, 3), (14, 5), (17, 5)):
                put(g, x, y, "Y")
        rect(g, 7, 17, 24, 18, "y")                      # the bowl's rim
        for y in range(19, 23):
            hw = 9 - (y - 19) * 2
            hline(g, 16 - hw, 15 + hw, y, "b")
            put(g, 16 - hw, y, "y")
        hline(g, 11, 20, 22, "z")
        rect(g, 9, 23, 22, 30, "m")                      # the marble plinth
        hline(g, 9, 22, 23, "M")
        vline(g, 9, 24, 30, "M")
        hline(g, 9, 22, 30, "n")
        if lit:                                           # the flame
            flame = [
                "......e.......",
                ".....eFe......",
                ".....eFFe.....",
                "....eFfFe.....",
                "...eFFfFFe....",
                "...eFffFFe....",
                "..eFFffFFFe...",
                "..eFfffFfFe...",
                "...eFfffFe....",
                "....eeeeee....",
            ]
            for j, line in enumerate(flame):
                for i, c in enumerate(line):
                    if c != ".":
                        put(g, 9 + i, 7 + j, c)
        else:
            vline(g, 16, 14, 16, "k")                    # a cold wick
        g = outline(g)
        sym(g)
        return text(g)

    stamp("great_lamp", "bronze", great_lamp_art(False), 2, 2,
          note="Hero's great lamp: a bronze bowl on a marble plinth before a polished reflector, cold")
    stamp("great_lamp_lit", "bronze", great_lamp_art(True), 2, 2,
          note="the great lamp, lit: the flame Leander swims by")

    def brazier_art():
        g = canvas(16, 32)
        flame = [
            ".....e....",
            "....eFe...",
            "...eFFe...",
            "...eFfFe..",
            "..eFfffFe.",
            "..eFfFffe.",
            ".eFffFfFe.",
            ".eFfffffFe",
            "..eeeeeee.",
        ]
        for j, line in enumerate(flame):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, 3 + i, 4 + j, c)
        rect(g, 2, 13, 13, 14, "y")                      # the bowl
        rect(g, 3, 15, 12, 16, "b")
        rect(g, 5, 17, 10, 17, "z")
        for y in range(18, 30):                          # three legs
            put(g, 4 - (y - 18) // 5, y, "b")
            put(g, 7, y, "y"); put(g, 8, y, "b")
        for y in range(27, 31):
            put(g, 3, y, "z")
        g = outline(g)
        sym(g)
        return text(g)

    stamp("brazier", "bronze", brazier_art(), 1, 2, note="a bronze tripod brazier, burning")

    stamp("oil_jar", "clay", """
................
................
................
................
......kkkk......
.....kSttSk.....
......kssk......
....kkmmmmkk....
...kmlhllllmk...
..kmlhlllllmdk..
..kmllllllmmdk..
..kmlllllmmmdk..
..kdmmmmmmmddk..
...kdmmmmmmdk...
....kkddddkk....
.....kkkkkk.....
""", 1, 1, note="a squat jar of lamp oil, stoppered")

    stamp("amphora_grey", "clay",
          recolor(O.STAMPS["amphora_plain"]["img"], "clay", {"m": "S", "l": "t", "h": "c", "d": "s"}), 1, 2,
          note="a Trojan grey-ware amphora, burnished like pewter")

    # =======================================================================
    # Sestos's homes
    # =======================================================================

    def net_rack_art():
        g = canvas(32, 32)
        for (x0, x1) in ((3, 6), (25, 28)):             # the A-frame legs
            for y in range(4, 31):
                t = (y - 4) / 26
                put(g, int(round(x0 + (x1 - x0) * t * (1 if x0 < 16 else -1) + (0 if x0 < 16 else 3))), y, "K")
        for x in (4, 27):
            vline(g, x, 3, 30, "K")
            vline(g, x + (1 if x < 16 else -1), 3, 30, "j")
        hline(g, 2, 29, 4, "K")                          # the top pole
        hline(g, 2, 29, 3, "J")
        for x in range(6, 26):                           # the net, sagging
            t = (x - 6) / 19
            bottom = int(round(8 + 14 * math.sin(math.pi * t)))
            for y in range(5, bottom):
                if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                    put(g, x, y, "n")
            put(g, x, bottom, "K")
        for x in range(7, 26, 4):                        # cork floats on the head rope
            rect(g, x, 5, x + 1, 6, "J")
            put(g, x + 1, 6, "j")
        g = outline(g)
        return text(g)

    stamp("net_rack", "nature", net_rack_art(), 2, 2,
          note="a drying rack: a net hung over a pole between two A-frames, cork floats on its head rope")

    stamp("floats", "nature", """
................
................
................
................
.......kk.......
......kKKk......
.....kKkkKk.....
....kn....nk....
...kJjk..kJjk...
...kjjk..kjjk...
....kk....kk....
...kn......nk...
..kJjk....kJjk..
..kjjk....kjjk..
...kk......kk...
...kn......nk...
..kJjk....kJjk..
..kjjk....kjjk..
...kkn....nkk...
.....nnnnnn.....
....knnnnnnk....
...knKnnnnKnk...
...knnKKKKnnk...
....knnnnnnk....
.....kkkkkk.....
................
................
................
................
................
................
................
""", 1, 2, note="strings of cork floats on a peg, a hank of line under them")

    stamp("wreath", "nature", """
................
................
................
................
................
................
................
.......kk.......
.......KK.......
.....kkkkkk.....
...kkgvgvgGkk...
..kgvGk..kgGvk..
.kvGk......kGgk.
.kgk........kvk.
.kGk........kgk.
.kvgk......kGvk.
..kGvk....kvGk..
...kgvGkkgGvk...
....kkpkkpkk....
.....kp..pk.....
.....kp..pk.....
......k..k......
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
""", 1, 2, note="an olive wreath on a peg: the ferryman's prize for swimming the strait as a boy")

    # =======================================================================
    # Priam's palace
    # =======================================================================

    def horse(g, x, y, body, mane):
        """A galloping horse in the Aegean manner, 15x10, facing right."""
        shape = [
            "...........mm..",
            "..........mBBb.",
            ".........mBBBBe",
            "........mBBB.BB",
            ".BBBBBBBBBB....",
            "BBBBBBBBBBB....",
            "BBBBBBBBBBB....",
            ".B.BB...BB.B...",
            "B...B...B...B..",
            "B....B.B.....B.",
        ]
        for j, line in enumerate(shape):
            for i, c in enumerate(line):
                if c == "B":
                    put(g, x + i, y + j, body)
                elif c in "mb":
                    put(g, x + i, y + j, mane)
                elif c == "e":
                    put(g, x + i, y + j, "k")

    def horse_fresco_art():
        g = canvas(32, 32)
        rect(g, 1, 3, 30, 27, "p")                       # the panel
        hline(g, 1, 30, 3, "o"); hline(g, 1, 30, 27, "o")
        for x in range(1, 31):                           # running spirals, top and foot
            put(g, x, 4, "r" if x % 4 < 2 else "p")
            put(g, x, 26, "b" if x % 4 < 2 else "p")
        hline(g, 1, 30, 5, "R"); hline(g, 1, 30, 25, "R")
        horse(g, 3, 9, "R", "D")                         # a bay
        horse(g, 14, 14, "w", "S")                       # a white
        for (x, y) in ((24, 8), (25, 8), (26, 9), (2, 21), (3, 21)):
            put(g, x, y, "o")                            # flowers in the field
        g = outline(g)
        return text(g)

    stamp("horse_fresco", "wall", horse_fresco_art(), 2, 2,
          note="a fresco of two horses at the gallop, a bay and a white: Troy of the fine horses")

    def throne_art():
        g = canvas(16, 32)
        rect(g, 2, 2, 13, 18, "m")                       # the high back
        rect(g, 3, 3, 12, 17, "l")
        rect(g, 4, 5, 11, 15, "r")                       # red cloth on the back
        for (x, y) in ((6, 7), (9, 7), (7, 10), (8, 10), (6, 13), (9, 13)):
            put(g, x, y, "y")
        hline(g, 2, 13, 2, "y")
        rect(g, 6, 0, 9, 1, "y")                         # a bronze finial
        rect(g, 1, 18, 14, 22, "d")                      # the seat
        hline(g, 1, 14, 18, "h")
        rect(g, 2, 19, 13, 20, "r")
        for y in range(23, 31):                          # lion legs
            put(g, 2, y, "d"); put(g, 3, y, "m")
            put(g, 12, y, "m"); put(g, 13, y, "d")
        hline(g, 1, 4, 30, "b"); hline(g, 11, 14, 30, "b")
        g = outline(g)
        sym(g)
        return text(g)

    stamp("throne", "wood", throne_art(), 1, 2, note="Priam's throne: a high cedar back hung with red, bronze-shod feet")

    def round_hearth_art():
        g = canvas(32, 32)
        ellipse(g, 16, 20, 15, 10, "c")                  # painted stucco rim
        for y in range(len(g)):
            for x in range(len(g[0])):
                dx, dy = (x + 0.5 - 16) / 15, (y + 0.5 - 20) / 10
                r = dx * dx + dy * dy
                if r <= 1:
                    ang = math.atan2(dy, dx)
                    if 0.62 < r and int((ang + math.pi) / (2 * math.pi) * 20) % 2 == 0:
                        g[y][x] = "f"                    # the painted flame band
                    if r <= 0.45:
                        g[y][x] = "s"                    # the hearth's bed
                    if r <= 0.22:
                        g[y][x] = "a"
        for (x, y) in ((12, 20), (13, 21), (19, 20), (18, 21), (16, 22), (15, 19), (17, 19)):
            put(g, x, y, "F")                            # coals
        flame = [
            ".....Y.......",
            "....YFY..Y...",
            "....FfF.YFY..",
            "...YFfFYFfF..",
            "..YFffFFfFFY.",
            "..FffffffFfF.",
            ".YFfffffffFFY",
            ".FFFfffffFFF.",
        ]
        for j, line in enumerate(flame):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, 10 + i, 10 + j, c)
        for y in range(29, 31):
            for x in range(4, 28):
                if g[y][x] == "c":
                    g[y][x] = "m"
        g = outline(g)
        return text(g)

    stamp("round_hearth", "clay", round_hearth_art(), 2, 2,
          note="the megaron's great round hearth: a painted stucco rim, the fire never out")

    # =======================================================================
    # Cassandra's room
    # =======================================================================

    def fresco_troy_art():
        g = canvas(32, 32)
        rect(g, 1, 3, 30, 28, "S")
        rect(g, 2, 4, 29, 27, "b")                       # a night sky
        for y in range(4, 12):
            for x in range(2, 30):
                if (x * 7 + y * 3) % 11 == 0:
                    put(g, x, y, "B")
        rect(g, 2, 20, 29, 27, "S")                      # the walls of the city
        hline(g, 2, 29, 20, "s")
        for x in range(2, 30, 3):
            put(g, x, 19, "S")
        for (x0, x1, y0) in ((3, 7, 14), (11, 16, 11), (21, 25, 15)):   # towers
            rect(g, x0, y0, x1, 26, "S")
            vline(g, x0, y0, 26, "s")
            for x in range(x0, x1 + 1, 2):
                put(g, x, y0 - 1, "S")
            rect(g, x0 + 2, y0 + 3, x0 + 2, y0 + 4, "o")  # a lit window
        flames = [  # fire over the towers: tongues of red with ochre hearts
            (5, 13, 4), (13, 10, 5), (23, 14, 4), (9, 18, 3), (18, 18, 3), (27, 18, 3),
        ]
        for (cx, top, h) in flames:
            for i in range(h + 2):
                y = top - i
                w = max(0, (h + 1 - i) // 2)
                hline(g, cx - w, cx + w, y, "r")
                if i < h - 1:
                    hline(g, cx - max(0, w - 1), cx + max(0, w - 1), y, "o")
            put(g, cx, top - h - 2, "r")
        for (x, y) in ((4, 6), (5, 5), (6, 6), (12, 4), (13, 5), (14, 4), (15, 5), (22, 7), (23, 6), (24, 7)):
            put(g, x, y, "k")                            # smoke
        for y in range(4, 28):                           # half of it whitewashed over
            edge = 17 + int(round(2.5 * math.sin(y * 0.8)))
            for x in range(edge, 30):
                g[y][x] = "w" if (x * 3 + y) % 7 else "p"
            put(g, edge, y, "p")
        for (x, y) in ((20, 28), (20, 29), (24, 28), (27, 28), (27, 29), (27, 30)):
            put(g, x, y, "w")                            # drips under the brush
        g = outline(g)
        return text(g)

    stamp("fresco_troy", "wall", fresco_troy_art(), 2, 2,
          note="Cassandra's painting of Troy burning, half whitewashed over in fresh, uneven strokes")

    def tripod_art():
        g = canvas(16, 32)
        rect(g, 2, 8, 13, 9, "y")                        # the cauldron
        for y in range(10, 15):
            hw = 6 - (y - 10) // 2
            hline(g, 8 - hw, 7 + hw, y, "b")
            put(g, 8 - hw, y, "y")
        for (x, y) in ((2, 5), (3, 4), (4, 4), (5, 5), (5, 6), (2, 6)):
            put(g, x, y, "y")                            # ring handles
        for y in range(15, 31):                          # tall legs
            put(g, 3 + (y - 15) // 8 * -1 + 1, y, "z")
            put(g, 7, y, "b"); put(g, 8, y, "z")
        hline(g, 2, 13, 22, "z")
        g = outline(g)
        sym(g)
        return text(g)

    stamp("tripod", "bronze", tripod_art(), 1, 2, note="a bronze tripod of Apollo's, cold")

    def laurel_art():
        g = canvas(16, 32)
        rng = [(8, 3), (6, 5), (10, 5), (5, 8), (11, 8), (7, 10), (9, 10), (4, 12), (12, 12), (6, 14), (10, 14),
               (8, 7), (8, 12), (5, 16), (11, 16), (8, 16), (7, 18), (9, 18)]
        for i, (x, y) in enumerate(rng):              # pointed leaves
            for (dx, dy, c) in ((0, 0, "g"), (0, -1, "v"), (1, 0, "G"), (-1, 1, "g"), (0, 1, "G"), (1, -1, "v")):
                put(g, x + dx, y + dy, c if i % 3 else ("V" if c == "v" else c))
        vline(g, 8, 19, 22, "K")
        rect(g, 4, 22, 11, 29, "m")                      # the pot
        hline(g, 3, 12, 22, "d"); hline(g, 3, 12, 23, "m")
        vline(g, 10, 24, 29, "d"); vline(g, 11, 24, 29, "d")
        g = outline(g)
        return text(g)

    stamp("laurel", "nature", laurel_art(), 1, 2, note="a potted laurel, Apollo's tree, a little neglected")

    # =======================================================================
    # The pilgrims' guest-room
    # =======================================================================

    def louter_art():
        g = canvas(16, 32)
        ellipse(g, 8, 11, 7.5, 4, "y")                   # the basin
        ellipse(g, 8, 10.5, 6, 2.5, "U")
        ellipse(g, 8, 10, 4, 1.5, "a", only="U")
        for y in range(13, 16):
            hline(g, 3 + (y - 13), 12 - (y - 13), y, "b")
        rect(g, 6, 16, 9, 27, "m")                       # the fluted stand
        for y in range(16, 28):
            put(g, 6, y, "M"); put(g, 9, y, "n")
        rect(g, 4, 27, 11, 29, "m")
        hline(g, 4, 11, 27, "M")
        hline(g, 4, 11, 29, "n")
        g = outline(g)
        sym(g)
        return text(g)

    stamp("louter", "bronze", louter_art(), 1, 2,
          note="a bronze basin on a marble stand: a guest's feet are washed before anything else")

    stamp("krater", "clay", """
................
................
................
..kkkkkkkkkkkk..
.kllllllllllllk.
kk.kmmmmmmmmk.kk
kmk.kmllllmk.kmk
.kkkmlhlllllkkk.
...kmhkkkklldk..
...kmkllklkldk..
...kmlkkkkkldk..
....kmllllldk...
.....kdmmmdk....
......kkmkk.....
.....kmmmmdk....
.....kkkkkkk....
""", 1, 1, note="a mixing krater of wine, black-figure, for whoever comes in from the road")

    stamp("horse_toy", "wood", """
................
................
................
..........kk....
.........kmdk...
........kllmdk..
........klkmdk..
...kkkkklllmk...
..khllllllmmk...
..klllllllmmk...
..kmmmmmmmmdk...
...kmk...kmk....
..kkkkkkkkkkkk..
..kbklmmmmmkbk..
...kk.kkkk.kk...
................
""", 1, 1, note="a little wooden horse on wheels, half whittled, shavings round it")

    # =======================================================================
    # The horse-breeder's stable
    # =======================================================================

    def stall_art():
        """A stall partition running out from the back wall: the planks' lit top
        edge, their face in shadow with the board joints, a post at each end
        with a bronze tethering ring."""
        g = canvas(16, 32)
        rect(g, 4, 3, 11, 29, "m")                       # the plank wall
        for y in range(3, 30):
            hline(g, 4, 6, y, "l")                       # its top edge, lit
            put(g, 7, y, "h")
            put(g, 11, y, "d")
            if y % 5 == 0:
                hline(g, 8, 10, y, "d")                  # board joints on the face
        rect(g, 3, 0, 12, 4, "d")                        # the head post
        rect(g, 4, 1, 11, 3, "l")
        hline(g, 4, 11, 1, "h")
        rect(g, 3, 26, 12, 31, "d")                      # the foot post
        rect(g, 4, 27, 11, 30, "m")
        hline(g, 4, 11, 27, "l")
        for (x, y, c) in ((9, 14, "y"), (10, 15, "b"), (9, 16, "y"), (8, 15, "b")):
            put(g, x, y, c)                              # a tethering ring
        g = outline(g)
        return text(g)

    stamp("stall", "wood", stall_art(), 1, 2, note="a stall partition: cedar planks between two posts")

    def hay_rack_art():
        g = canvas(32, 32)
        rect(g, 2, 8, 29, 9, "K")                        # the rack's top rail
        rect(g, 4, 26, 27, 27, "K")                      # bottom rail
        for x in range(4, 28, 3):                        # slats, sloping out
            for y in range(10, 26):
                put(g, x - (25 - y) // 6, y, "K")
        for y in range(4, 24):                           # hay piled in it
            for x in range(4, 28):
                if g[y][x] == "." and (y > 8 or abs(x - 16) < 10 - (8 - y) * 2):
                    g[y][x] = "J" if (x * 3 + y) % 5 else "j"
        for (x, y) in ((6, 3), (9, 2), (14, 1), (20, 2), (24, 3), (11, 4), (18, 3)):
            put(g, x, y, "J")
        sym(g)
        g = outline(g)
        return text(g)

    stamp("hay_rack", "nature", hay_rack_art(), 2, 2, note="a hay rack on the wall, piled high")

    def trough_art():
        g = canvas(32, 16)
        rect(g, 1, 3, 30, 13, "m")
        hline(g, 1, 30, 3, "M")
        rect(g, 3, 5, 28, 8, "u")
        hline(g, 3, 28, 5, "U")
        for x in (8, 9, 20, 21):
            put(g, x, 6, "a")
        for y in range(9, 14):
            for x in range(1, 31):
                if x % 6 == 0:
                    put(g, x, y, "n")
        hline(g, 1, 30, 13, "n")
        g = outline(g)
        sym(g)
        return text(g)

    stamp("trough", "bronze", trough_art(), 2, 1, note="a stone water trough")

    stamp("straw", "nature", """
................
................
.......J........
....J..jJ.......
..J.jJJjJJ..J...
...jJjJJjJJj....
..JJjJjJJjJjJ...
.jJjJJjjJJjJjj..
..jJjjJJjJjJJ.J.
.J.JjJjjJJjj....
...jJJjJjJj.J...
....j.JjJ.j.....
.......J........
................
................
................
""", 1, 1, walk={(0, 0)}, note="a heap of clean straw on the floor; walkable")

    stamp("bridles", "wood", """
................
................
................
................
................
..kkkkkkkkkkkk..
..kddddddddddk..
..kkkkkkkkkkkk..
...kbk....kbk...
...kmk....kmk...
..kmkmk..kmkmk..
.kmk.kmkkmk.kmk.
.kdk..kdkdk..kdk
.kdk..kdkdk..kdk
.kmk..kmkmk..kmk
.kdk..kdkdk..kdk
.kmk..kmkmk..kmk
..kmkkmk.kmkkmk.
..kybbyk.kybbyk.
..kbkkbk.kbkkbk.
...kk.kk..kk.kk.
....krk....krk..
....krk....krk..
....kRk....kRk..
.....k......k...
................
................
................
................
................
................
................
""", 1, 2, note="two bridles on a peg-board, bronze bits and red tassels")

    stamp("wheel", "wood", """
................
.....kkkkkk.....
...kkmllllmkk...
..kmlkkkkkkdmk..
.kmlk..kk..kdmk.
.klk...kk...kdk.
kmlk...kk...kdmk
kmlkkkkbbkkkkdmk
kmlkkkkbbkkkkdmk
kmlk...kk...kdmk
.kmk...kk...kdk.
.kmmk..kk..kddk.
..kmmkkkkkkddk..
...kkmmmmddkk...
.....kkkkkk.....
................
""", 1, 1, note="a chariot wheel, four-spoked, waiting for a new rim")

    # =======================================================================
    # The mason's house
    # =======================================================================

    stamp("drum", "clay", """
................
....kkkkkkkk....
..kkcccccccckk..
.kcccccccccccck.
.kccccckkcccctk.
.ktcccccccccctk.
..kktttttttkk...
.kcScSccScScSck.
.kcScSccScScStk.
.kcScSccScScStk.
.kcScSccScScStk.
.kcScSccScScStk.
.ktSttSttSttSsk.
..kkssssssssk...
....kkkkkkkk....
................
""", 1, 1, note="a column drum of white limestone, fluted, the dowel hole cut in its top")

    stamp("capital", "clay", """
................
.kkkkkkkkkkkkkk.
.kcccccccccccck.
.kcccccccccccck.
.kttttttttttttk.
.kkkkkkkkkkkkkk.
..kccccccccctk..
...kccccccctk...
....kkttttkk....
....kStStsSk....
...kSsSsSsSsk...
...kssssssssk.k.
...kkkkkkkkkkks.
.s..........s...
................
................
""", 1, 1, note="a capital half carved: the abacus and echinus true, the neck still rough, chips round it")

    stamp("block", "clay", """
................
................
................
..kkkkkkkkkkkk..
.kcccccccccctk..
.kctttttttttSk..
.kckkkkkkkkkSk..
.ktSSSSSSSSSsk..
.ktSSkSSSkSSsk..
.ktSSSkSkSSSsk..
.ktSSSSkSSSSsk..
.ktSSSSSSSSSsk..
.ksssssssssssk..
.kkkkkkkkkkkkk..
................
................
""", 1, 1, note="a squared block, the family's mark cut in its face")

    stamp("workbench", "wood", """
................................
................................
..........kk..........kkkk......
.........kmdk........kyyyyk.....
....kkkkkkmdkk.......kyk........
...kbbbbbkdkmdk......kyk..kk....
...kkkkkkkk.kk.......kkk.kyyk...
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.khhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
.kllllllllllllllllllllllllllllk.
.kmmmmmmmmmmmmmmmmmmmmmmmmmmmmk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
..kmk.....................kbk...
..kdk.....................kyk...
..kdk......................k....
..kkk...........................
""", 2, 1, note="the workbench: a mallet, a chisel, a square and a plumb bob over the edge")

    stamp("tools", "wood", """
................
................
................
................
..kkkkkkkkkkkk..
..kddddddddddk..
..kkkkkkkkkkkk..
..kyk..kmk..k...
..kyk.kmmmk.kk..
..kyk.kmdmk.kbk.
..kyk..kmk..kbk.
..kyyyyk.k..kbk.
..kyyyyk.k..kbk.
..kkkkk.kdk.kbk.
........kdk.kyk.
........kdk.kyk.
........kdk..k..
........kkk.....
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
................
""", 1, 2, note="the mason's tools on a peg-board: a bronze square, a mallet, a long chisel")

    # =======================================================================
    # The peplos-weaver's house
    # =======================================================================

    def loom_art():
        g = canvas(32, 48)
        for x in (2, 3, 28, 29):                         # the uprights
            vline(g, x, 2, 46, "m" if x in (3, 28) else "d")
        rect(g, 1, 2, 30, 4, "l")                        # the cloth beam
        hline(g, 1, 30, 2, "h"); hline(g, 1, 30, 4, "d")
        rect(g, 5, 5, 26, 30, "y")                       # the peplos, saffron
        for y in range(5, 31):
            put(g, 5, y, "b"); put(g, 26, y, "b")
        for x in range(5, 27):                           # its border: a red meander
            put(g, x, 6, "r" if x % 4 < 2 else "b")
            put(g, x, 29, "r" if x % 4 < 2 else "b")
        figs = [  # a god and a giant fighting, woven in red
            "....RR..........RR....",
            "....RR..........RR....",
            "...RrrR........RrrR...",
            "..R.rr.RR....RR.rr.R..",
            "....rr....RR....rr....",
            "...R..R........R..R...",
            "..R....R......R....R..",
        ]
        for j, line in enumerate(figs):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, 5 + i, 12 + j, c)
        for y in range(21, 26):                          # a band of rosettes
            for x in range(7, 25, 4):
                if (y - 21) in (1, 3) and True:
                    put(g, x, y, "R")
                if (y - 21) == 2:
                    put(g, x - 1, y, "R"); put(g, x + 1, y, "R")
        hline(g, 5, 26, 31, "C")                         # the shed rod
        for x in range(6, 26):                           # the warp, hanging free
            if x % 2 == 0:
                vline(g, x, 32, 38, "c")
        hline(g, 4, 27, 35, "d")                         # the heddle bar
        for x in range(6, 26, 3):                        # loom weights
            rect(g, x, 39, x + 1, 42, "m")
            put(g, x, 39, "l")
        g = outline(g)
        return text(g)

    stamp("loom_big", "wood", loom_art(), 2, 3,
          note="the upright loom: Athena's saffron peplos, a god and a giant woven in red, the weights swinging")

    stamp("dye_vats", "cloth", """
................................
................................
................................
................................
..kkkkkkk..kkkkkkk..kkkkkkk.....
.kRrrrrrRkkiuuuuuikkoyyyyyok....
.knRRRRRnkkniiiiinkknoooooonk.k.
.knnnnnnnkknnnnnnnkknnnnnnnkknk.
.kCnnnnnnkkCnnnnnnkkCnnnnnnkknk.
.kCnnnnnnkkCnnnnnnkkCnnnnnnkknk.
..kCnnnnk..kCnnnnk..kCnnnnkkknk.
..kCnnnnk..kCnnnnk..kCnnnnk.knk.
...kkkkk....kkkkk....kkkkk..kk..
................................
................................
................................
""", 2, 1, note="three dye pots: madder, woad and weld, and the stirring stick")

    stamp("skeins", "cloth", """
................
................
................
................
................
..kkkkkkkkkkkk..
..knnnnnnnnnnk..
..kkkkkkkkkkkk..
..kRk.kik.kok...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
.kRrkkiukkoyk...
..kRk.kik.kok...
..kRk.kik.kok...
...k...k...k....
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
""", 1, 2, note="skeins of dyed wool drying on a peg: madder, woad and weld")

    # =======================================================================
    # The temple of Athena
    # =======================================================================

    def palladion_art():
        g = canvas(16, 48)
        # the image: archaic and stiff, dark old wood, a spear raised in the
        # right hand and a round shield on the left arm, a gleam on its helmet
        fig = [
            "......kkkk......",
            ".....kyYyyk..k..",
            ".....kzbbzk.kYk.",
            ".....kzkkzk.kyk.",
            ".....kzzzzk.kyk.",
            "......kzzk..kyk.",
            "...kkkzzzzkkkyk.",
            "..kYyykzzzzzzbk.",
            ".kYybyykzzzzkbk.",
            ".kyykbyyzzzzk.k.",
            ".kyybyykzzzzk...",
            ".kbyyybkzzzzk...",
            "..kbbbkzzzzzk...",
            "...kkkkzzzzzk...",
            "......kzzzzzk...",
            "......kzzkzzk...",
            ".....kzzzkzzzk..",
            ".....kzzzkzzzk..",
            ".....kkkkkkkkk..",
        ]
        for j, line in enumerate(fig):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, i, 2 + j, c)
        for (x, y) in ((2, 3), (13, 1), (1, 14), (15, 17), (3, 19)):
            put(g, x, y, "e")                            # a faint hum of light, new
        rect(g, 3, 21, 12, 46, "m")                      # the pedestal
        rect(g, 2, 21, 13, 23, "M")
        hline(g, 2, 13, 23, "n")
        for y in range(24, 44):
            put(g, 3, y, "M"); put(g, 12, y, "n")
        rect(g, 2, 43, 13, 46, "M")
        hline(g, 2, 13, 46, "n")
        rect(g, 5, 28, 10, 37, "n")                      # a carved owl
        for (x, y) in ((6, 30), (9, 30)):
            put(g, x, y, "Y")
        hline(g, 7, 8, 32, "z")
        g = outline(g)
        return text(g)

    stamp("palladion", "bronze", palladion_art(), 1, 3,
          note="the Palladion: a small dark image of Pallas, spear raised, that fell from the sky, on a tall pedestal")

    def temple_altar_art():
        g = canvas(32, 16)
        rect(g, 3, 4, 28, 14, "m")
        rect(g, 2, 4, 29, 6, "M")
        for x in (2, 3, 28, 29):                         # the horns
            put(g, x, 2, "M"); put(g, x, 3, "M")
        rect(g, 3, 8, 28, 9, "r")                        # the red fillet
        for x in range(4, 28, 4):
            put(g, x, 10, "r"); put(g, x, 11, "r")
        hline(g, 3, 28, 14, "n")
        for (x, y, c) in ((15, 0, "e"), (16, 0, "e"), (14, 1, "F"), (15, 1, "f"), (16, 1, "f"), (17, 1, "F"),
                          (14, 2, "F"), (15, 2, "F"), (16, 2, "F"), (17, 2, "F"), (13, 3, "z"), (18, 3, "z")):
            put(g, x, y, c)
        g = outline(g)
        sym(g)
        return text(g)

    stamp("temple_altar", "bronze", temple_altar_art(), 2, 1,
          note="a horned marble altar bound with a red fillet, a small flame on it")

    def shield_art():
        g = canvas(16, 32)
        vline(g, 8, 2, 4, "k")                           # the peg
        ellipse(g, 8, 15, 7, 8, "z")
        ellipse(g, 8, 15, 6, 7, "b")
        ellipse(g, 8, 14, 5, 6, "y")
        owl = [  # Athena's owl as the blazon
            ".kk.kk.",
            "kzkkkzk",
            "kYzkzYk",
            ".kzzzk.",
            ".kzzzk.",
            "..kzk..",
        ]
        for j, line in enumerate(owl):
            for i, c in enumerate(line):
                if c != ".":
                    put(g, 5 + i, 11 + j, c)
        g = outline(g)
        return text(g)

    stamp("shield", "bronze", shield_art(), 1, 2,
          note="a votive shield hung on the wall, Athena's owl for its blazon")
