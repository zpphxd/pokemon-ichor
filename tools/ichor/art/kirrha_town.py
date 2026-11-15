"""The harbor towns' houses, for gTileset_Kirrha: a kit of one-cell parts.

A house is a terracotta roof (two rows: ridge and eaves) over one or two
storeys, each a strip of parts: left corner, wall, window, door, right
corner, and the households' own signs (the inn's painted ship-and-mule
board, the sweeper's brooms, the muleteer's harness and bells). Kirrha's
houses are limewashed with laurel-green shutters and grey stone quoins;
Aigion's are the same parts in ochre stucco with blue shutters (the "clay2"
recolor, which costs no tiles). The map builder composes each household
from these parts (RECIPES, by name), every one different. Plus the
muleteer's lean-to stable.
"""
from __future__ import annotations

import kirrha_lib as KL
from kirrha_lib import struct

SEC = "town"


def _wall(L, x0, y0, w=16, h=16):
    KL.stucco(L, x0, y0, w, h, base="lm2", lit="lm3", shade="lm1")


def _quoins(L, x, y0, h, right=False):
    """Grey stone quoins up a house's corner, alternating long and short."""
    for k, y in enumerate(range(y0, y0 + h, 4)):
        w = 5 if k % 2 == 0 else 3
        x1 = x if not right else x - w + 1
        L.rect(x1, y, w, 3, "pg3")
        L.hline(x1, x1 + w - 1, y + 3, "pg1")
        L.px(x1 if not right else x1 + w - 1, y, "pg3")


def _plinth(L, x0, y, w):
    L.hline(x0, x0 + w - 1, y, "pg3")
    L.hline(x0, x0 + w - 1, y + 1, "pg3")
    L.hline(x0, x0 + w - 1, y + 2, "pg1")
    L.hline(x0, x0 + w - 1, y + 3, "ink")


