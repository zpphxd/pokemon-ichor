#!/usr/bin/env python3
"""Kirrha's pieces: Strophios's inn round its courtyard well, the Agora stall
in a fishing shed, the muleteer's half-stable and Thyia's room full of
brooms. Registered into westrooms_art.STAMPS on import."""
import math

from westrooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, noise, Canvas, OA  # noqa: F401

# ---- the pilgrims' inn -----------------------------------------------------------


def _alcove(side):
    """A sleeping alcove: a box of boards with a straw bed in it, its open
    side hung with a curtain of old sailcloth, patched, drawn half back.
    side 'w': on the west wall, opening east; 's': along the south, opening
    north. 2x2, wood."""
    c = Canvas(32, 32)
    if side == "w":
        c.rect(0, 0, 27, 31, "d")                # the box: boards, seen from above
        c.rect(0, 2, 25, 29, "m")
        c.hl(0, 25, 2, "l")
        c.hl(0, 27, 0, "k")
        c.hl(0, 27, 31, "k")
        c.rect(1, 5, 22, 26, "C")                # the bed: a straw tick, a blanket
        c.rect(1, 5, 7, 26, "c")                 # the pillow end against the wall
        c.rect(8, 5, 22, 26, "u")
        for y in range(7, 26, 4):
            c.hl(8, 22, y, "U")
        c.vl(8, 5, 26, "k")
        c.box(0, 4, 23, 27, "k")
        # the curtain: sailcloth hung from a rail along the open side, drawn
        # back toward the top so the bed shows
        c.vl(26, 0, 31, "k")
        c.rect(23, 1, 30, 14, "c")
        for y in range(1, 15):
            c.px(23 + (y % 3), y, "C")
            c.px(28 - (y % 2), y, "C")
        c.rect(24, 15, 29, 30, "c")
        c.vl(26, 15, 30, "C")
        c.vl(29, 15, 30, "C")
        c.rect(25, 19, 28, 23, "r")              # a red patch
        c.box(25, 19, 28, 23, "R")
        c.rect(24, 6, 26, 9, "U")                # a blue one, higher up
        c.box(22, 0, 31, 31, "k")
        c.hl(23, 30, 0, "y")                     # the rail's rings
        c.px(31, 15, "k")
    else:
        c.rect(0, 0, 31, 27, "d")
        c.rect(2, 0, 29, 25, "m")
        c.vl(2, 0, 25, "l")
        c.vl(0, 0, 27, "k")
        c.vl(31, 0, 27, "k")
        c.rect(5, 1, 26, 22, "C")
        c.rect(5, 1, 26, 7, "c")
        c.rect(5, 8, 26, 22, "r")
        for x in range(7, 26, 4):
            c.vl(x, 8, 22, "R")
        c.hl(5, 26, 8, "k")
        c.box(4, 0, 27, 23, "k")
        c.hl(0, 31, 23, "k")
        c.rect(1, 24, 14, 30, "c")               # the curtain along the front, drawn aside
        c.rect(17, 24, 30, 30, "c")
        for x in range(1, 31):
            if c.get(x, 25) == "c" and x % 3 == 0:
                c.vl(x, 25, 30, "C")
        c.rect(19, 26, 22, 29, "U")
        c.box(18, 25, 23, 30, "u")
        c.hl(0, 31, 24, "y")
        c.hl(0, 31, 31, "k")
        c.vl(15, 24, 31, "k")
        c.vl(16, 24, 31, "k")
    c.outline("k")
    return c


_aw = _alcove("w")
stamp("alcove_w", 2, 2, art=[("wood", _aw)], note="a sleeping alcove behind a patched sailcloth curtain, opening east")
stamp("alcove_e", 2, 2, art=hflip(grid("wood", _aw.text(), 32, 32)),
      note="a sleeping alcove behind a patched sailcloth curtain, opening west")
stamp("alcove_s", 2, 2, art=[("wood", _alcove("s"))],
      note="a sleeping alcove along the south side, its sailcloth curtain drawn aside")


