"""The Euploia's hold: MAP_TRIREME_EUPLOIA_HOLD as one 18x9 scene.

The rowers' deck under the open deck, lit by the daylight through the oar
ports and the hatch. Across the top, the starboard hull from inside: deck
beams, strakes, frames and a row of oar ports bright with the day. Below it
the starboard bank, three tiers of seats stepping down toward the gangway
(thranites at the top, zygites, thalamites at the bottom). Under sail the
rowers rest ("Oars in, lads!"), so each seat keeps only its cushion, and its
oar lies in its port, the loom angled up through the tiers. The gangway runs
the length of the hull (rows 5-6) past the mast's step and the ladder up to
the hatch, where the light falls; the port bank's bottom tier (row 7), its
looms angled down, and the bilge (row 8) close the room. Water jars and rope at
the bow end, a lamp and a pithos at the stern end.

The talkable rowers (object events) sit on the bottom tiers, on seats with no
loom drawn; the Potion lies under the port bench.
"""
from __future__ import annotations

from trireme_lib import CELL, Scene

W, H = 18, 9
PW, PH = W * CELL, H * CELL
LADDER = (11, 5)
MAST = 8                 # the mast's column: the deck's x = 11, less 3
SEATS = {(5, 4), (13, 4), (9, 7), (14, 7)}   # empty seats: the talkable rowers
POTION = (3, 7)
X0, X1 = 1, 16           # the hold's inside, between the bow and stern bulkheads


def wall(s: Scene):
    """Rows 0-1: the starboard hull from inside: deck beams, strakes, frames,
    and the oar ports where the looms go out, bright with the day."""
    B = s.B
    for x in range(X0 * CELL, (X1 + 1) * CELL):
        for y in range(0, 32):
            if y < 3:
                c = "hd0"
            elif y == 3:
                c = "ink"
            else:
                k = (y - 4) % 6
                c = "wd1" if k == 0 else "wd0" if k < 4 else "hd0"
            fx = x % 32
            if fx in (0, 1, 2, 3):                     # a frame
                c = {0: "ink", 1: "pk1", 2: "wd1", 3: "ink"}[fx] if y > 3 else c
            B.px(x, y, c)
        B.px(x, 31, "ink")
    # the oar ports, two to a bench's width, where the looms go out
    for cx in range(X0, X1 + 1):
        for px in (cx * CELL + 3, cx * CELL + 11):
            B.blit(["kkkkk", "kFFfk", "kFFfk", "kFffk", "kkkkk"], {"k": "ink", "F": "fc", "f": "lt1"},
                   px, 22)


# Each tier's seats: a seat block with a cushion every 16 px, its oar's loom
# angled up (or, on the port bank, down) through the tiers to its port.
TIERS_N = (2, 3, 4)          # thranites, zygites, thalamites, top to bottom
TIER_S = 7                   # the port bank's bottom tier


def bench_row(s: Scene, row):
    """The step of the tier: dark between the seats, a riser below."""
    B = s.B
    y0 = row * CELL
    for x in range(X0 * CELL, (X1 + 1) * CELL):
        for y in range(y0, y0 + CELL):
            k = y - y0
            if k < 9:
                c = "hd0" if k < 8 else "ink"
            elif k == 9:
                c = "pk1"
            else:
                c = "wd0" if k < 13 else "hd0"
                if x % 16 in (7, 8):
                    c = "wd1" if x % 16 == 7 else "ink"      # the tier's posts
            B.px(x, y, c)


def seat(s: Scene, cx, row, cushion=True):
    B = s.B
    x, y0 = cx * CELL, row * CELL
    B.blit([
        " kkkkkkkkkkkk ",
        "kPPPPPPPPPPPPk",
        "kppppppppppppk",
        "kwwwwwwwwwwwwk",
        "kwk        kwk",
        " k          k ",
    ], {"k": "ink", "P": "pk3", "p": "pk2", "w": "wd1"}, x + 1, y0 + 3)
    if cushion:
        c = ("rd", "rd0") if cx % 2 else ("b1", "b0")
        B.blit([" kkkkk ", "kcccccC", "kCCCCCk"], {"k": "ink", "c": c[0], "C": c[1]}, x + 2, y0 + 1)


def loom(s: Scene, cx, row, up=True):
    """An oar's loom from its seat's handle, angled through the tiers to its port."""
    B = s.B
    x0, y0 = cx * CELL + 12, row * CELL + 6
    end = 25 if up else PH
    k = 0
    while True:
        y = y0 - k if up else y0 + k
        if (up and y < end) or (not up and y >= end):
            break
        x = x0 - k // 2
        B.px(x, y, "pk2")
        B.px(x + 1, y, "wd1")
        k += 1
    B.blit(["kPk", "kpk"], {"k": "ink", "p": "pk2", "P": "pk3"}, x0 - 1, y0)


