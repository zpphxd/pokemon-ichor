#!/usr/bin/env python3
"""Lebadeia's pieces: the pilgrims' hall cut into the rock, Herkyna's round
river house with the mill-race through it, and Agamedes the mason's
workroom. Registered into westrooms_art.STAMPS on import."""
from westrooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, noise, Canvas, OA  # noqa: F401

# ---- the pilgrims' hall ------------------------------------------------------


def _votives(seed, new=False):
    """Small wooden tablets hung on pegs in rows over the rock, each a
    pilgrim's account of what they saw below. 1x2 on the wall: three rows of
    tablets, each on its own peg and string, a little crooked, some darkened
    with age. new: the newest, pale fresh wood, all cut alike."""
    c = Canvas(16, 32)
    for ri, y0 in enumerate((3, 12, 21)):
        x = (ri * 3 + seed) % 4
        n = 0
        while x + 5 <= 16:
            w = 5 if new or noise(x, ri, seed) < 0.6 else 4
            h = 5 if new else (4 if noise(ri, x, seed + 1) < 0.5 else 5)
            if not new and noise(x, ri, seed + 7) < 0.1:
                x += w + 1
                continue
            ty = y0 + (0 if new else int(noise(x, ri, seed + 2) * 2))
            pc = x + w // 2
            c.px(pc, ty - 3, "k")                               # the peg
            c.px(pc, ty - 2, "r" if (n + ri + seed) % 5 == 0 else "d")
            c.px(pc - 1, ty - 1, "d")
            c.px(pc + 1, ty - 1, "d")
            old = not new and noise(x, ri, seed + 4) < 0.35
            face, lit, ink = ("c", "c", "m") if new else (("m", "l", "d") if old else ("l", "h", "d"))
            c.rect(x, ty, x + w - 1, ty + h - 1, face)
            c.hl(x, x + w - 2, ty, lit)
            for ly in range(ty + 1, ty + h - 1, 2):             # scratched lines of writing
                c.hl(x + 1, x + w - 2 - (1 if (ly + n) % 3 == 0 else 0), ly, ink)
            c.box(x - 1, ty - 1, x + w, ty + h, "k")
            c.px(x - 1, ty - 1, ".")
            c.px(x + w, ty - 1, ".")
            x += w + 2
            n += 1
    return c


for _i, _s in enumerate((3, 8, 14, 21)):
    stamp(f"votives_{'abcd'[_i]}", 1, 2, art=[("wood", _votives(_s))],
          note="small wooden votive tablets hung on pegs in rows over the rock, one pilgrim's account each")
stamp("votives_new", 1, 2, art=[("wood", _votives(5, new=True))],
      note="the newest tablets, pale fresh wood, all cut alike: all four words the same")


def _rock_lamp():
    """A lamp in a niche cut into the rock, its flame lighting the niche."""
    c = Canvas(16, 16)
    c.ell(7.5, 8, 5, 6, "1")
    c.ell(7.5, 8.5, 4, 5, "2")
    c.ell(7.5, 9, 3, 3.5, "l")
    c.ell(7.5, 9.5, 2, 2.2, "L")
    c.rect(4, 12, 11, 13, "3")                   # the niche's sill
    c.hl(4, 11, 12, "5")
    c.paste(["..kkkk..",
             ".k3333k.",
             "k344443k",
             ".kk33kk."], 4, 11)                 # a clay lamp, in stone tones
    c.px(7, 9, "L")
    c.px(7, 8, "6")
    c.px(8, 10, "L")
    return c


stamp("rock_lamp", 1, 1, art=[("stone", _rock_lamp())], note="a clay lamp burning in a niche cut into the rock")


def _sleep_bench(blanket="r"):
    """A sleeping bench along the side wall, end on: a low timber bench, a
    straw tick plumped up, a pillow at the head and a blanket folded at the
    foot. 1x2."""
    base, lit, dark = {"r": ("r", "r", "R"), "u": ("u", "U", "u")}[blanket]
    c = Canvas(16, 32)
    c.rect(2, 2, 13, 29, "m")                    # the bench's frame
    c.vl(2, 2, 29, "l")
    c.vl(13, 2, 29, "d")
    c.hl(2, 13, 29, "d")
    c.rect(3, 3, 12, 27, "c")                    # the tick
    c.vl(12, 4, 27, "C")
    c.vl(3, 4, 27, "C")
    for y in (10, 16):
        c.hl(4, 11, y, "C")
    c.ell(7.5, 6, 4, 2.4, "c")                   # the pillow
    c.hl(5, 10, 8, "C")
    c.px(4, 5, "C")
    c.px(11, 5, "C")
    c.rect(3, 19, 12, 26, base)                  # the folded blanket
    c.hl(3, 12, 19, lit if blanket == "u" else "c")
    c.hl(3, 12, 20, lit)
    c.hl(3, 12, 23, "k")
    c.hl(3, 12, 24, lit)
    c.hl(3, 12, 26, dark if blanket == "r" else "k")
    c.vl(12, 20, 26, "R" if blanket == "r" else "k")
    c.px(4, 27, "c")                             # a fringe
    c.px(6, 27, "c")
    c.px(8, 27, "c")
    c.px(10, 27, "c")
    c.rect(2, 30, 3, 30, "d")
    c.rect(12, 30, 13, 30, "d")
    c.outline("k")
    return c