def _well():
    """The courtyard well: a round curb of grey stone, the water low and dark
    in it, a timber frame over it with a pulley, rope and bucket. 2x2, in the
    bronze palette (its marble greys are the curb, its browns the frame)."""
    c = Canvas(32, 32)
    c.ell(15.5, 20, 13.5, 10, "n")              # the curb's outer face
    c.ell(15.5, 18, 13.5, 10, "m")
    c.ell(15.5, 17, 13, 9, "M")                 # its lit top
    c.ell(15.5, 18, 9.5, 6.5, "k")
    c.ell(15.5, 18.5, 8.5, 5.5, "u")             # the water, down in the dark
    c.ell(14, 17, 3, 1.4, "U")
    c.px(18, 20, "a")
    for i in range(10):                          # joints between the curb stones
        a = i / 10 * 2 * math.pi
        x, y = 15.5 + math.cos(a) * 11.3, 17.5 + math.sin(a) * 7.8
        c.px(int(round(x)), int(round(y)), "n")
    # the frame: two posts and a crossbeam with a pulley
    for x in (3, 27):
        c.rect(x, 2, x + 2, 21, "z")
        c.vl(x, 2, 21, "y")
    c.rect(3, 2, 29, 4, "b")
    c.hl(3, 29, 2, "y")
    c.hl(3, 29, 4, "z")
    c.ell(15.5, 5, 2.5, 2.5, "z")
    c.px(15, 4, "y")
    c.vl(16, 7, 14, "n")                         # the rope
    c.paste(["kkkkk", "kbyzk", "kbbzk", ".kkk."], 14, 14)   # the bucket
    c.outline("k")
    return c


stamp("well", 2, 2, art=[("bronze", _well())], note="the courtyard well: a stone curb, a frame, pulley, rope and bucket")


def _inn_sign():
    """The big painted sign over the hearth: a ship under sail and a mule
    with packs, side by side, and the letters under them (too small to read
    from here: WE TAKE YOU ALL THE WAY. WHEN THE GOD IS IN.) 4x1, wood."""
    c = Canvas(64, 16)
    c.rect(0, 0, 63, 15, "k")
    c.rect(1, 1, 62, 14, "c")
    c.hl(1, 62, 1, "h")
    c.rect(1, 13, 62, 14, "l")
    # the ship: black hull, a red stripe, a square sail with a blue band
    c.paste(["......k........",
             ".....kcCk......",
             "....kccCCk.....",
             "....kuuuUk.....",
             "....kccCCk.....",
             ".....kkkk......",
             "kkkkkkkkkkkkkk.",
             ".krrrrrrrrrrk..",
             "..kkkkkkkkkk..."], 4, 1)
    # the mule with its packs
    c.paste(["..kk.............",
             ".kddk..kkkkk.....",
             "kdddkkkuuurkk....",
             ".kddddddddddddk..",
             "..kdddddddddddk..",
             "...kdk.....kdk...",
             "...kdk.....kdk..."], 22, 2)
    # the letters: two lines of dark strokes
    for x in range(41, 61):
        if x % 4 != 3:
            c.px(x, 4, "d")
            c.px(x, 8, "d")
    for x in range(43, 58):
        if x % 5 != 4:
            c.px(x, 6, "r")
    c.px(0, 0, ".")
    c.px(63, 0, ".")
    return c


stamp("inn_sign", 4, 1, art=[("wood", _inn_sign())],
      note="the painted sign over the hearth: a ship and a mule. WE TAKE YOU ALL THE WAY. (WHEN THE GOD IS IN.)")


def _bundle_shelf():
    """Pilgrims' bundles stacked on a shelf, each with a name tag tied on.
    2x2 on the wall: two shelves of squat cloth bundles, knotted at the top,
    and blankets rolled and corded."""
    c = Canvas(32, 32)
    for y0 in (13, 27):
        c.rect(0, y0, 31, y0 + 2, "m")
        c.hl(0, 31, y0, "h")
        c.hl(0, 31, y0 + 2, "d")
        c.px(3, y0 + 3, "k")
        c.px(28, y0 + 3, "k")

    def bundle(x, base, w, h, col):
        lit = {"c": "c", "C": "c", "u": "U", "r": "r"}[col]
        dark = {"c": "C", "C": "l", "u": "u", "r": "R"}[col]
        top = base - h
        c.rect(x, top + 2, x + w - 1, base - 1, col)
        c.hl(x + 1, x + w - 2, top + 1, col)
        c.vl(x + w - 1, top + 2, base - 1, dark)
        c.hl(x, x + w - 1, base - 1, dark)
        c.hl(x + 1, x + w - 3, top + 2, lit)
        mid = x + w // 2
        c.paste(["k.k", "kkk"], mid - 1, top - 1)    # the knot's two ears
        c.px(mid, top + 1, "d")
        c.paste(["d", "h", "l"], x + w - 2, base - 6)   # the name tag on its cord
    def roll(x, base, w, col):
        dark = {"c": "C", "u": "u", "r": "R"}[col]
        c.rect(x, base - 5, x + w - 1, base - 1, col)
        c.hl(x, x + w - 1, base - 1, dark)
        c.vl(x + 2, base - 5, base - 1, "d")
        c.vl(x + w - 3, base - 5, base - 1, "d")
        c.ell(x + w - 1, base - 3, 1.5, 2.2, dark)
    bundle(1, 13, 8, 8, "c")
    roll(10, 13, 9, "u")
    bundle(20, 13, 7, 9, "r")
    bundle(27, 13, 4, 6, "C")
    roll(1, 27, 8, "r")
    bundle(10, 27, 8, 9, "C")
    bundle(19, 27, 6, 7, "u")
    bundle(25, 27, 6, 8, "c")
    c.outline("k")
    return c