def tiers(s: Scene):
    for row in TIERS_N + (TIER_S,):
        bench_row(s, row)
    for row in TIERS_N + (TIER_S,):
        for cx in range(X0, X1 + 1):
            if cx == LADDER[0] and row < LADDER[1]:
                continue
            empty = (cx, row) in SEATS or (cx, row) == POTION
            seat(s, cx, row, cushion=True)
            if not empty:
                loom(s, cx, row, up=row != TIER_S)
            if (cx, row) == POTION:
                for x in range(cx * CELL + 4, cx * CELL + 12):
                    for y in range(row * CELL + 9, row * CELL + 13):
                        s.B.px(x, y, "ink")


def gangway(s: Scene):
    B = s.B
    for x in range(X0 * CELL, (X1 + 1) * CELL):
        for y in range(5 * CELL, 7 * CELL):
            r = (y // 4) % 4
            yy = y % 4
            joint = (r * 5 + 3) % 16
            c = "wd1" if yy == 3 or (x - joint) % 16 == 0 else "pk1"
            if yy == 0 and c == "pk1":
                c = "pk2"
            if y == 5 * CELL:
                c = "ink"
            if y in (5 * CELL + 1, 5 * CELL + 2):
                c = "wd0"                               # shadow under the bottom tier
            B.px(x, y, c)
    # the light falling through the hatch onto the gangway
    lx = LADDER[0] * CELL
    for x in range(lx, lx + 16):
        for y in range(5 * CELL + 3, 7 * CELL):
            c = B.get(x, y)
            edge = x < lx + 2 or x > lx + 13
            if c == "pk1":
                B.px(x, y, "pk2" if edge else "pk3")
            elif c == "pk2":
                B.px(x, y, "pk3" if edge else "lt1")
            elif c == "wd1" and not edge:
                B.px(x, y, "pk2")


def ladder(s: Scene):
    """The ladder up to the hatch, over the tiers at the ladder's column, with
    daylight in the opening above (top layer above the gangway: walk behind)."""
    B, T = s.B, s.T
    x0 = LADDER[0] * CELL
    # the shaft of light down the ladder's column
    for y in range(0, 5 * CELL):
        for x in range(x0, x0 + 16):
            c = "lt1" if (x + y) % 2 else "pk3"
            if y < 4:
                c = "fc"
            B.px(x, y, c)
    for y in range(0, 5 * CELL + 10):
        layer = B if y < 5 * CELL else T
        for x in (x0 + 2, x0 + 12):
            layer.px(x, y, "ink")
            layer.px(x + 1, y, "pk3")
            layer.px(x + 2, y, "wd1")
        if y % 8 == 3:
            for x in range(x0 + 4, x0 + 12):
                layer.px(x, y, "pk2" if y < 5 * CELL else "pk3")
                layer.px(x, y + 1, "wd0")


def mast(s: Scene):
    """The mast down through the hold to its step on the keel."""
    B, T = s.B, s.T
    x0 = MAST * CELL + 5
    for y in range(0, 6 * CELL + 6):
        layer = B if y < 5 * CELL else T
        for dx, c in ((0, "ink"), (1, "pk1"), (2, "pk3"), (3, "pk2"), (4, "wd1"), (5, "ink")):
            layer.px(x0 + dx, y, c)
    step = [
        "  kkkkkkkkkkk   ",
        " kwwkpPPpkwwk   ",
        "kpppkpPPpkpppk  ",
        "kPPPkpPPpkPPPk  ",
        "kwwwwkkkkwwwwk  ",
        " kkkkkkkkkkkk   ",
    ]
    B.blit(step, {"k": "ink", "w": "wd0", "p": "pk2", "P": "pk3"}, MAST * CELL + 1, 6 * CELL + 6)


def bulkheads(s: Scene):
    """The bow and stern ends: dark timber, frames converging."""
    B = s.B
    for cx in (0, W - 1):
        for x in range(cx * CELL, cx * CELL + CELL):
            for y in range(0, PH):
                inner = (x - cx * CELL) if cx == 0 else (cx * CELL + 15 - x)
                c = "hd0" if inner < 12 else "wd0"
                if inner in (12, 13):
                    c = "ink" if inner == 13 else "wd1"
                if inner == 6 and y % 8 < 6:
                    c = "wd0"
                B.px(x, y, c)


def stores(s: Scene):
    """Water jars and rope at the bow end; a pithos and a lamp at the stern."""
    B, M = s.B, s.M
    jar = [
        "  kkkk  ",
        "  k33k  ",
        " kk22kk ",
        "k3222211",
        "k3222211",
        "k3222211",
        "k3222111",
        " k22111k",
        "  k211k ",
        "  k11k  ",
        "   kk   ",
    ]
    for (x, y) in ((1 * CELL + 1, 5 * CELL + 3), (1 * CELL + 8, 5 * CELL + 4),
                   (2 * CELL + 2, 5 * CELL + 3)):
        M.blit(jar, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, x, y)
    coil = [
        "  kkkkkkk  ",
        " krrRrrrrk ",
        "krkkkkkkkrk",
        "krkrrrrrkrk",
        "krkkkkkkkrk",
        " krrrrRrrk ",
        "  kkkkkkk  ",
    ]
    M.blit(coil, {"k": "ink", "r": "rp", "R": "rp1"}, 2 * CELL + 3, 6 * CELL + 6)
    pithos = [
        "   kkkkkkkk   ",
        "  k3333333k   ",
        " kkkkkkkkkkk  ",
        "k32222222211k ",
        "k32222222211k ",
        "k32222222111k ",
        "k32222222111k ",
        " k322222111k  ",
        " k322221111k  ",
        "  k2221111k   ",
        "  k2211111k   ",
        "   k21111k    ",
        "    kkkkk     ",
    ]
    M.blit(pithos, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, 16 * CELL + 1, 5 * CELL + 2)
    lamp = [
        "   k    ",
        "   k    ",
        "  kfk   ",
        " kfFfk  ",
        "kppppppk",
        " kpppk  ",
        "  kkk   ",
    ]
    M.blit(lamp, {"k": "ink", "f": "lt1", "F": "fc", "p": "pk2"}, 15 * CELL + 6, 4 * CELL + 6)


def bilge(s: Scene):
    """Row 8: the port tier's riser and the dark of the bilge below the benches."""
    B = s.B
    for x in range(X0 * CELL, (X1 + 1) * CELL):
        for y in range(8 * CELL, PH):
            k = y - 8 * CELL
            c = "wd0" if k < 3 else "hd0" if k < 12 else "ink"
            if x % 16 in (14, 15) and k < 10:
                c = "wd1" if x % 16 == 14 else "ink"
            B.px(x, y, c)


def draw():
    s = Scene("hold", W, H)
    wall(s)
    gangway(s)
    bilge(s)
    tiers(s)
    mast(s)
    ladder(s)
    bulkheads(s)
    stores(s)
    # the bottom edge of the port tiers in shadow
    for x in range(PW):
        for y in range(PH - 3, PH):
            if s.B.get(x, y) is not None:
                s.B.px(x, y, "hd0" if y < PH - 1 else "ink")
    s.flatten()
    walkability(s)
    return s


def void():
    """The dark outside the hold's walls: its layout's border."""
    s = Scene("void", 1, 1)
    s.B.rect(0, 0, CELL, CELL, "ink")
    s.piece("void", "The dark beyond the hold", 0, 0, 1, 1, "The hold's border.")
    return s


def walkability(s: Scene):
    for y in range(H):
        for x in range(W):
            s.walk[y][x] = "X"
    for y in (5, 6):
        for x in range(3, 16):
            s.walk[y][x] = "."
    s.walk[6][MAST] = "X"
    s.set_walk(*LADDER, "w", "MB_LADDER")
    s.piece("hold_wall", "The starboard hull from inside", 1, 0, 2, 2,
            "Deck beams, strakes, frames every 32 px, two rows of oar ports with the daylight "
            "in them. Solid.")
    s.piece("benches", "The three tiers of rowers' benches", 1, 2, 2, 3,
            "Thranites (row 2), zygites (row 3), thalamites (row 4): a seat with its cushion "
            "every 16 px, its oar's loom angled up through the tiers to its port. Solid. Row 7 "
            "is the port bank's bottom tier, its looms angled down; row 8 the bilge.")
    s.piece("empty_seat", "A seat without its oar", 5, 4, 1, 1,
            "A cushion and no loom: a talkable rower's object event sits here. Also at (13,4), "
            "(9,7) and (14,7).")
    s.piece("seat_potion", "The port bottom bench with a gap under it", POTION[0], POTION[1], 1, 1,
            "The Potion's item jar goes here.")
    s.piece("gangway", "The gangway", 3, 5, 2, 2, "Walkable, rows 5-6.")
    s.piece("ladder", "The ladder up to the hatch", LADDER[0], 2, 1, 4,
            "Daylight down the ladder's column. The foot (11,5) is MB_LADDER: the warp.")
    s.piece("hold_mast", "The mast and its step", MAST, 0, 1, 7, "The step (8,6) is solid.")
    s.piece("hold_stores", "Water jars and rope", 1, 5, 2, 2, "Solid.")
    s.piece("pithos_lamp", "A pithos and a hanging lamp", 15, 4, 2, 3, "Solid.")