stamp("sleep_bench", 1, 2, art=[("wood", _sleep_bench("r"))],
      note="a sleeping bench: a straw tick, a cloak for a pillow, a red blanket folded at its foot")
stamp("sleep_bench_b", 1, 2, art=[("wood", _sleep_bench("u"))],
      note="a sleeping bench with a blue blanket folded at its foot")


def _firepit():
    """The hall's hearth: a round pit ringed with fire-blackened stones,
    split logs burning down to a bed of embers. 2x2, clay."""
    c = Canvas(32, 32)
    c.ell(15.5, 16, 14, 13, "k")
    # the stone ring: lumpy stones, lit on top
    for i in range(16):
        import math
        a = i / 16 * 2 * math.pi
        sx, sy = 15.5 + math.cos(a) * 11.5, 16 + math.sin(a) * 10.5
        c.ell(sx, sy, 3, 2.6, "S")
        c.ell(sx - 0.6, sy - 0.8, 1.8, 1.2, "t")
        c.px(int(sx + 1), int(sy + 1), "s")
    c.ell(15.5, 16.5, 8.5, 7.5, "k")
    c.ell(15.5, 16.5, 7.5, 6.5, "a")             # ash
    c.ell(15.5, 17, 6, 5, "d")                   # embers
    for (x, y) in [(11, 15), (14, 19), (19, 18), (17, 14), (12, 19), (20, 16)]:
        c.px(x, y, "f")
        c.px(x + 1, y, "F")
    # split logs crossed over the coals
    c.line(10, 14, 21, 20, "k")
    c.line(10, 13, 21, 19, "m")
    c.line(10, 20, 21, 13, "k")
    c.line(10, 19, 21, 12, "l")
    # flames, flickering up from the crossing
    c.paste(["....f.....",
             "...fF..f..",
             "..fFF.fF..",
             ".fFYFfFYf.",
             ".fYYYFYYFf",
             "fFYYYYYYFf",
             ".fFYYYYFf.",
             "..ffFFff.."], 11, 9)
    c.outline("k")
    return c


stamp("firepit", 2, 2, art=[("clay", _firepit())],
      note="the hall's hearth: a pit ringed with fire-blackened stones, logs burning on a bed of embers")


def _smoke():
    """Smoke going up from the fire to the smoke-hole in the rock: a wavering
    column, dense near the fire and thinning toward the ceiling, on the top
    layer so people pass under it. 2x2."""
    import math
    c = Canvas(32, 32)
    for y in range(32):
        t = (31 - y) / 31.0                      # 0 at the fire, 1 at the ceiling
        cx = 15.5 + math.sin(y / 4.5) * (1.5 + t * 3)
        wdt = 3.0 + t * 4.5
        dens = 0.9 - t * 0.55
        for x in range(32):
            d = abs(x - cx)
            if d > wdt:
                continue
            n = noise(x, y, 4)
            if d < wdt * 0.45 and n < dens:
                c.px(x, y, "c" if (x + y) % 3 else "t")
            elif n < dens * 0.7 and (x + y) % 2 == 0:
                c.px(x, y, "t" if d < wdt * 0.75 else "S")
    return c


stamp("smoke", 2, 2, top=[("clay", _smoke())], walk={(0, 0), (1, 0), (0, 1), (1, 1)},
      note="smoke rising from the fire toward the smoke-hole, over the walkers' heads")