def _window(L, x, y, big=True):
    """A small dark window with laurel-green shutters folded open."""
    w, h = (6, 7) if big else (4, 5)
    L.rect(x, y, w, h, "ink")
    L.rect(x + 1, y + 1, w - 2, h - 2, "wd0")
    L.hline(x - 1, x + w, y - 1, "pg3")
    L.hline(x - 1, x + w, y + h, "pg1")
    for sx in (x - 3, x + w):
        L.rect(sx, y, 3, h, "dg1")
        L.vline(sx + (0 if sx < x else 2), y, y + h - 1, "dg0")
        L.hline(sx, sx + 2, y + h // 2, "dg0")


def kit():
    """The house parts. Row 0: roof ridge row (left, mid, right); row 1: roof eaves
    row (left, mid, right); row 2: ground storey: left corner, wall, window, door,
    right corner; row 3: upper storey: left corner, wall, window, right corner, and
    the timber balcony."""
    s = struct("house", "House kit: roof, ground storey, upper storey", 5, 4,
               walk=["XXXXX", "XXXXX", "XXXDX", "XXXXX"],
               notes="Limewashed walls, grey quoins and plinth, laurel-green shutters, a "
                     "terracotta roof. Build a house left to right: roof rows (left end, mids, "
                     "right end) over storeys (left corner, walls, windows, the door, right "
                     "corner). The door is MB_NON_ANIMATED_DOOR: put the warp on it.",
               section=SEC)
    M = s.M
    # roof rows 0-1, columns 0-2
    KL.roof(M, 0, 0, 48, 32, ridge=True, eaves=True)
    # the gable ends: a lit verge board on the left, a shaded one on the right
    for y in range(1, 30):
        M.px(1, y, "tc3")
        M.px(46, y, "tc0")
    # the ridge's ends round off over the grass behind
    for x in range(0, 3):
        M.px(x, 0, None)
        M.px(47 - x, 0, None)
    # columns 3-4 of the roof rows: a chimney piece and a ridge with a pot
    KL.roof(M, 48, 0, 32, 32, ridge=True, eaves=True, ends=(False, False))
    M.rect(54, 2, 6, 9, "pg3")
    M.vline(54, 2, 10, "pg1")
    M.vline(59, 2, 10, "ink")
    M.hline(53, 60, 1, "ink")
    M.hline(53, 60, 2, "lm3")
    M.blit([" kk ", "k12k", "k12k", " kk "], {"k": "ink", "1": "tc2", "2": "tc1"}, 70, 2)
    # the roof rows stand on aethos grass, so the hipped corners show the ground
    KL.ground(s, "grass", [(x, y) for y in (0, 1) for x in range(5)])
    # ground storey, row 2 (y 32-47)
    y0 = 32
    _wall(M, 0, y0, 80, 16)
    M.hline(0, 79, y0, "lm0")
    M.hline(0, 79, y0 + 1, "lm1")
    _plinth(M, 0, y0 + 12, 80)
    _quoins(M, 0, y0 + 2, 10)
    _quoins(M, 79, y0 + 2, 10, right=True)
    M.vline(0, y0, y0 + 15, "ink")
    M.vline(79, y0, y0 + 15, "ink")
    _window(M, 37, y0 + 4)
    # the door (cell 3): a plank door under a stone lintel, a step
    dx = 48
    M.rect(dx + 3, y0 + 2, 10, 2, "pg3")
    M.hline(dx + 3, dx + 12, y0 + 4, "pg1")
    M.rect(dx + 4, y0 + 5, 8, 11, "ink")
    M.rect(dx + 5, y0 + 6, 6, 10, "wd1")
    M.vline(dx + 8, y0 + 6, y0 + 15, "wd0")
    M.px(dx + 9, y0 + 11, "pg3")
    M.hline(dx + 3, dx + 12, y0 + 15, "pg3")
    # the right corner (cell 4) is a wall with its quoins already drawn
    # upper storey, row 3 (y 48-63): wall, a beam at the floor line, small windows,
    # and the balcony in cell 4
    y1 = 48
    _wall(M, 0, y1, 64, 16)
    M.hline(0, 63, y1, "lm0")
    M.hline(0, 63, y1 + 14, "wd1")
    M.hline(0, 63, y1 + 15, "wd0")
    for x in range(2, 64, 8):
        M.px(x, y1 + 14, "wd0")
    _quoins(M, 0, y1 + 1, 13)
    _quoins(M, 63, y1 + 1, 13, right=True)
    M.vline(0, y1, y1 + 15, "ink")
    M.vline(63, y1, y1 + 15, "ink")
    _window(M, 37, y1 + 4, big=False)
    # the balcony: timber posts and rail across a wall, a pot of basil
    _wall(M, 64, y1, 16, 16)
    M.hline(64, 79, y1, "lm0")
    M.rect(64, y1 + 9, 16, 2, "wd1")
    M.hline(64, 79, y1 + 9, "wd0")
    for x in (65, 70, 75):
        M.vline(x, y1 + 11, y1 + 15, "wd0")
    M.hline(64, 79, y1 + 15, "wd0")
    M.rect(70, y1 + 5, 5, 4, "tc1")
    M.hline(69, 75, y1 + 4, "dg1")
    M.px(71, y1 + 3, "dg0")
    M.px(73, y1 + 3, "dg1")
    s.names = {
        "roof_l": (0, 0), "roof_m": (1, 0), "roof_r": (2, 0), "roof_chimney": (3, 0),
        "roof_pot": (4, 0),
        "eave_l": (0, 1), "eave_m": (1, 1), "eave_r": (2, 1), "eave_m2": (3, 1), "eave_m3": (4, 1),
        "wall_l": (0, 2), "wall": (1, 2), "window": (2, 2), "door": (3, 2), "wall_r": (4, 2),
        "up_l": (0, 3), "up": (1, 3), "up_window": (2, 3), "up_r": (3, 3), "balcony": (4, 3),
    }
    return s


def signs():
    """The households' signs, each a ground-storey wall cell: the inn's painted
    ship-and-mule board on a bracket, the sweeper's brooms, the muleteer's harness
    and bells, and a votive niche with a lamp."""
    s = struct("house_signs", "House kit: the households' signs", 4, 1, walk=["XXXX"],
               notes="Ground-storey wall cells: the inn's sign (a ship and a mule, 'WE TAKE "
                     "YOU ALL THE WAY'), the old sweeper's brooms leaning by her door, the "
                     "muleteer's harness and bells, a niche with an oil lamp.", section=SEC)
    M = s.M
    _wall(M, 0, 0, 64, 16)
    M.hline(0, 63, 0, "lm0")
    M.hline(0, 63, 1, "lm1")
    _plinth(M, 0, 12, 64)
    # the inn's board: a bracket and a hanging painted board
    M.hline(2, 13, 2, "wd0")
    M.vline(3, 2, 4, "wd0")
    M.vline(12, 2, 4, "wd0")
    M.rect(1, 4, 14, 8, "wd1")
    M.rect(2, 5, 12, 6, "lm3")
    M.blit(["  k    ", " kkk   ", "ttttt  ", " ttt   "], {"k": "ink", "t": "tc1"}, 3, 6)
    M.blit(["kk ", "kkk", "k k"], {"k": "wd0"}, 10, 7)
    M.px(12, 6, "wd0")
    # brooms: two leaning, their straw heads down
    for bx, tilt in ((19, 1), (25, -1)):
        M.line(bx, 1, bx + 3 * tilt, 9, "wd1")
        M.blit([" 33 ", "3232", "2323", "3232"], {"3": "tc3", "2": "tc2"}, bx + 3 * tilt - 1, 9)
    M.px(29, 5, "wd0")
    M.hline(28, 30, 4, "wd0")
    # harness and bells: a collar on a peg, a strap of bells
    M.px(39, 2, "wd0")
    M.ellipse(34, 3, 44, 11, "wd0")
    M.ellipse(36, 5, 42, 9, "lm2")
    M.vline(45, 2, 10, "wd0")
    for by in (4, 7, 10):
        M.blit(["k", "3"], {"k": "ink", "3": "tc3"}, 46, by)
    # votive niche with a lamp
    M.rect(52, 3, 8, 8, "lm0")
    M.rect(53, 4, 6, 7, "ink")
    M.rect(54, 8, 4, 2, "tc1")
    M.px(55, 7, "tc3")
    M.px(56, 6, "tc2")
    M.hline(51, 60, 11, "pg3")
    s.names = {"inn_sign": (0, 0), "brooms": (1, 0), "harness": (2, 0), "niche": (3, 0)}
    return s


def stable():
    """The muleteer's lean-to: a timber stable against his house's end wall, a mule
    looking out over the half-door, hay. 2x2."""
    s = struct("stable", "The muleteer's lean-to stable", 2, 2, walk=["XX", "XX"],
               notes="A timber lean-to with a pan-tile roof against the muleteer's house, a "
                     "mule (Onotis) over the half-door, a hay rack. Row 0: roof; row 1: front.",
               section=SEC)
    KL.ground(s, "grass")
    M = s.M
    KL.roof(M, 0, 2, 32, 14, ridge=False, eaves=True)
    for y in range(2, 9):
        for x in range(0, 9 - y):
            M.px(31 - x, y, None)
    # front: posts, half-door, the mule's head, hay
    for y in range(16, 32):
        for x in range(0, 32):
            X = x % 5
            M.px(x, y, "wd2" if X else "wd1")
    M.hline(0, 31, 16, "ink")
    M.rect(4, 17, 14, 8, "ink")
    M.rect(4, 25, 14, 6, "wd1")
    M.hline(4, 17, 25, "wd3")
    M.blit(["  kk    ", " kwwk   ", "kwwwwk  ", "kwwwwwk ", " kwwk k ", "  kk    "],
           {"k": "ink", "w": "sa0"}, 7, 19)
    M.px(8, 18, "wd0")
    M.px(11, 18, "wd0")
    M.rect(21, 20, 9, 9, "oc1")
    for x in range(21, 30, 2):
        M.vline(x, 20, 28, "wd3")
    M.hline(20, 30, 19, "wd0")
    M.hline(0, 31, 31, "ink")
    return s


def build():
    k = kit()
    sg = signs()
    k2 = KL.recolor(k, KL.AIGION, key="house_aigion",
                    title="House kit, Aigion: ochre stucco, blue shutters",
                    notes="The kit, slot for slot, in Aigion's ochre and blue (the same tiles "
                          "in the clay2 palette).")
    sg2 = KL.recolor(sg, KL.AIGION, key="house_signs_aigion",
                     title="House kit, Aigion: the households' signs",
                     notes="The signs in Aigion's ochre and blue.")
    return [k, sg, stable(), k2, sg2]


# Households, by part name: each row left to right, top row first. The map
# builder places them; every house has its own shape.
RECIPES = {
    # Strophios's pilgrims' inn: two storeys, five wide, the board by the door
    "inn": [["roof_l", "roof_chimney", "roof_m", "roof_m", "roof_r"],
            ["eave_l", "eave_m", "eave_m2", "eave_m", "eave_r"],
            ["up_l", "up_window", "balcony", "up_window", "up_r"],
            ["wall_l", "window", "inn_sign", "door", "wall_r"]],
    # the muleteer: one storey, four wide, harness by the door (the stable beside it)
    "muleteer": [["roof_l", "roof_m", "roof_pot", "roof_r"],
                 ["eave_l", "eave_m", "eave_m3", "eave_r"],
                 ["wall_l", "harness", "door", "wall_r"]],
    # Thyia the old sweeper: small, three wide, brooms by the door
    "sweeper": [["roof_l", "roof_m", "roof_r"],
                ["eave_l", "eave_m", "eave_r"],
                ["brooms", "door", "wall_r"]],
    # Tisamenos the old Achaean: narrow and tall, three wide, two storeys
    "achaean": [["roof_l", "roof_chimney", "roof_r"],
                ["eave_l", "eave_m", "eave_r"],
                ["up_l", "up_window", "up_r"],
                ["wall_l", "door", "niche"]],
    # Helike the goatherd: four wide, one storey, against the hillside
    "goatherd": [["roof_l", "roof_m", "roof_m", "roof_r"],
                 ["eave_l", "eave_m3", "eave_m", "eave_r"],
                 ["wall_l", "window", "door", "wall_r"]],
}