stamp("bundle_shelf", 2, 2, art=[("wood", _bundle_shelf())],
      note="pilgrims' bundles stacked on two shelves, a name tag tied to each")


def _long_table(n=5, counter_at=1):
    """The inn's long table, end to end along the courtyard: bowls of fish
    stew, bread, a jug, cups."""
    c = Canvas(16 * n, 16)
    c.rect(0, 3, 16 * n - 1, 11, "k")
    c.rect(1, 3, 16 * n - 2, 9, "l")
    c.hl(1, 16 * n - 2, 3, "h")
    c.hl(1, 16 * n - 2, 9, "m")
    c.rect(1, 10, 16 * n - 2, 10, "d")
    for x in (2, 3, 16 * n - 4, 16 * n - 3, 8 * n, 8 * n + 1):
        c.vl(x, 11, 14, "d")
    for cx in range(6, 16 * n - 6, 14):          # what's on it
        c.ell(cx, 6, 2.5, 1.6, "C")
        c.ell(cx, 5.8, 1.6, 0.8, "m")
        c.px(cx + 5, 5, "c")
        c.px(cx + 6, 5, "C")
        c.px(cx + 5, 6, "C")
    c.paste(["kk.", "rRk", "rRk", ".k."], 8 * n - 5, 3)   # a red jug
    return c


stamp("long_table", 5, 1, art=[("wood", _long_table())], behavior={(1, 0): "MB_COUNTER"},
      note="the inn's long table: bowls, bread, a jug; Strophios is talked to across it")

# ---- the Agora stall ---------------------------------------------------------------


def _boat_counter(n=5):
    """The counter is an upturned boat: keel along the middle, the planks
    sweeping down to the gunwale on the floor, a red stripe, and the eye
    painted on the bow to see by. n cells long, every cell a counter."""
    W = 16 * n
    c = Canvas(W, 16)
    for x in range(W):
        t = x / (W - 1)
        # a full hull, blunt at the stern (left), pointed at the bow (right)
        if t < 0.08:
            half = 4 + t / 0.08 * 3
        elif t > 0.82:
            half = 7 * ((1 - t) / 0.18) ** 0.7
        else:
            half = 7
        top, bot = int(round(8 - half)), int(round(8 + half))
        for y in range(top, bot + 1):
            if y == top or y == bot:
                c.px(x, y, "k")
            elif y == 7:
                c.px(x, y, "h")                  # the keel, lit
            elif y == 8:
                c.px(x, y, "d")
            elif y < 7:
                c.px(x, y, "l" if (y - top) % 2 else "m")
            elif y == bot - 1:
                c.px(x, y, "r")                  # the red stripe at the gunwale
            elif y == bot - 2:
                c.px(x, y, "R")
            else:
                c.px(x, y, "m" if (y - 8) % 2 else "d")
    c.paste([".kkk.", "kcckk", "kcukk", ".kkk."], W - 15, 3)   # the eye
    for x in range(12, W - 22, 11):              # trinkets laid out on the keel
        c.paste(["kk", "Uk"], x, 5)
        c.paste(["k", "y"], x + 5, 6)
    return c


stamp("boat_counter", 5, 1, art=[("wood", _boat_counter())],
      behavior={(i, 0): "MB_COUNTER" for i in range(5)},
      note="the stall's counter: an upturned boat, its eye painted on the bow")