def _kerb(n):
    """The low stone kerb round the fire, where the pilgrims sit to dry out:
    n cells long, end on to the room."""
    c = Canvas(16 * n, 16)
    c.rect(0, 4, 16 * n - 1, 14, "k")
    for i in range(n * 2):
        x0 = i * 8 + 1
        c.rect(x0, 5, x0 + 6, 13, "S")
        c.hl(x0, x0 + 6, 5, "t")
        c.hl(x0, x0 + 6, 6, "t")
        c.vl(x0 + 6, 6, 13, "s")
        c.hl(x0, x0 + 6, 13, "s")
        if noise(i, 1, 2) < 0.5:
            c.px(x0 + 2, 9, "s")
    c.hl(0, 16 * n - 1, 15, "a")                 # its shadow
    return c


stamp("hearth_kerb", 3, 1, art=[("clay", _kerb(3))], behavior={(2, 0): "MB_COUNTER"},
      note="the stone kerb round the fire: pilgrims sit on it; the hall-keeper is talked to across it")


def _kindling():
    c = Canvas(16, 16)
    c.ell(7.5, 10, 6.5, 5, "K")                  # a deep wicker basket
    c.ell(7.5, 9, 6, 3.5, "j")
    for x in range(2, 14):
        for y in range(8, 15):
            if c.get(x, y) == "K" and (x + y) % 3 == 0:
                c.px(x, y, "J")
    for (x0, y0, x1, y1) in [(3, 2, 6, 9), (6, 1, 8, 9), (9, 2, 11, 9), (11, 4, 12, 9), (4, 4, 10, 8)]:
        c.line(x0, y0, x1, y1, "d")
        c.line(x0 + 1, y0, x1 + 1, y1, "m")
    c.outline("k")
    return c


stamp("kindling", 1, 1, art=[("nature", _kindling())], note="a wicker basket of split kindling")


def _hydria():
    """A three-handled water jar for the hall: water to warm, and to wash."""
    return """
................
......kkkk......
.....kmllmk.....
......kmmk......
..kk.kmmmmk.kk..
.kmdkmlhllmkdmk.
.kd.klhhllmk.dk.
..k.kllllllmkk..
...kmllllllmmk..
...kmmllllmmmk..
...kdmmmmmmmdk..
....kdmmmmmdk...
.....kdddddk....
......kkkkk.....
................
................
"""


stamp("hydria", 1, 1, art=[("clay", _hydria())], note="a hydria, the hall's water jar")


def _honey_cakes():
    """A flat basket heaped with honey cakes by the door: for the snakes
    below, two for the way down."""
    c = Canvas(16, 16)
    c.ell(7.5, 10.5, 7, 4.5, "K")
    c.ell(7.5, 9.5, 6.5, 3.5, "j")
    for (cx, cy) in [(4, 8), (8, 7), (11, 9), (6, 10), (9, 10), (7, 5), (4, 11), (11, 12)]:
        c.ell(cx, cy, 2, 1.5, "m")
        c.px(cx - 1, cy - 1, "J")
        c.px(cx, cy - 1, "J")
        c.px(cx + 1, cy, "d")
    c.outline("k")
    return c


stamp("honey_cakes", 1, 1, art=[("nature", _honey_cakes())],
      note="a basket of honey cakes by the door, for the snakes below")


def _staffs():
    """Pilgrims' staffs leaned on the rock, and the white linen they go down
    in, hung on pegs."""
    c = Canvas(16, 32)
    # a white robe hung on a peg
    c.px(4, 5, "k")
    c.paste(["..kkkk..",
             ".kccccCk",
             "kcccccCk",
             "kccccCCk",
             "kcccccCk",
             "kccccCCk",
             ".kcccCk.",
             ".kcccCk.",
             ".kccCCk.",
             ".kkkkkk."], 1, 6)
    # three staffs leaning, the tallest with a crook
    for (x0, y0, x1, y1, hi) in [(9, 3, 11, 29, "l"), (12, 6, 13, 29, "h"), (14, 9, 14, 29, "l")]:
        c.line(x0, y0, x1, y1, "m")
        c.line(x0 - 1, y0, x1 - 1, y1, hi)
    c.paste(["kk.", "k.k", "..k"], 8, 1)
    for (x, y) in [(10, 29), (11, 30), (12, 30), (13, 30), (14, 30)]:
        c.px(x, y, "k")
    c.outline("k")
    return c


stamp("staffs", 1, 2, art=[("wood", _staffs())],
      note="pilgrims' staffs leaned on the rock, and the white linen they go down in")


def _blankets():
    c = Canvas(16, 16)
    layers = [("u", "U"), ("r", "R"), ("c", "C"), ("u", "U"), ("R", "r")]
    y = 13
    for (a, b) in layers:
        c.rect(2, y - 2, 13, y, a)
        c.hl(2, 13, y - 2, b if a != "R" else "r")
        y -= 3
    c.outline("k")
    return c


