"""Akti's harbor life for gTileset_Akti: the fish stall, the upturned boat,
laundry, octopus drying, a rope coil, a bollard's mooring line and stacked
amphorae.
"""
from __future__ import annotations

import math

from akti_lib import Struct, ground
import kalliste_akti as KA

SEC = "akti"


def fish_stall():
    """A market stall for the catch: a blue-and-white striped awning on two posts,
    and a counter of baskets heaped with fish, octopus and lemons, a tuna in front."""
    s = Struct("fish_stall", "Fish stall with a striped awning", 3, 2, SEC,
               walk=["XXX", "XXX"],
               notes="The fishwife's stall on the quay: a striped awning (row 0) over a "
                     "counter of baskets (row 1), on quay paving. She stands beside it.")
    B, M = s.B, s.M
    KA.quay(B, 0, 0, 48, 32)
    # posts
    for x in (2, 44):
        M.rect(x, 4, 2, 26, "wd2")
        M.vline(x - 1, 4, 29, "ink")
        M.vline(x + 2, 4, 29, "ink")
        M.vline(x + 1, 4, 29, "wd1")
    # the awning: stripes running front to back, a scalloped valance
    for x in range(0, 48):
        stripe = (x // 4) % 2
        for y in range(1, 11):
            if stripe == 0:
                c = "w0" if y < 8 else "sl3"
            else:
                c = "b1" if y < 8 else "b2"
            M.px(x, y, c)
    M.hline(0, 47, 0, "ink")
    for x in range(0, 48):
        drop = [3, 2, 1, 1, 2, 3][x % 6]
        for y in range(11, 11 + drop):
            M.px(x, y, "b2" if (x // 4) % 2 else "w0")
        M.px(x, 11 + drop, "ink")
    M.vline(0, 0, 13, "ink")
    M.vline(47, 0, 13, "ink")
    # the counter: planks with a dark foot, baskets on top
    M.rect(0, 20, 48, 12, "wd2")
    M.hline(0, 47, 20, "wd3")
    M.hline(0, 47, 21, "wd3")
    M.hline(0, 47, 31, "ink")
    for x in range(0, 48, 8):
        M.vline(x, 22, 30, "wd1")
    M.vline(0, 20, 31, "ink")
    M.vline(47, 20, 31, "ink")

    def basket(x, y, goods):
        M.blit(["  kkkkkkkk  ", " k33333333k ", "k3232323232k", "k2323232323k",
                "k3232323232k", " k22222222k "], {"k": "ink", "3": "wd3", "2": "wd1"}, x, y)
        M.blit(goods, {"s": "sl3", "S": "w0", "d": "sl2", "k": "ink", "b": "b2", "r": "rd",
                       "o": "tc1", "p": "tc3", "g": "g1"}, x + 1, y - 4)
    basket(2, 16, ["  ssSs  d ", " sSsbsdsdk", "dssSssdsds", " ddsdddsd "])
    basket(18, 16, ["  ppoo    ", " poooop   ", " ooroor p ", "o o oo o o"])
    basket(33, 16, ["  ssSs  d ", " sSsbsdsdk", "dssSssdsds", " ddsdddsd "])
    tuna = [
        "      kkkkkkkkk     ",
        "k   kkSSSSSssssskk  ",
        "kk kSsssssssssddssk ",
        "ksskdddddddddddddddk",
        "kk kdddddddddddddk  ",
        "k   kkkkkkkkkkkk    ",
    ]
    M.blit(tuna, {"k": "ink", "S": "w0", "s": "sl3", "d": "sl2"}, 14, 24)
    return s


def upturned_boat():
    """A small boat turned keel-up on two trestles on the grass, where Diktys mends nets."""
    s = Struct("boat_upturned", "Upturned boat on trestles", 2, 1, SEC,
               walk=["XX"],
               notes="A rowing boat turned keel-up on trestles, on aethos grass. Diktys's "
                     "seat by the south road.")
    ground(s, "grass")
    M = s.M
    for x in range(4, 29):                   # trodden earth under it
        if x % 2 == 0:
            M.px(x, 14, "wd0")
    for x in (6, 24):
        M.vline(x, 9, 14, "wd1")
        M.vline(x + 1, 9, 14, "wd2")
        M.px(x - 1, 14, "wd1")
        M.px(x + 2, 14, "wd1")
    for x in range(2, 30):
        bulge = int(round(2.5 * math.sin(math.pi * (x - 2) / 27)))
        top = 5 - bulge
        for y in range(top, 11):
            c = "w0"
            if y == top:
                c = "wd1"
            elif y == top + 1:
                c = "wd2"
            elif y >= 9:
                c = "b1"
            elif y == 8:
                c = "b2"
            M.px(x, y, c)
        M.px(x, top - 1, "ink")
        M.px(x, 11, "ink")
    M.vline(1, 4, 11, "ink")
    M.vline(30, 4, 11, "ink")
    M.blit([" kk", "kwk", "kbk"], {"k": "ink", "w": "w0", "b": "b0"}, 25, 6)
    return s


def laundry():
    """Washing on a line between two posts: a sheet, a blue chiton, a red cloth."""
    s = Struct("laundry", "Laundry on a line", 3, 1, SEC,
               walk=["XTX"],
               notes="A washing line between two posts over grass. The posts are solid; "
                     "the middle is walkable, and the washing is drawn over the player.")
    ground(s, "grass")
    T = s.T
    for x in (3, 44):
        T.vline(x, 1, 15, "dk")
        T.vline(x + 1, 1, 15, "w3")
        T.px(x, 0, "ink")
        T.px(x + 1, 0, "ink")

    def sag(x):
        return int(round(2 * math.sin(math.pi * (x - 5) / 38)))
    for x in range(5, 44):
        T.px(x, 2 + sag(x), "dk")

    def cloth(x0, w, h, c, hi, lo):
        for x in range(x0, x0 + w):
            for y in range(3 + sag(x), 3 + sag(x) + h + (x % 2)):
                T.px(x, y, hi if x == x0 else (lo if x == x0 + w - 1 else c))
            T.px(x, 3 + sag(x), "w0")
    cloth(7, 9, 9, "w1", "w0", "w2")
    cloth(18, 7, 7, "b1", "b2", "b0")
    cloth(27, 5, 9, "tc1", "tc2", "tc1")
    cloth(34, 7, 5, "w2", "w1", "w3")
    for x in (7, 15, 18, 24, 27, 31, 34, 40):
        T.px(x, 2 + sag(x), "ink")
    return s


def octopus_line():
    """Octopus hung on a line to dry in the sun, between two posts on the quay."""
    s = Struct("octopus_line", "Octopus drying on a line", 2, 1, SEC,
               walk=["XX"],
               notes="Two posts on the quay with octopus hung over the line to dry. "
                     "Quay paving underneath; the octopus are drawn over the player.")
    B, T = s.B, s.T
    KA.quay(B, 0, 0, 32, 16)
    for x in (1, 29):
        T.vline(x, 0, 15, "wd2")
        T.vline(x + 1, 0, 15, "wd1")
        T.px(x, 15, "ink")
        T.px(x + 1, 15, "ink")
    T.hline(3, 28, 1, "ink")
    octo = [" pp ", "pppp", "poop", "pooo", "o o o", "o oo ", " o  o", "o  o "]
    for x0 in (4, 11, 18, 24):
        T.blit(octo, {"p": "tc3", "o": "tc1"}, x0, 2)
        T.px(x0 + 1, 4, "ink")
        T.px(x0 + 2, 4, "ink")
    return s


def rope_coil():
    s = Struct("rope_coil", "A coil of rope on the quay", 1, 1, SEC, walk=["X"],
               notes="A coiled hawser on quay paving.")
    B, M = s.B, s.M
    KA.quay(B, 0, 0, 16, 16)
    for r, c in ((6, "wd1"), (5, "rp"), (4, "wd2"), (3, "rp"), (2, "wd2")):
        M.ellipse(8 - r - 1, 9 - r + 1, 8 + r - 1, 9 + r - 2, c)
    M.ellipse(6, 8, 8, 9, "wd0")
    for k in range(0, 360, 30):
        a = math.radians(k)
        M.px(int(7 + 6 * math.cos(a)), int(8 + 5 * math.sin(a)), "ink")
    M.hline(9, 15, 13, "rp")
    M.hline(9, 15, 14, "wd2")
    return s


def bollard_line():
    """A bollard on the quay's coping with a mooring line running out over the edge."""
    s = Struct("bollard_line", "Bollard with a mooring line", 1, 1, SEC, walk=["X"],
               notes="A stone bollard on the quay's north edge, its line running up to a "
                     "boat moored to the north.")
    B, M = s.B, s.M
    q = KA.harbor_steps()
    for y in range(16):
        for x in range(16):
            B.px(x, y, q.B.get(32 + x, y))
    # replace the old trailing rope with a taut line up off the top edge
    for y in range(16):
        for x in range(16):
            if B.get(x, y) == "e2" and (x >= 12 or y <= 8):
                B.px(x, y, "s4")
    for (x, y) in ((9, 6), (10, 5), (10, 4), (11, 3), (11, 2), (12, 1), (12, 0)):
        M.px(x, y, "rp")
        M.px(x + 1, y, "wd2")
    return s


def amphora_stack():
    """Amphorae laid in a pyramid in a wooden rack, ready to load."""
    s = Struct("amphora_stack", "Amphorae stacked in a rack", 2, 1, SEC, walk=["XX"],
               notes="Transport amphorae laid on their sides in a three-high pyramid, "
                     "on quay paving.")
    B, M = s.B, s.M
    KA.quay(B, 0, 0, 32, 16)
    amph = [
        "  kkkkkkkk ",
        " k3322221kk",
        "k332222211k",
        " k1111111kk",
        "  kkkkkkkk ",
    ]
    key = {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}
    for i in range(3):
        M.blit(amph, key, 1 + i * 10, 10)
    for i in range(2):
        M.blit(amph, key, 6 + i * 10, 6)
    M.blit(amph, key, 11, 2)
    M.hline(0, 31, 15, "wd1")
    return s


def build():
    # (the upturned boat is drawn as an object event: tools/ichor/art/akti_objects.py)
    return [fish_stall(), laundry(), octopus_line(), rope_coil(),
            bollard_line(), amphora_stack()]