def _hanging(kind):
    """Votives hung on strings from the beam, for the healing god and for
    Apollo: on the top layer, over people's heads."""
    c = Canvas(16, 16)
    if kind == "wreaths":
        for (x, ln) in [(4, 4), (11, 7)]:
            c.vl(x, 0, ln, "n")
            c.ell(x, ln + 3.5, 3, 3, "g")
            for y in range(ln + 2, ln + 6):
                for xx in range(x - 1, x + 2):
                    if abs(xx - x) + abs(y - ln - 3.5) < 1.6:
                        c.px(xx, y, ".")
            c.px(x - 2, ln + 2, "v")
            c.px(x + 1, ln + 1, "v")
            c.px(x + 2, ln + 4, "G")
        c.outline("k")
        return "nature", c
    if kind == "omphaloi":
        for (x, ln) in [(3, 5), (8, 2), (13, 6)]:
            c.vl(x, 0, ln, "S")
            c.ell(x, ln + 3, 2, 2.6, "t")
            c.px(x - 1, ln + 2, "c")
            c.hl(x - 1, x + 1, ln + 3, "s")       # the netted pattern of the omphalos
            c.px(x, ln + 4, "s")
        c.outline("k")
        return "clay", c
    if kind == "feet":
        for (x, ln, foot) in [(4, 3, True), (11, 6, False)]:
            c.vl(x, 0, ln, "S")
            if foot:
                c.paste(["mm..", "lm..", "lm..", "llmm", "hlllm"], x - 1, ln + 1)
            else:
                c.paste([".m.m.", "mlmlm", "mlllm", ".lll.", ".lm.."], x - 2, ln + 1)
        c.outline("k")
        return "clay", c
    raise ValueError(kind)


for _k in ("wreaths", "omphaloi", "feet"):
    _pal, _c = _hanging(_k)
    stamp(f"hang_{_k}", 1, 1, top=[(_pal, _c)], walk={(0, 0)},
          note={"wreaths": "laurel wreaths hung on strings from the beam",
                "omphaloi": "little clay omphaloi on strings, the navel of the world for a coin",
                "feet": "clay feet and hands on strings, for the healing god, if your foot hurts"}[_k])


def _votive_strings(seed):
    """Votives on strings down the shed wall from the beam: laurel wreaths,
    little clay omphaloi, clay feet and hands. 1x2 on the wall, each string
    one palette's colors (nature for wreaths, clay for the clay ones)."""
    nat, clay = Canvas(16, 32), Canvas(16, 32)
    # nature in one 8-pixel column, clay in the other, so no 8x8 tile mixes them
    xs = [2, 5, 10, 13]
    kinds = ["wreath", "wreath", "foot", "omphalos"] if seed == 0 else ["omphalos", "hand", "wreath", "wreath"]
    for i, (x, kind) in enumerate(zip(xs, kinds)):
        top = 8 + (i * 5 + seed * 3) % 7
        if kind == "wreath":
            nat.vl(x, 7, top + 1, "n")
            nat.ell(x, top + 5, 2.6, 2.6, "g")
            nat.px(x, top + 5, ".")
            nat.px(x - 1, top + 4, "v")
            nat.px(x + 1, top + 6, "G")
            nat.px(x - 2, top + 6, "v")
        else:
            clay.vl(x, 7, top + 1, "S")
            if kind == "omphalos":
                clay.ell(x, top + 4, 2, 2.6, "t")
                clay.px(x - 1, top + 3, "c")
                clay.hl(x - 1, x + 1, top + 4, "s")
            elif kind == "foot":
                clay.paste(["mm..", "lm..", "lm..", "llmm", "hllm"], x - 1, top + 2)
            else:
                clay.paste([".m.m.", "mlmlm", "mlllm", ".lll.", ".lm.."], x - 2, top + 2)
    nat.outline("k")
    clay.outline("k")
    return [("nature", nat), ("clay", clay)]


stamp("votive_strings_a", 1, 2, art=_votive_strings(0),
      note="votives on strings down the wall: wreaths, clay feet and hands, little omphaloi")
stamp("votive_strings_b", 1, 2, art=_votive_strings(1),
      note="votives on strings down the wall: wreaths, clay feet and hands, little omphaloi")