stamp("blankets", 1, 1, art=[("wood", _blankets())], note="a pile of folded blankets for those who come up cold")

# ---- Herkyna's house: the mill-race --------------------------------------------


def _race(phase, plank=False, end=None):
    """The mill-race in its stone channel, running east across the floor:
    marble-grey kerbs, the water low between them. In the bronze palette (its
    marble greys are the kerbs; its browns the plank). end: 'in' where it
    comes through the west wall, 'out' where it leaves by the east."""
    c = Canvas(16, 16)
    c.rect(0, 0, 15, 2, "m")                     # north kerb, its top lit
    c.hl(0, 15, 0, "M")
    c.hl(0, 15, 3, "k")
    c.rect(0, 4, 15, 4, "z")                     # the inner face in shadow
    c.rect(0, 5, 15, 11, "u")
    c.hl(0, 15, 12, "n")                         # the south kerb's inner face, lit
    c.rect(0, 13, 15, 15, "m")
    c.hl(0, 15, 15, "n")
    for x in (5, 13):                            # joints in the kerb stones
        c.vl((x + phase * 3) % 16, 0, 2, "n")
        c.vl((x + phase * 5 + 2) % 16, 13, 15, "n")
    # ripples running east
    for (x, y) in [(1, 6), (7, 8), (11, 6), (3, 10), (13, 9)]:
        xx = (x + phase * 4) % 16
        c.hl(xx, min(15, xx + 2), y, "U")
        c.px(min(15, xx + 3), y, "a")
    if plank:
        c.rect(3, 0, 12, 15, "z")
        c.rect(4, 0, 11, 14, "b")
        c.vl(4, 0, 14, "y")
        c.vl(11, 0, 14, "z")
        c.hl(4, 11, 7, "z")
        c.px(6, 2, "z")
        c.px(9, 11, "z")
        c.hl(3, 12, 15, "k")
    if end == "in":
        c.rect(0, 0, 4, 15, "k")
        c.rect(0, 5, 3, 11, "z")
        c.paste(["mmmmm", "Mmmmn", "mmmn.", "mmn..", "mn..."], 0, 0)
        c.vl(4, 4, 12, "n")
        for y in (6, 9):
            c.hl(4, 6, y, "a")
    if end == "out":
        c.rect(11, 0, 15, 15, "k")
        c.rect(12, 5, 15, 11, "z")
        c.paste(["mmmmm", "nmmmM", ".nmmm", "..nmm", "...nm"], 11, 0)
        c.vl(11, 4, 12, "n")
    return c


stamp("race_a", 1, 1, art=[("bronze", _race(0))], note="the mill-race in its stone channel")
stamp("race_b", 1, 1, art=[("bronze", _race(1))], note="the mill-race in its stone channel")
stamp("race_c", 1, 1, art=[("bronze", _race(2))], note="the mill-race in its stone channel")
stamp("race_plank", 1, 1, art=[("bronze", _race(1, plank=True))], walk={(0, 0)},
      note="the plank across the mill-race")
stamp("race_in", 1, 1, art=[("bronze", _race(0, end="in"))],
      note="the mill-race coming in under the west wall")
stamp("race_out", 1, 1, art=[("bronze", _race(2, end="out"))],
      note="the mill-race going out under the east wall, toward the mill")


