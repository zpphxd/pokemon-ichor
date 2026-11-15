#!/usr/bin/env python3
"""Arkadia's homes: Nyktimos's hearth hall with its empty place, Hippothoos's
charcoal-burner's hut dug into the hill, and Krotos's house that is half a
byre. Registered into arkrooms_art.STAMPS on import."""
import math

from arkrooms_art import Canvas, stamp, noise

# ---------------------------------------------------------------------------
# Nyktimos's hall
# ---------------------------------------------------------------------------


def _wolf_pelt():
    """3x2 on the wall: a great grey wolf's pelt spread over the hearth, head
    up, forelegs and hindlegs stretched out, the tail hanging. Lykaon."""
    c = Canvas(48, 32)
    # body
    for y in range(6, 27):
        for x in range(10, 38):
            nx, ny = (x - 23.5) / 11.5, (y - 16.5) / 10.5
            if nx * nx + ny * ny <= 1.0:
                c.put(x, y, "s")
    # legs to the four corners
    for (sx, sy, ex, ey) in [(14, 10, 3, 4), (33, 10, 44, 4), (14, 23, 4, 29), (33, 23, 43, 29)]:
        for t in range(0, 21):
            x = round(sx + (ex - sx) * t / 20)
            y = round(sy + (ey - sy) * t / 20)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if abs(dx) + abs(dy) < 2:
                        c.put(x + dx, y + dy, "s")
        c.put(ex, ey, "k")
    # the head at the top
    c.ellipse(23.5, 5, 5, 4, "s")
    for (x, y) in [(19, 1), (20, 0), (21, 1), (26, 1), (27, 0), (28, 1)]:   # ears
        c.put(x, y, "p")
    c.put(21, 5, "k")
    c.put(26, 5, "k")
    c.hline(22, 25, 8, "p")
    c.put(23, 9, "k")
    c.put(24, 9, "k")
    # the tail
    for y in range(26, 32):
        c.put(23, y, "s")
        c.put(24, y, "p")
    # the dark saddle down the back, pale belly fur at the edges, an outline
    for y in range(8, 26):
        for x in range(19, 29):
            if c.get(x, y) == "s" and abs(x - 23.5) < 3 + (y % 3):
                c.put(x, y, "p")
    out = [r[:] for r in c.g]
    for y in range(32):
        for x in range(48):
            if c.g[y][x] == ".":
                if any(0 <= x + dx < 48 and 0 <= y + dy < 32 and c.g[y + dy][x + dx] not in ".k"
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[y][x] = "k"
            elif c.g[y][x] == "s" and noise(x, y, 3) < 0.25:
                out[y][x] = "S"
    c.g = out
    return c


stamp("wolf_pelt", 3, 2, art=[("nature", _wolf_pelt())],
      note="a great grey wolf's pelt over the hearth: the ancestor, Lykaon. Nobody sits under it")


def _hall_hearth():
    """3x2: the hall's hearth against the wall, a wide stone curb, a fire of
    split logs, an iron spit across on two forked irons."""
    c = Canvas(48, 32)
    c.box(1, 8, 46, 29, "S")
    c.hline(2, 45, 9, "t")
    c.hline(2, 45, 28, "s")
    c.rect(5, 12, 42, 26, "a")
    for (x0, x1, y) in [(9, 38, 24), (12, 35, 22)]:
        c.hline(x0, x1, y, "d")
        c.hline(x0, x1, y + 1, "k")
    for x in range(10, 38):
        h = int(4 + 6 * abs(math.sin(x * 0.7)) + (x % 3))
        for y in range(22 - h, 22):
            t = (22 - y) / h
            c.put(x, y, "Y" if t < 0.3 else ("F" if t < 0.65 else "f"))
    # the spit and its forked irons
    for x0 in (4, 43):
        c.vline(x0, 2, 12, "s")
        c.vline(x0 + 1, 2, 12, "k")
        c.put(x0 - 1, 2, "s")
        c.put(x0 + 2, 2, "s")
    c.hline(4, 44, 4, "s")
    c.hline(4, 44, 5, "k")
    return c


stamp("hall_hearth", 3, 2, art=[("clay", _hall_hearth())],
      note="the hall's hearth, a fire of split logs, an iron spit across it")


def _feast_table():
    """5x2: the long table, always laid for one more than the house: four
    places with bread and cups, and at the east end the guest's place, a bowl
    and a cup set out and nothing in them."""
    c = Canvas(80, 32)
    c.box(0, 5, 79, 22, "m")
    c.hline(1, 78, 6, "l")
    for y in (11, 17):
        c.hline(1, 78, y, "d")
    c.box(0, 22, 79, 26, "d")
    for x in (4, 5, 74, 75):
        c.vline(x, 26, 30, "k")
    c.hline(4, 75, 28, "d")
    # four places, used
    for px in (6, 22, 38, 54):
        c.ellipse(px + 4, 10, 4, 2.5, "C", "k")
        c.ellipse(px + 4, 10, 2, 1, "b")
        c.box(px + 1, 14, px + 4, 17, "r")
        c.put(px + 2, 15, "R")
        c.ellipse(px + 9, 15, 2.5, 2, "y", "z")
    # the guest's place: clean, empty, waiting
    c.ellipse(72, 10, 4, 2.5, "c", "k")
    c.ellipse(72, 10, 2, 1, "C")
    c.box(68, 14, 71, 17, "c")
    c.put(69, 15, "C")
    # a big round loaf and a jug in the middle
    c.ellipse(46.5, 18, 4, 3, "b", "k")
    c.hline(44, 49, 17, "y")
    return c


stamp("feast_table", 5, 2, art=[("wood", _feast_table())],
      note="the long table, laid for one more than the house: the last place, a bowl and a cup, waits empty")


def _ladder():
    """1x3 against the wall: the ladder to the sleeping loft, up into the dark
    of its hatch in the ceiling."""
    c = Canvas(16, 48)
    c.rect(1, 0, 14, 7, "k")
    c.hline(0, 15, 8, "d")
    c.hline(0, 15, 9, "m")
    for x in (3, 12):
        c.vline(x, 0, 46, "l")
        c.vline(x + 1, 0, 46, "d")
    for y in range(4, 46, 6):
        c.hline(4, 11, y, "h")
        c.hline(4, 11, y + 1, "m")
    c.hline(2, 13, 47, "k")
    return c


stamp("ladder", 1, 3, art=[("wood", _ladder())], note="the ladder to the sleeping loft")


def _spear_rack():
    """1x2 on the wall: two boar spears with their cross-bars, on pegs."""
    c = Canvas(16, 32)
    for x0 in (4, 10):
        c.vline(x0, 6, 31, "m")
        c.vline(x0 + 1, 6, 31, "d")
        c.paste(x0 - 1, 0, """
.kk.
kCCk
kCck
kCCk
.kk.
""")
        c.hline(x0 - 2, x0 + 3, 7, "k")
    c.box(1, 13, 14, 15, "d")
    return c


stamp("boar_spears", 1, 2, art=[("wood", _spear_rack())], note="two boar spears on pegs")

# ---------------------------------------------------------------------------
# Hippothoos's hut
# ---------------------------------------------------------------------------


def _sacks():
    """2x3: charcoal sacks stacked to the roof, black dust on the sacking, a
    few lumps spilled from a split one."""
    c = Canvas(32, 48)
    rows = [(40, [(0, 15), (16, 31)]), (30, [(4, 19), (18, 31)]), (20, [(0, 14), (13, 28)]),
            (10, [(3, 18), (17, 31)]), (1, [(0, 15), (14, 29)])]
    for (y0, spans) in rows:
        for (x0, x1) in spans:
            for y in range(y0, min(y0 + 10, 48)):
                for x in range(x0, x1 + 1):
                    nx = (x - (x0 + x1) / 2) / ((x1 - x0) / 2 + 0.5)
                    ny = (y - y0 - 5) / 5.2
                    if nx * nx + ny * ny * 0.8 > 1.0:
                        continue
                    edge = nx * nx + ny * ny * 0.8 > 0.75
                    if edge:
                        c.put(x, y, "k" if ny > -0.3 else "d")
                    else:
                        # old sacking gone grey-brown, black dust in the weave
                        n = noise(x, y, 5)
                        if ny < -0.45:
                            c.put(x, y, "j" if n < 0.6 else "K")
                        elif n < 0.22:
                            c.put(x, y, "k")
                        elif n < 0.5 or ny > 0.4:
                            c.put(x, y, "d")
                        else:
                            c.put(x, y, "K")
            c.put((x0 + x1) // 2, y0 + 1, "n")
            c.put((x0 + x1) // 2 + 1, y0 + 1, "n")
            c.put((x0 + x1) // 2, y0 + 2, "K")
    # the split sack and its spill
    for (x, y) in [(22, 44), (24, 45), (21, 46), (26, 46), (23, 47), (19, 47)]:
        c.put(x, y, "k")
        c.put(x + 1, y, "d")
    return c


stamp("charcoal_sacks", 2, 3, art=[("nature", _sacks())],
      note="charcoal sacks stacked to the roof, black with dust")


def _rake():
    """1x3 leaning on the logs: the long iron rake for drawing a kiln, its
    handle worn, its teeth black."""
    c = Canvas(16, 48)
    for y in range(8, 47):
        x = 6 + (y - 8) // 16
        c.put(x, y, "b")
        c.put(x + 1, y, "d")
    c.hline(1, 13, 5, "a")
    c.hline(1, 13, 6, "k")
    for x in range(1, 14, 3):
        c.vline(x, 7, 10, "a")
        c.put(x, 11, "k")
    c.vline(6, 3, 7, "s")
    c.vline(7, 3, 7, "a")
    return c


stamp("iron_rake", 1, 3, art=[("clay", _rake())], note="the long iron rake for drawing a kiln")


def _cot():
    """2x1: a low cot of poles and rawhide, a straw pillow and a dark wool
    blanket thrown over, sooty like everything here."""
    c = Canvas(32, 16)
    c.box(0, 3, 31, 12, "k")
    c.rect(1, 4, 30, 11, "m")
    c.hline(1, 30, 4, "l")
    c.box(2, 4, 8, 10, "C")
    c.hline(3, 7, 5, "c")
    for y in range(4, 12):                       # the blanket, folded over the foot
        for x in range(11, 31):
            c.put(x, y, "R" if (x + y) % 5 else "d")
    c.hline(11, 30, 4, "r")
    c.vline(11, 4, 11, "k")
    c.put(18, 8, "k")
    c.put(25, 6, "k")
    c.hline(0, 31, 12, "d")
    for x in (1, 30):
        c.vline(x, 13, 14, "k")
    return c


stamp("cot", 2, 1, art=[("wood", _cot())], note="a low cot, a straw pillow, a dark wool blanket")


def _log_pile():
    """2x1: oak and beech logs stacked, waiting for the kiln (rock palette's
    log browns, end grain out)."""
    c = Canvas(32, 16)
    for (cx, cy) in [(4, 12), (10, 12), (16, 12), (22, 12), (28, 12), (7, 7), (13, 7), (19, 7), (25, 7),
                     (10, 2.5), (16, 2.5), (22, 2.5)]:
        c.ellipse(cx, cy, 3, 2.6, "h", "k")
        c.put(int(cx), int(cy), "E")
        c.put(int(cx) + 1, int(cy), "e")
    return c


stamp("log_pile", 2, 1, art=[("rock", _log_pile())], note="logs stacked for the kiln")


def _soot_drawing():
    """2x2 on the wall: a board pegged to the logs and on it, in soot, a kiln
    mound with every vent marked, arrows for the wind."""
    c = Canvas(32, 32)
    c.box(1, 2, 30, 28, "h", "d")
    for y in (8, 15, 22):
        c.hline(2, 29, y, "l")
    for (x, y) in [(3, 4), (28, 4), (3, 26), (28, 26)]:
        c.put(x, y, "k")
    # the mound
    for x in range(5, 27):
        top = 24 - int(14 * math.sin((x - 5) / 21 * math.pi))
        c.put(x, top, "k")
        c.put(x, 24, "k")
    for (x, y) in [(9, 18), (13, 13), (18, 12), (22, 16), (15, 20)]:   # vents
        c.put(x, y, "k")
        c.put(x, y - 1, "d")
        c.put(x + 1, y - 2, "d")
    for x in range(12, 20):                       # the smoke
        c.put(x, 7 - (x % 3 == 0), "d")
    c.hline(4, 8, 5, "k")
    c.put(8, 4, "k")
    c.put(8, 6, "k")
    return c


stamp("soot_drawing", 2, 2, art=[("wood", _soot_drawing())],
      note="a board on the logs and on it, in soot, a kiln mound with all its vents marked")


def _charcoal_heap():
    """1x1: a heap of charcoal lumps by the door, black and grey."""
    c = Canvas(16, 16)
    for (cx, cy, rx, ry) in [(5, 11, 4, 3), (11, 12, 4, 3), (8, 7, 4, 3), (3, 14, 2, 1.5), (13, 9, 2, 2)]:
        c.ellipse(cx, cy, rx, ry, "1", "k")
        c.hline(int(cx - rx / 2), int(cx), int(cy - ry + 1), "3")
        c.put(int(cx), int(cy), "2")
    return c


stamp("charcoal_heap", 1, 1, art=[("rock", _charcoal_heap())], note="a heap of charcoal by the door")


def _sacking():
    """2x1 at the door: a doormat of old sacking, black at the edges. Both
    cells are the exit."""
    c = Canvas(32, 16)
    c.box(2, 3, 29, 13, "j", "K")
    for y in range(4, 13):
        for x in range(3, 29):
            if (x + y * 2) % 4 == 0:
                c.put(x, y, "K")
    for x in range(3, 29, 5):
        c.put(x, 12, "d")
    return c


stamp("sacking_mat", 2, 1, art=[("nature", _sacking())], walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"},
      note="a doormat of old sacking; both cells are the exit")


def _bucket():
    """1x1: a wooden water bucket, for when the kiln catches."""
    c = Canvas(16, 16)
    c.box(3, 5, 12, 14, "m")
    c.ellipse(7.5, 5.5, 4.5, 2, "u", "k")
    for y in (8, 12):
        c.hline(3, 12, y, "d")
    c.put(5, 5, "U")
    return c


stamp("bucket", 1, 1, art=[("wood", _bucket())], note="a water bucket, for when the kiln catches")

# ---------------------------------------------------------------------------
# Krotos's house and byre
# ---------------------------------------------------------------------------


def _rail(kind):
    """1x1: the wooden rail that divides house from byre, running north-south:
    a post cap and two rails seen from above. kind: post, rail, end."""
    c = Canvas(16, 16)
    for x in (6, 9):
        c.vline(x, 0, 15, "l")
        c.vline(x + 1, 0, 15, "d")
    if kind in ("post", "end"):
        c.box(4, 3, 11, 12, "m")
        c.rect(5, 4, 10, 6, "h")
        c.rect(5, 7, 10, 11, "l")
        c.hline(4, 11, 12, "k")
    if kind == "end":
        for y in range(13, 16):
            for x in range(4, 12):
                c.put(x, y, ".")
    return c


stamp("rail_post", 1, 1, art=[("wood", _rail("post"))], note="a post of the rail between house and byre")
stamp("rail", 1, 1, art=[("wood", _rail("rail"))], note="the rail between house and byre")
stamp("rail_end", 1, 1, art=[("wood", _rail("end"))], note="the rail's last post, by the gap")

KID = {
    "white": """
..........
...k..k...
..kwkkwk..
.kwwwwwwk.
kwkwwwwwwk
kwwwwwwwwk
.kwwnwwwwk
..kkkkkkk.
""",
    "brown": """
..........
..k...k...
.kmk.kmk..
.kmmmmmmkk
kmkmmmmmmk
kmmmmdmmmk
.kmmmmmmdk
..kkkkkkk.
""",
}


def _kids(which):
    """1x1: kid goats curled up asleep in the straw."""
    c = Canvas(16, 16)
    if which == "pair":
        c.paste(0, 3, KID["white"])
        c.paste(6, 7, KID["brown"])
    else:
        c.paste(3, 5, KID["brown" if which == "brown" else "white"])
    return c


stamp("kids_pair", 1, 1, art=[("nature", _kids("pair"))], note="two kid goats asleep in the straw")
stamp("kid_brown", 1, 1, art=[("nature", _kids("brown"))], note="a brown kid asleep in the straw")


def _cheese_press():
    """1x2: a cheese press: a beam weighted with a stone over a basket mould,
    whey dripping into a bowl. Wood throughout; the stone is its darkest."""
    c = Canvas(16, 32)
    for x0 in (2, 12):
        c.vline(x0, 4, 30, "m")
        c.vline(x0 + 1, 4, 30, "d")
    c.box(1, 6, 14, 9, "l")
    c.hline(2, 13, 7, "h")
    c.ellipse(7.5, 4, 4.5, 3.5, "d", "k")
    c.put(6, 2, "m")
    c.box(4, 14, 11, 22, "C")
    for y in range(15, 22, 2):
        c.hline(5, 10, y, "c")
    c.box(4, 22, 11, 24, "m")
    c.ellipse(7.5, 27, 4, 2, "c", "k")
    c.put(7, 25, "c")
    return c


stamp("cheese_press", 1, 2, art=[("wood", _cheese_press())],
      note="a cheese press, a stone on its beam, whey dripping into a bowl")


def _syrinx():
    """1x1 on the wall: Krotos's syrinx, seven reeds bound with cord, on a peg."""
    c = Canvas(16, 16)
    for i in range(7):
        x = 4 + i
        top = 3
        bottom = 13 - i
        for y in range(top, bottom + 1):
            c.put(x, y, "J" if i % 2 == 0 else "j")
        c.put(x, top, "K")
        c.put(x, bottom + 1, "k")
    for x in range(3, 12):
        c.put(x, 6, "n")
        c.put(x, 9, "n")
    c.put(7, 1, "k")
    c.put(7, 2, "n")
    return c


stamp("syrinx", 1, 1, art=[("nature", _syrinx())], note="a syrinx on a peg, seven reeds bound with cord")


def _pan_mask():
    """1x1 on the wall: a wooden mask of Pan, horned and grinning, over the
    byre's door."""
    c = Canvas(16, 16)
    c.paste(1, 0, """
k............k
kdk........kdk
.kmk......kmk.
..kmkkkkkkmk..
...kmllllmk...
..kmlkllklmk..
..kmlklrklmk..
..kmllllllmk..
..kmlllmllmk..
..kmkkkkkkmk..
...kmckcckmk..
...kmkkkkkmk..
....kmdddmk...
.....kmmmk....
......kkk.....
""")
    return c


stamp("pan_mask", 1, 1, art=[("wood", _pan_mask())], note="a wooden mask of Pan, horned and grinning")


def _back_door():
    """1x2 in the byre wall: the back door to the pasture, planks and a bar."""
    c = Canvas(16, 32)
    c.box(1, 4, 14, 31, "m")
    for x in (4, 7, 10):
        c.vline(x, 5, 30, "d")
    c.hline(2, 13, 5, "l")
    c.box(0, 16, 15, 18, "d")
    c.hline(1, 14, 17, "l")
    c.put(11, 24, "k")
    c.hline(0, 15, 3, "k")
    return c


stamp("back_door", 1, 2, art=[("wood", _back_door())], note="the byre's back door to the pasture, barred")


def _hay_rack():
    """2x1 on the wall: a wicker hay rack, stuffed."""
    c = Canvas(32, 16)
    c.box(1, 2, 30, 13, "K")
    for x in range(3, 30, 4):
        c.vline(x, 3, 12, "j")
    for y in range(3, 9):
        for x in range(2, 30):
            if noise(x, y, 4) < 0.6:
                c.put(x, y, "J" if noise(x, y, 5) < 0.6 else "v")
    c.hline(1, 30, 13, "k")
    return c


stamp("hay_rack", 2, 1, art=[("nature", _hay_rack())], note="a wicker hay rack, stuffed full")


def _trough():
    """2x1: a stone water trough for the goats (rock palette, the water its
    wet sheens)."""
    c = Canvas(32, 16)
    c.box(1, 3, 30, 13, "7")
    c.hline(2, 29, 4, "8")
    c.rect(4, 6, 27, 10, "2")
    for x in range(5, 27, 4):
        c.put(x, 7, "4")
        c.put(x + 1, 8, "5")
    c.hline(1, 30, 13, "6")
    c.hline(1, 30, 14, "k")
    return c


stamp("trough", 2, 1, art=[("rock", _trough())], note="a stone water trough for the goats")


def _bed():
    """2x2: Krotos's bed, a frame of rough poles heaped with goatskins, a
    rolled blanket for a pillow. Seen from the foot."""
    c = Canvas(32, 32)
    c.box(1, 3, 30, 27, "k")
    c.rect(2, 4, 29, 25, "m")
    c.vline(2, 4, 26, "l")
    c.vline(29, 4, 26, "d")
    # two goatskins over the bed, shaggy edges, one white, one brown
    for (cx, cy, rx, ry, main, dark) in ((15.5, 12, 12, 7, "c", "C"), (15.5, 20, 12, 5, "l", "d")):
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                r = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if r > 1.0 + (noise(x, y, 3) - 0.5) * 0.3:
                    continue
                c.put(x, y, dark if (r > 0.75 or (x + y * 3) % 7 == 0) else main)
    c.box(4, 4, 27, 8, "u")
    c.hline(5, 26, 5, "U")
    c.hline(5, 26, 7, "u")
    for x in (2, 3, 28, 29):
        c.vline(x, 27, 30, "k")
    c.hline(1, 30, 27, "d")
    return c


stamp("fleece_bed", 2, 2, art=[("wood", _bed())], note="a bed of rough poles heaped with goatskins")


def _milk_pails():
    """1x1: two wooden milk pails, one full."""
    c = Canvas(16, 16)
    for (x0, full) in ((1, True), (8, False)):
        c.box(x0, 6, x0 + 6, 14, "m")
        c.ellipse(x0 + 3, 6, 3.2, 1.6, "c" if full else "d", "k")
        c.hline(x0, x0 + 6, 9, "d")
        c.hline(x0, x0 + 6, 12, "d")
        c.put(x0 + 3, 3, "k")
        c.put(x0 + 1, 4, "k")
        c.put(x0 + 5, 4, "k")
    return c


stamp("milk_pails", 1, 1, art=[("wood", _milk_pails())], note="two milk pails, one full")


def _bear_rug():
    """2x1, walkable: an old brown bearskin before the hearth, head to the
    left, paws out."""
    c = Canvas(32, 16)
    for y in range(16):
        for x in range(32):
            r = ((x - 17) / 12) ** 2 + ((y - 8) / 5.5) ** 2
            if r <= 1.0:
                c.put(x, y, "d" if r > 0.7 or (x + y) % 6 == 0 else "m")
    for (px, py) in [(8, 2), (8, 13), (26, 2), (26, 13)]:
        c.ellipse(px, py, 2.5, 2, "d", "k")
    c.ellipse(4.5, 8, 4, 3.5, "m", "k")
    c.put(3, 7, "k")
    c.put(1, 8, "k")
    c.put(5, 5, "d")
    c.put(5, 11, "d")
    return c


stamp("bear_rug", 2, 1, art=[("nature", _bear_rug())], walk={(0, 0), (1, 0)},
      note="an old bearskin before the hearth")