def _votive_table():
    """A trestle table of votives nobody's buying: clay feet and hands in
    rows, little omphaloi, a stack of wreaths. 2x1, clay."""
    c = Canvas(32, 16)
    c.rect(1, 4, 30, 10, "d")
    c.rect(1, 3, 30, 8, "m")
    c.hl(1, 30, 3, "l")
    for x in (3, 4, 27, 28):
        c.vl(x, 11, 14, "d")
    for x in range(3, 14, 4):
        c.paste(["l.", "lm"], x, 5)              # feet
    for x in range(16, 22, 3):
        c.paste(["t", "s"], x, 5)                # omphaloi
    c.paste(["kSSk", "SttS", "kSSk"], 24, 4)    # a bowl of offerings
    c.outline("k")
    return c


stamp("votive_table", 2, 1, art=[("clay", _votive_table())], note="a trestle table of clay votives nobody is buying")


def _lantern():
    """The ship's lantern hung over the door from a bracket: bronze, horn
    panes, a flame. Top layer, so the player walks under it."""
    c = Canvas(16, 16)
    c.vl(8, 0, 3, "z")
    c.paste(["..kkk..",
             ".kbyyk.",
             "kzyYYbk",
             "kzeFeBk",
             "kzeYeBk",
             "kzFeFbk",
             "kzbbbbk",
             ".kzzzk.",
             "..kkk.."], 5, 3)
    c.replace("B", "z")
    return c


stamp("lantern", 1, 1, top=[("bronze", _lantern())], walk={(0, 0)},
      note="a ship's lantern hung over the door")


def _potion_crate():
    """A crate of potion flasks: votives aren't selling."""
    c = Canvas(16, 16)
    c.rect(1, 5, 14, 14, "m")
    c.hl(1, 14, 5, "h")
    c.hl(1, 14, 9, "d")
    c.vl(14, 5, 14, "d")
    for (x, col) in [(3, "u"), (6, "r"), (9, "u"), (12, "U")]:
        c.paste(["k", col, col], x, 1)
        c.paste([col + col, col + "c"], x - 0, 3)
    c.outline("k")
    return c


stamp("potion_crate", 1, 1, art=[("wood", _potion_crate())], note="a crate of potion flasks")


def _rope_coil():
    c = Canvas(16, 16)
    for r, col in [(6.5, "K"), (5.5, "n"), (4.2, "j"), (3.2, "n"), (2, "K")]:
        c.ell(7.5, 9, r, r * 0.65, col)
    c.ell(7.5, 9, 1, 0.6, "M")
    c.line(13, 8, 15, 4, "n")
    c.outline("k")
    return c


stamp("rope_coil", 1, 1, art=[("nature", _rope_coil())], note="a coil of rope")


def _net_hang():
    """A fishing net hung up to dry on the shed wall: cork floats along the
    top rope, the mesh sagging. 2x2 on the wall, nature."""
    c = Canvas(32, 32)
    c.hl(1, 30, 4, "K")
    for x in (1, 30):
        c.px(x, 3, "k")
    for y in range(5, 28):
        for x in range(2, 30):
            depth = 22 + int(4 * math.sin(math.pi * (x - 2) / 27))
            if y > depth:
                continue
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                c.px(x, y, "n")
    for x in range(4, 30, 5):
        c.paste(["jJ", "Kj"], x, 3)             # cork floats
    return c


stamp("net_hang", 2, 2, art=[("nature", _net_hang())], note="a fishing net hung up to dry, cork floats along its rope")


def _anchor_stone():
    c = Canvas(16, 16)
    c.ell(7.5, 9.5, 6, 5, "3")
    c.ell(7, 8.5, 4.5, 3.5, "4")
    c.ell(7.5, 6, 1.6, 1.4, "1")
    c.px(6, 7, "5")
    c.outline("k")
    return c


stamp("anchor_stone", 1, 1, art=[("stone", _anchor_stone())], note="an old anchor stone with its rope hole")

# ---- the muleteer's house ------------------------------------------------------------


def _stall_wall(h=3):
    """A stall partition of rough boards, seen end on: 1 wide, h tall, with
    a mule's bell hung on its post."""
    c = Canvas(16, 16 * h)
    c.rect(5, 0, 10, 16 * h - 3, "m")
    c.vl(5, 0, 16 * h - 3, "l")
    c.vl(10, 0, 16 * h - 3, "d")
    for y in range(4, 16 * h - 3, 7):
        c.hl(5, 10, y, "d")
    c.rect(4, 16 * h - 6, 11, 16 * h - 2, "d")   # the post at its foot
    c.hl(4, 11, 16 * h - 6, "l")
    c.paste(["k", "y", "bb", "zk"], 11, 16 * h - 14)   # a bell on a thong
    c.outline("k")
    return c