def _goose_pen():
    """The goose pen of woven willow by the door: a ring of wattle round
    clean straw, a water dish and one white feather. Empty, until Goose
    comes home. 2x2, nature."""
    c = Canvas(32, 32)
    c.ell(15.5, 18, 15, 12.5, "K")
    c.ell(15.5, 17, 13.5, 11, "j")
    c.ell(15.5, 19, 12, 9.5, "K")
    c.ell(15.5, 19.5, 11.5, 9, "J")              # straw inside
    for y in range(11, 29):
        for x in range(4, 28):
            if c.get(x, y) == "J" and noise(x, y, 6) < 0.35:
                c.px(x, y, "j")
    # the wattle's weave: alternating withies, upright stakes
    for y in range(4, 31):
        for x in range(0, 32):
            ch = c.get(x, y)
            if ch in "Kj" and (y < 11 or y > 27 or x < 5 or x > 26):
                if (x // 2 + y // 2) % 2 == 0:
                    c.px(x, y, "J" if ch == "j" else "j")
    for x in (3, 9, 16, 22, 28):
        c.vl(x, 6 if 6 < x < 26 else 9, 8 if 6 < x < 26 else 12, "M")
    c.ell(21, 21, 3, 2, "d")                     # the water dish
    c.ell(21, 20.5, 2, 1, "U")
    c.paste(["..w", ".ww", "ww.", "n.."], 10, 18)  # a white feather
    c.outline("k")
    return c


stamp("goose_pen", 2, 2, art=[("nature", _goose_pen())],
      note="the goose pen of woven willow by the door, clean straw, a water dish, a white feather")


def _spin_stool():
    """The grandmother's spinning stool by the hearth: the distaff stuck in a
    hank of carded wool, the spindle hanging from its thread."""
    c = Canvas(16, 16)
    c.rect(2, 8, 13, 10, "m")                    # the stool's seat
    c.hl(2, 13, 8, "h")
    c.vl(3, 11, 14, "d")
    c.vl(12, 11, 14, "d")
    c.rect(2, 7, 13, 7, "c")                     # a fleece on it
    c.ell(10, 4, 3.5, 3, "c")                    # the wool on the distaff
    c.ell(10.5, 4.5, 2, 1.5, "C")
    c.line(8, 1, 13, 10, "l")                    # the distaff
    c.vl(5, 2, 11, "C")                          # the thread
    c.paste(["kmk", ".l.", ".l.", "kmk"], 4, 11)  # the spindle and its whorl
    c.outline("k")
    return c


stamp("spin_stool", 1, 1, art=[("wood", _spin_stool())],
      note="the grandmother's spinning stool: the distaff in a hank of wool, the spindle hanging")


def _window_goose():
    """The window, with a little clay figure on the sill: a girl holding a
    goose, the nymph Herkyna as the river's children make her. Drawn in the
    wall palette's red ochre so it shares the sill's tiles."""
    fig = Canvas(16, 32)
    fig.paste(["...kk.....",
               "..kRRk.kk.",
               "..kRrk.kwk",
               "...kk.kwpk",
               "..kRRkkwpk",
               ".kRrrRkppk",
               ".kRrrRkpk.",
               ".kRrRRkk..",
               ".kRRRRk...",
               "..kkkk...."], 3, 10)
    return over(OA.STAMPS["window"]["img"], fig.img("wall"))


stamp("window_goose", 1, 2, art=_window_goose(),
      note="a shuttered window, and on its sill a clay girl holding a goose")


def _pallet(blanket="u"):
    """A low straw pallet on the floor with a blanket thrown over: 2x1."""
    c = Canvas(32, 16)
    c.rect(1, 3, 30, 14, "k")
    c.rect(2, 4, 29, 13, "C")
    c.rect(2, 4, 9, 12, "c")                     # a pillow
    c.hl(2, 9, 12, "C")
    b, B = ("u", "U") if blanket == "u" else ("R", "r")
    c.rect(10, 4, 29, 13, b)
    for x in range(12, 29, 4):
        c.vl(x, 4, 13, B)
    c.hl(10, 29, 13, "k")
    c.vl(10, 4, 13, "k")
    return c


stamp("pallet", 2, 1, art=[("wood", _pallet("u"))], note="a straw pallet with a blue blanket thrown over")
stamp("pallet_red", 2, 1, art=[("wood", _pallet("r"))], note="a straw pallet with a red blanket")


def _quern():
    """The millstone by the race: a round upper stone with its hole and a
    peg handle, on the lower stone."""
    c = Canvas(16, 16)
    c.ell(7.5, 10, 7, 4.5, "2")
    c.ell(7.5, 8, 7, 4.5, "4")
    c.ell(7, 7.5, 5.5, 3.2, "5")
    c.ell(7.5, 8, 1.5, 1, "1")
    c.line(12, 4, 13, 1, "E")
    c.px(13, 0, "h")
    c.outline("k")
    return c


stamp("quern", 1, 1, art=[("stone", _quern())], note="a quern: the upper millstone on the lower, a peg for a handle")


def _eel_trap():
    """A wicker fish trap, its cone mouth toward you, dripping."""
    c = Canvas(16, 16)
    c.ell(7.5, 9, 6.5, 5.5, "K")
    c.ell(7.5, 9, 5, 4.2, "j")
    c.ell(7.5, 9, 3, 2.6, "K")
    c.ell(7.5, 9, 1.5, 1.2, "M")
    for y in range(4, 15):
        for x in range(1, 15):
            if c.get(x, y) == "j" and (x + y) % 3 == 0:
                c.px(x, y, "J")
    c.outline("k")
    return c


stamp("eel_trap", 1, 1, art=[("nature", _eel_trap())], note="a wicker fish trap, still dripping")

# ---- the mason's house ---------------------------------------------------------


def _chisels():
    """The mason's tools hung on pegs on the plaster: four iron chisels,
    point down, mushroomed at the top from the mallet, and a toothed claw
    chisel; their peg rail above. 1x2 on the wall, stone."""
    c = Canvas(16, 32)
    c.rect(0, 7, 15, 9, "E")                     # the peg rail
    c.hl(0, 15, 7, "h")
    c.hl(0, 15, 10, "1")
    for (x, ln, tip) in [(2, 12, "point"), (6, 15, "flat"), (10, 11, "claw"), (13, 14, "point")]:
        c.px(x, 10, "k")                         # the peg
        c.paste([".5.", "545", "434"], x - 1, 11)   # the struck head
        c.vl(x, 14, 14 + ln - 4, "5")
        c.vl(x + 1, 14, 14 + ln - 4, "3")
        y = 14 + ln - 3
        if tip == "point":
            c.px(x, y, "5")
            c.px(x, y + 1, "4")
        elif tip == "flat":
            c.hl(x - 1, x + 2, y, "5")
            c.hl(x - 1, x + 2, y + 1, "3")
        else:
            c.hl(x - 1, x + 2, y, "5")
            c.px(x - 1, y + 1, "4")
            c.px(x + 1, y + 1, "4")
    return c


stamp("chisels", 1, 2, art=[("stone", _chisels())], note="chisels in rows on pegs, each in its place")


def _mason_tools():
    """A mason's square, a plumb bob on its line and a bow saw, hung on the
    plaster: 1x2, stone."""
    c = Canvas(16, 32)
    c.px(3, 3, "k")
    c.line(3, 4, 3, 22, "6")                     # the plumb line
    c.paste(["k4k", "454", "343", ".3.", ".k."], 2, 22)
    c.px(9, 3, "k")
    c.rect(8, 4, 9, 22, "h")                     # the square
    c.rect(8, 21, 14, 22, "h")
    c.vl(9, 5, 21, "E")
    c.hl(9, 14, 22, "E")
    for y in range(6, 21, 3):
        c.px(8, y, "e")
    c.outline("k")
    return c


stamp("mason_tools", 1, 2, art=[("stone", _mason_tools())], note="a mason's square and a plumb bob, hung on pegs")


def _workbench():
    """The heavy bench: a mallet lying on it, chisels, a block of soft stone
    being dressed, and a scatter of dust. 3x1, wood (its bronze for iron)."""
    c = Canvas(48, 16)
    c.rect(1, 3, 46, 10, "k")
    c.rect(2, 3, 45, 8, "l")
    c.hl(2, 45, 3, "h")
    c.hl(2, 45, 8, "m")
    c.rect(2, 9, 45, 9, "d")
    for x in (4, 5, 42, 43):
        c.vl(x, 10, 14, "d")
    c.vl(3, 10, 14, "k")
    c.vl(6, 10, 14, "k")
    c.vl(41, 10, 14, "k")
    c.vl(44, 10, 14, "k")
    # the mallet: a round wooden head and handle
    c.paste(["..kkkk...........",
             ".kmmllk..........",
             "kmmllhlkkkkkkkk..",
             "kmmlllkdlllllllk.",
             ".kmmmk.kkkkkkkk..",
             "..kkk............"], 5, 2)
    # chisels lying across
    c.line(24, 4, 31, 6, "z")
    c.line(24, 5, 31, 7, "b")
    c.line(27, 3, 33, 4, "z")
    # a block being dressed, and its chips
    c.paste(["kkkkkkk",
             "kCcccck",
             "kcccccC",
             "kCcCCCk",
             "kkkkkkk"], 36, 2)
    for (x, y) in [(34, 6), (35, 7), (40, 7), (21, 5)]:
        c.px(x, y, "C")
    return c


stamp("workbench", 3, 1, art=[("wood", _workbench())],
      note="the mason's bench: the mallet on it, chisels, a block half dressed")


SNAKE = """
..........2222....
.........256652...
........25665512..
........2562222...
.........252......
........2562......
.......2562.......
......2562........
......2562........
.......2562.......
........2562......
.........2562.....
..........2562....
..222222...2552...
.25566652222562...
256655556666652...
2555222225555552..
.2222.....22222...
"""


def _snake_relief():
    """The half-carved votive: a squared limestone block, and on its face a
    snake rising out of its coil, the left half finished and smoothed, the
    right still rough from the point chisel with the snake's line scratched
    on to follow. 2x2, stone."""
    c = Canvas(32, 32)
    c.rect(1, 2, 30, 30, "k")
    c.rect(2, 3, 29, 8, "5")                     # the top, lit
    c.hl(2, 29, 3, "6")
    c.hl(2, 29, 8, "4")
    c.rect(2, 9, 29, 29, "4")                    # the face
    c.hl(2, 29, 9, "3")
    c.vl(29, 9, 29, "3")
    c.hl(2, 29, 29, "2")
    for y in range(10, 29):                      # the rough half: point-chisel pocks
        for x in range(17, 29):
            n = noise(x, y, 12)
            if n < 0.22:
                c.px(x, y, "3")
            elif n > 0.88:
                c.px(x, y, "5")
            elif n > 0.8:
                c.px(x, y, "2")
    c.paste(SNAKE, 3, 10)
    c.px(14, 12, "k")                            # the eye
    for (x, y) in [(19, 24), (20, 23), (21, 22), (22, 22), (23, 23), (24, 24), (25, 25), (26, 25)]:
        c.px(x, y, "6")                          # its line, scratched on the rough stone
    for (x, y) in [(30, 27), (31, 29), (29, 31), (4, 31), (17, 31), (18, 30)]:
        c.px(x, y, "6")                          # chips at its foot
    return c


stamp("snake_relief", 2, 2, art=[("stone", _snake_relief())],
      note="a half-carved votive: a snake coming up out of the rough stone")


def _blocks():
    """Rough quarried blocks waiting, stacked two high: 2x1, stone."""
    c = Canvas(32, 16)
    for (x0, y0, x1, y1) in [(1, 6, 15, 14), (16, 7, 30, 14), (6, 1, 22, 7)]:
        c.rect(x0, y0, x1, y1, "4")
        c.hl(x0, x1, y0, "5")
        c.vl(x1, y0, y1, "3")
        c.hl(x0, x1, y1, "2")
        for x in range(x0 + 1, x1):
            for y in range(y0 + 1, y1):
                if noise(x, y, x0) < 0.12:
                    c.px(x, y, "3")
    c.outline("k")
    return c


stamp("blocks", 2, 1, art=[("stone", _blocks())], note="rough quarried blocks waiting to be dressed")


def _dust(seed):
    """A drift of stone dust swept into a corner: pale limestone on the
    earth floor (the floor palette's own), flat on the bottom layer."""
    c = Canvas(16, 16)
    pts = [(int(noise(i, 3, seed) * 12) + 2, int(noise(3, i, seed) * 10) + 3) for i in range(4)]
    for (x, y) in pts:
        c.ell(x, y, 3 + noise(x, y, seed) * 2, 2, "y")
    for (x, y) in pts:
        c.ell(x - 0.5, y - 0.5, 2, 1.2, "l")
        c.px(x - 1, y - 1, "L")
    for y in range(16):
        for x in range(16):
            if c.get(x, y) == "." and noise(x, y, seed + 2) < 0.06:
                c.px(x, y, "l")
    return c


for _i in range(3):
    stamp(f"dust_{'abc'[_i]}", 1, 1, flat=[("floor", _dust(_i + 4))], walk={(0, 0)},
          note="a drift of stone dust swept into the corner")


def _bucket():
    c = Canvas(16, 16)
    c.ell(7.5, 6, 5.5, 2.5, "m")
    c.rect(2, 6, 13, 13, "m")
    c.ell(7.5, 13, 5.5, 2, "m")
    c.ell(7.5, 6, 4.5, 1.6, "u")
    c.px(6, 6, "U")
    c.hl(2, 13, 8, "z")
    c.hl(2, 13, 12, "z")
    c.vl(13, 7, 13, "d")
    c.vl(2, 7, 13, "l")
    c.line(2, 6, 7, 1, "z")
    c.line(7, 1, 13, 6, "z")
    c.outline("k")
    return c


stamp("bucket", 1, 1, art=[("wood", _bucket())], note="a bucket of water for wetting the stone")


# ---- shared furnishings ---------------------------------------------------------


def _bed_roll():
    """A sleeping place on the floor for the pilgrims who don't get a bench:
    a rush mat, a blanket rolled at its head. 2x1, walkable, middle layer."""
    c = Canvas(32, 16)
    c.rect(1, 2, 30, 13, "j")
    for y in range(3, 13):
        for x in range(2, 30):
            c.px(x, y, "J" if (x + (y // 2) * 2) % 4 < 2 else "j")
    c.box(1, 2, 30, 13, "K")
    c.hl(2, 29, 14, "M")
    c.rect(3, 4, 9, 11, "w")                     # the rolled blanket at its head
    c.vl(5, 4, 11, "n")
    c.vl(8, 4, 11, "n")
    c.box(2, 3, 10, 12, "k")
    return c


stamp("bed_roll", 2, 1, art=[("nature", _bed_roll())], walk={(0, 0), (1, 0)},
      note="a rush mat on the floor with a blanket rolled at its head: a bed for the pilgrims who don't get a bench")


def _bundles():
    """Pilgrims' bundles: a sack and a rolled blanket tied with cord, a
    gourd for water."""
    c = Canvas(16, 16)
    c.ell(5, 10, 4.5, 4.5, "C")                  # the sack
    c.ell(4.5, 9, 3, 3, "c")
    c.paste(["kCk", ".k."], 3, 4)
    c.rect(8, 8, 14, 13, "u")                    # a rolled blanket
    c.vl(8, 8, 13, "U")
    c.vl(11, 8, 13, "C")
    c.ell(12, 5, 2, 2.5, "l")                    # a gourd
    c.px(12, 2, "m")
    c.outline("k")
    return c


stamp("bundles", 1, 1, art=[("wood", _bundles())], note="pilgrims' bundles: a sack, a rolled blanket, a gourd")


def _toy_goose():
    """Herkyna's toy: a wooden goose on four wheels, on a string."""
    c = Canvas(16, 16)
    c.paste(["......kk......",
             ".....kcck.....",
             ".....kcCkk....",
             "......kcbbk...",
             "..k...kck.....",
             ".kck.kcck.....",
             ".kccccccck....",
             ".kcccccCCk....",
             "..kCCCCCk.....",
             "...kkkkk......",
             "...kmk.kmk....",
             "....k...k....."], 1, 2)
    c.line(9, 12, 14, 14, "C")
    return c


stamp("toy_goose", 1, 1, art=[("wood", _toy_goose())], note="Herkyna's wooden goose on wheels, on a string")


def _river_stones():
    """A basket of smooth river stones, the ones too good for the floor."""
    c = Canvas(16, 16)
    c.ell(7.5, 10.5, 6.5, 4.5, "K")
    c.ell(7.5, 9.5, 5.5, 3, "j")
    for (x, y, t) in [(5, 8, "w"), (8, 7, "U"), (10, 9, "u"), (6, 10, "U"), (9, 10, "n"), (4, 10, "u")]:
        c.ell(x, y, 1.6, 1.1, t)
    c.outline("k")
    return c


stamp("river_stones", 1, 1, art=[("nature", _river_stones())], note="a basket of smooth river stones")


def _drum_offcut():
    """A spoiled column drum, cracked through, kept for the pieces."""
    c = Canvas(16, 16)
    c.ell(7.5, 11, 6, 3.5, "3")
    c.rect(2, 5, 13, 11, "4")
    c.ell(7.5, 5, 6, 3.5, "5")
    c.ell(7.5, 5, 4.5, 2.5, "4")
    for x in range(3, 13, 3):
        c.vl(x, 7, 12, "3")                      # the flutes
    c.line(9, 3, 11, 8, "2")                     # the crack that spoiled it
    c.outline("k")
    return c


stamp("drum_offcut", 1, 1, art=[("stone", _drum_offcut())], note="a spoiled column drum, cracked through")


def _herm_blank():
    """A herm roughed out for a crossroads: a square pillar, the god's head
    blocked in at the top, no face yet. 1x2, stone."""
    c = Canvas(16, 32)
    c.rect(4, 14, 11, 29, "4")                   # the shaft
    c.vl(4, 14, 29, "5")
    c.vl(11, 14, 29, "3")
    c.ell(7.5, 8, 4.5, 5.5, "4")                 # the head, blocked out
    c.ell(6.5, 7, 2.5, 3, "5")
    c.rect(5, 12, 10, 14, "3")                   # the beard, a rough wedge
    c.hl(5, 10, 12, "4")
    c.rect(3, 29, 12, 30, "3")                   # its base
    for (x, y) in [(8, 18), (6, 22), (9, 25), (7, 9)]:
        c.px(x, y, "3")                          # point marks
    c.outline("k")
    return c


stamp("herm_blank", 1, 2, art=[("stone", _herm_blank())],
      note="a herm roughed out for some crossroads: the god's head blocked in, no face yet")