stamp("stall_wall", 1, 3, art=[("wood", _stall_wall())], note="a stall partition of rough boards")


def _manger():
    """A hay manger along the back of a stall: a slatted wooden rack, hay
    poking through. 2x1, nature."""
    c = Canvas(32, 16)
    c.rect(1, 2, 30, 12, "K")
    c.rect(2, 3, 29, 9, "J")
    for x in range(2, 30):
        if noise(x, 1, 3) < 0.5:
            c.px(x, 2, "J")
            c.px(x, 1, "j")
    for x in range(3, 30, 4):
        c.vl(x, 3, 11, "K")
    c.hl(2, 29, 10, "M")
    c.hl(2, 29, 12, "M")
    c.outline("k")
    return c


stamp("manger", 2, 1, art=[("nature", _manger())], note="a slatted hay manger")


MULE = """
..........kk.kk.................
.........kMuk.kuk...............
.........kMuk.kuk...............
.........kMuk.kMuk..............
..........kuukMuuk..............
.........kuUUuuuuk..............
........kuUUUUuuuk...kkkkkkkk...
.......kuUUUkUUuuukkkuuuuuuuukk.
......kuUUUUUUuuuuuMuuMMMMMMuuuk
.....kUUUUUUUUuukuMMUUUUUUUUMMuk
....kUUUUUUUUuuk.kuUUUUUUUUUUUuuk
....kwUUUUUuuk..kuUUUUUUUUUUUUuuk
....kwwUUUuuk...kuuuuuuuuuuuuuuuk
.....kkkkkkk....kuuuuuuuuuuuuuuk.
...............kuMuuuuuuuuuuuMk..
..............kMMkuuuuuuuuuuMMk..
..............kMk.kMMMMkkkMMMkk..
...............k...kkkk...kkk....
"""


def _mule():
    """The one mule left in, asleep in its stall: lying in the straw with
    its legs folded, head down on the straw in front of it, long ears up, a
    pale muzzle, the dark stripe of the pack-saddle down its back. 2x2."""
    c = Canvas(32, 32)
    c.ell(16, 25, 15, 6, "j")                    # the straw bed
    for x in range(1, 31):
        for y in range(19, 31):
            if c.get(x, y) == "j" and noise(x, y, 8) < 0.4:
                c.px(x, y, "J")
    c.paste(MULE, 0, 9)
    c.px(10, 16, "k")                            # the shut eye
    c.px(11, 16, "k")
    return c


stamp("mule", 2, 2, art=[("nature", _mule())], note="the one mule left, asleep in the straw, ears laid back")


def _ladder(h=3):
    c = Canvas(16, 16 * h)
    c.line(3, 0, 4, 16 * h - 2, "m")
    c.line(11, 0, 12, 16 * h - 2, "m")
    c.line(2, 0, 3, 16 * h - 2, "l")
    c.line(10, 0, 11, 16 * h - 2, "l")
    for y in range(4, 16 * h - 2, 6):
        c.hl(4, 10, y, "l")
        c.hl(4, 10, y + 1, "d")
    c.outline("k")
    return c


stamp("ladder", 1, 3, art=[("wood", _ladder())], note="the ladder up to the hay loft")


def _harness():
    """Harness and bells on pegs: a padded collar, a bridle with a red
    tassel, a strap of bronze bells. 1x2 on the wall, wood."""
    c = Canvas(16, 32)
    for x in (3, 11):
        c.px(x, 5, "k")
    c.ell(4, 13, 3.5, 5.5, "d")                  # the collar
    c.ell(4, 13, 2, 3.8, ".")
    for y in range(8, 19):
        for x in range(0, 9):
            if c.get(x, y) == "d" and (x + y) % 3 == 0:
                c.px(x, y, "m")
    c.vl(11, 6, 24, "d")                         # the bridle's strap, a tassel
    c.paste(["rr", "Rr", "rR", ".r"], 11, 25)
    for i, y in enumerate(range(9, 23, 4)):      # the bells, big to small down the strap
        c.paste(["kbk" if i < 2 else "kb", "byy" if i < 2 else "by", "kzk" if i < 2 else "kz"], 12, y)
    c.outline("k")
    return c


stamp("harness", 1, 2, art=[("wood", _harness())], note="harness and bells on pegs: a collar, a bridle, a strap of bells")


def _window_hive():
    """The window, and on its sill a wooden beehive: a hollowed log with a
    little door, a smear of wax. Drawn in the wall palette's browns."""
    hive = Canvas(16, 32)
    hive.paste(["..kkkkkkkkkk..",
                ".k3333333333k.",
                "k232323232323k",
                "k222222222222k",
                "k211211211212k",
                "k222k...k2222k",
                "k212kkkkk2122k",
                ".k1111111111k.",
                "..kkkkkkkkkk.."], 1, 11)
    hive.px(7, 16, "o")
    hive.px(8, 17, "o")
    return over(OA.STAMPS["window"]["img"], hive.img("wall"))


stamp("window_hive", 1, 2, art=_window_hive(), note="a window, and on its sill a wooden beehive")


def _trough():
    c = Canvas(32, 16)
    c.rect(1, 3, 30, 13, "3")
    c.hl(1, 30, 3, "5")
    c.rect(3, 5, 28, 10, "1")
    c.rect(4, 6, 27, 9, "2")
    c.hl(4, 27, 6, "3")
    c.hl(1, 30, 13, "2")
    c.outline("k")
    return c


stamp("trough", 2, 1, art=[("stone", _trough())], note="a stone water trough")


def _panniers():
    """A pair of wicker panniers for a pack-saddle, empty."""
    c = Canvas(16, 16)
    for x0 in (1, 8):
        c.rect(x0, 4, x0 + 6, 13, "j")
        for y in range(5, 13):
            for x in range(x0 + 1, x0 + 6):
                if (x + y) % 3 == 0:
                    c.px(x, y, "J")
        c.hl(x0, x0 + 6, 4, "J")
        c.hl(x0, x0 + 6, 13, "K")
    c.hl(4, 11, 2, "K")
    c.outline("k")
    return c


stamp("panniers", 1, 1, art=[("nature", _panniers())], note="a pair of wicker panniers for a pack-saddle")


def _sack():
    c = Canvas(16, 16)
    c.ell(7.5, 10, 6, 5, "C")
    c.ell(7, 9, 4.5, 4, "c")
    c.paste([".kk.", "kCCk", ".kk."], 6, 2)
    c.rect(6, 4, 9, 5, "C")
    c.px(5, 11, "C")
    c.outline("k")
    return c


stamp("sack", 1, 1, art=[("wood", _sack())], note="a sack of barley")


def _hay():
    c = Canvas(16, 16)
    c.ell(7.5, 10, 7, 5, "j")
    c.ell(7, 8.5, 5.5, 4, "J")
    for i in range(10):
        x, y = int(noise(i, 1, 2) * 12) + 2, int(noise(1, i, 2) * 8) + 5
        c.line(x, y, x + 2, y - 1, "K")
    c.outline("k")
    return c


stamp("hay", 1, 1, art=[("nature", _hay())], note="an armful of hay")

# ---- Thyia's house: the old sweeper's ---------------------------------------------


def _broom(c, x, top, tilt=0, worn=0, color="J"):
    """One broom leaning, handle up: a long handle, a head of tied twigs.
    worn: the head is that much shorter."""
    bot = 31
    head = 9 - worn
    c.line(x, top, x + tilt, bot - head, "d")
    c.line(x + 1, top, x + tilt + 1, bot - head, "m")
    hx = x + tilt
    c.hl(hx - 1, hx + 2, bot - head, "K")        # the binding
    for i in range(head):
        y = bot - head + 1 + i
        spread = 1 + i // 3
        for xx in range(hx - spread, hx + spread + 2):
            c.px(xx, y, color if (xx + y) % 3 else "j")
        c.px(hx - spread - 1, y, "k")
        c.px(hx + spread + 2, y, "k")


def _brooms_corner(variant):
    """Brooms stood in a corner, every one of them a different age."""
    c = Canvas(16, 32)
    if variant == 0:
        _broom(c, 3, 2, tilt=-1, worn=0)
        _broom(c, 8, 5, tilt=0, worn=3)
        _broom(c, 12, 9, tilt=1, worn=5, color="j")
    else:
        _broom(c, 4, 4, tilt=1, worn=2)
        _broom(c, 10, 1, tilt=-1, worn=0)
    c.outline("k")
    return c


stamp("brooms_a", 1, 2, art=[("nature", _brooms_corner(0))], note="brooms stood in the corner, new to worn to a stub")
stamp("brooms_b", 1, 2, art=[("nature", _brooms_corner(1))], note="two brooms stood in the corner")


def _brooms_drying():
    """A bundle of new brooms hung head-down from the beam to dry: fresh
    green-gold twigs. 2x2 on the wall."""
    c = Canvas(32, 32)
    c.hl(0, 31, 3, "K")
    for i, x in enumerate(range(3, 30, 5)):
        c.vl(x, 3, 6, "n")
        ln = 10 + (i % 3) * 2
        c.vl(x, 6, 6 + ln, "m")
        c.vl(x + 1, 6, 6 + ln, "d")
        c.hl(x - 1, x + 2, 6 + ln, "K")
        for j in range(8):
            y = 7 + ln + j
            spread = 1 + j // 3
            for xx in range(x - spread, x + spread + 2):
                c.px(xx, y, "v" if (xx + y + i) % 4 == 0 else ("J" if (xx + y) % 2 else "j"))
    c.outline("k")
    return c


stamp("brooms_drying", 2, 2, art=[("nature", _brooms_drying())],
      note="a bundle of new brooms hung head-down from the beam to dry")


def _broom_sword():
    """Her old broom, from the god's own floor, on two pegs over the bed like
    a sword: worn nearly to the binding. 2x1 on the wall."""
    c = Canvas(32, 16)
    c.px(6, 5, "k")
    c.px(25, 5, "k")
    c.hl(2, 24, 7, "d")
    c.hl(2, 24, 8, "m")
    c.hl(2, 24, 6, "n")
    c.vl(24, 5, 10, "K")
    c.vl(25, 5, 10, "K")
    for x in range(26, 30):
        for y in range(5 - (x - 26) // 2, 11 + (x - 26) // 2):
            c.px(x, y, "j" if (x + y) % 2 else "J")
    c.paste(["k", "w", "w"], 4, 9)             # a ribbon tied to it
    c.outline("k")
    return c


stamp("broom_sword", 2, 1, art=[("nature", _broom_sword())],
      note="her old broom from the god's floor, on two pegs over the bed like a sword")


def _laurel_pot():
    """A young laurel in a big clay pot, cut from the tree at the temple
    door: a slim trunk, a crown of dark glossy leaves. 2x2, nature."""
    c = Canvas(32, 32)
    c.ell(15.5, 28, 9.5, 3, "d")                 # the pot
    c.rect(7, 21, 24, 28, "m")
    c.ell(15.5, 21, 9, 2.5, "d")
    c.ell(15.5, 20.5, 7.5, 1.6, "K")             # the earth in it
    c.vl(9, 22, 27, "d")
    c.hl(7, 24, 23, "d")
    for x in range(11, 22, 3):
        c.px(x, 25, "j")                         # a band of incised dots
    c.vl(15, 8, 20, "K")                         # the trunk
    c.vl(16, 10, 20, "M")
    # the crown: overlapping clusters of leaves
    for (cx, cy, r) in [(15, 7, 6), (10, 9, 4.5), (21, 9, 4.5), (13, 3, 4), (19, 4, 4), (16, 12, 4)]:
        c.ell(cx, cy, r, r * 0.8, "G")
    for (cx, cy, r) in [(14, 6, 4.5), (9, 8, 3), (20, 8, 3), (12, 2.5, 2.5), (18, 3, 2.5)]:
        c.ell(cx, cy, r, r * 0.7, "g")
    for y in range(0, 16):
        for x in range(0, 32):
            if c.get(x, y) == "g" and noise(x, y, 3) < 0.25:
                c.px(x, y, "v")
            if c.get(x, y) == "G" and noise(x, y, 4) < 0.08:
                c.px(x, y, "g")
    c.outline("k")
    return c


stamp("laurel_pot", 2, 2, art=[("nature", _laurel_pot())],
      note="a young laurel in a big clay pot, cut from the tree at the temple door")


def _dustpan():
    c = Canvas(16, 16)
    c.paste(["kkkkkkk.",
             "kjJJJJjk",
             "kjjjjjjk",
             ".kKKKKk.",
             "...kk...",
             "...kmk..",
             "....kmk.",
             ".....kk."], 4, 6)
    return c


stamp("dustpan", 1, 1, art=[("nature", _dustpan())], note="a wicker dustpan, empty")
