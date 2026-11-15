"""Stone on the mountain: Eleutherai's Cyclopean walls, towers and gate, the
god's roofless temple and its empty plinth, troughs, the shepherds' fold,
boundary stones, the great herm, the ivy shrine (clean and desecrated), the
crags' scattered detail, ivy and marked ivy on rock, cave mouths, the cave's
props, dig spots, and the maenads' dancing floor.

Light from the top left. The fort's stone is drawn on a 32 px repeat (its
blocks are bigger than a cell), so a run of wall alternates two middle cells.
"""
from __future__ import annotations

import numpy as np

import kithairon_ground as G
import kithairon_lib as K

SEC = "stone"
SOUTH_EDGE = "1|11100011"         # a crag cell with rock north, east and west, open south


# --------------------------------------------------------------------------
# Cyclopean masonry
# --------------------------------------------------------------------------

# Polygonal blocks on a 16 x 16 repeat: three or four fitted stones a cell.
_SEEDS = [(4, 3), (12, 4), (8, 10), (1, 12), (14, 13)]


def _cyclo():
    near = np.zeros((16, 16), int)
    gap = np.zeros((16, 16), float)
    for y in range(16):
        for x in range(16):
            ds = []
            for i, (px, py) in enumerate(_SEEDS):
                dx = min(abs(x - px), 16 - abs(x - px))
                dy = min(abs(y - py), 16 - abs(y - py))
                ds.append(((dx * dx * 0.7 + dy * dy * 1.4) ** 0.5, i))
            ds.sort()
            near[y, x] = ds[0][1]
            gap[y, x] = ds[1][0] - ds[0][0]
    return near, gap


_CN, _CG = _cyclo()
_TONES = ["cy3", "cy2", "cy3", "cy2", "cy2"]


def cyclo(x, y, dark=0):
    """Cyclopean masonry at pixel (x, y): huge fitted blocks with dark joints,
    each lit on its upper-left rim and shaded on its lower-right."""
    xx, yy = x % 16, y % 16
    i = _CN[yy, xx]
    g = _CG[yy, xx]
    if g < 0.9:
        return "cy0"
    up = _CN[(yy - 1) % 16, xx] != i or _CN[yy, (xx - 1) % 16] != i
    dn = _CN[(yy + 1) % 16, xx] != i or _CN[yy, (xx + 1) % 16] != i
    tone = _TONES[i]
    if g < 2.0 and up and not dn:
        return "cy4" if not dark else "cy3"
    if g < 2.0 and dn and not up:
        return "cy1"
    if K.hsh(xx, yy, 5) % 17 == 0:
        return "cy1"
    if dark:
        return {"cy3": "cy2", "cy2": "cy1"}[tone]
    return tone


def _wall_cell(L, ox, oy, row, side):
    """One cell of a wall face. row 0: the upper courses under the coping;
    row 1: the lower courses down to the footing."""
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, cyclo(x, y + row * 16, dark=1 if (row == 1 and y > 9) else 0))
    if row == 0:
        for x in range(16):
            L.px(ox + x, oy + 0, "ink")
            L.px(ox + x, oy + 1, "cy4" if (x + 3) % 8 else "cy3")
            L.px(ox + x, oy + 2, "cy3")
            L.px(ox + x, oy + 3, "cy1")
    else:
        for x in range(16):
            L.px(ox + x, oy + 14, "cy0")
            L.px(ox + x, oy + 15, "ink" if x % 3 else "cy0")
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "ink")
            if 0 < y < 14 or row == 0:
                L.px(ox + 1, oy + y, "cy4" if y > 0 else "ink")
    if side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "ink")
            if 0 < y < 14 or row == 0:
                L.px(ox + 14, oy + y, "cy1" if y > 0 else "ink")


def fort():
    """The fort's walls, as parts that snap together on the map:

      W0_*, W1_*   a wall's face seen from the south, two rows (the upper
                   courses under the coping; the lower courses to the footing),
                   L, M (repeats), R
      T0_*, T1_*, T2_*  a square tower, 2 wide: its battlements seen from above,
                   then two rows of face with an arrow slit
      gate_*, gateF_*   the gate, 3 wide: jambs of single stones and the lintel
                   drawn over the player, over the passage (walk through)
      side, side_foot   a wall seen from above, running north, and its end
      slit, door   an arrow slit (W0) and the watch-house door (W1, a door)
    """
    names = {"W0_L": (0, 0), "W0_M": (1, 0), "W0_R": (2, 0), "slit": (3, 0),
             "W1_L": (0, 1), "W1_M": (1, 1), "W1_R": (2, 1), "door": (3, 1),
             "side": (4, 0), "side_foot": (4, 1),
             "T0_L": (5, 0), "T0_R": (6, 0), "T1_L": (5, 1), "T1_R": (6, 1),
             "T2_L": (5, 2), "T2_R": (6, 2),
             "gate_L": (0, 2), "gate_M": (1, 2), "gate_R": (2, 2),
             "gateF_L": (0, 3), "gateF_M": (1, 3), "gateF_R": (2, 3),
             "court": (3, 2)}
    s = K.struct("fort", "Eleutherai's Cyclopean walls, towers and gate", 7, 4, SEC,
                 walk=["XXXXXXX", "XXXDXXX", "XTX.XXX", "X.XXXXX"], names=names,
                 notes="A wall run is W0 over W1: L, then M repeated, then R. A tower "
                       "(T0 over T1 over T2, 2 wide) stands in a run's place with its T0 "
                       "row above the coping. The gate is gate_* over gateF_* (3 wide): "
                       "the passage is the middle column, its lintel drawn over the player. "
                       "`side` is a wall seen from above, running north; `side_foot` ends "
                       "it. `door` (a W1 cell) is the watch-house's door; `slit` an arrow "
                       "slit for W0. `court` is the parade ground's beaten earth (walkable).")
    B, T = s.B, s.T
    for i, side in enumerate("LMR"):
        _wall_cell(B, i * 16, 0, 0, side)
        _wall_cell(B, i * 16, 16, 1, side)
    # slit and door
    _wall_cell(B, 48, 0, 0, "M")
    K.put(B, 48 + 6, 5, ["K44K", "K00K", "K00K", "K00K", "K00K", "K00K", "KccK"],
          {"K": "cy1", "4": "cy4", "0": "ink", "c": "cy3"})
    _wall_cell(B, 48, 16, 1, "M")
    K.put(B, 48 + 2, 16, [
        "KKKKKKKKKKKK",
        "K4444444444K",
        "K3333333333K",
        "KKKKKKKKKKKK",
        "K3K000000K1K",
        "K3K000000K1K",
        "K3K0w00w0K1K",
        "K3K0w00w0K1K",
        "K3K000000K1K",
        "K3K000000K1K",
        "K3K000000K1K",
        "K3K000000K1K",
        "K3K000000K1K",
        "K3K000000K1K",
        "KKKKKKKKKKKK",
    ], {"K": "ink", "4": "cy4", "3": "cy3", "1": "cy1", "0": "cy0", "w": "cy1"})
    s.behaviors[(3, 1)] = "MB_NON_ANIMATED_DOOR"
    # side: a wall top running north, seen from above; side_foot its end face
    for y in range(16):
        for x in range(16):
            if x in (0, 15):
                c = "ink"
            elif x in (1, 2):
                c = "cy4" if (y // 4) % 2 == 0 else "cy3"
            elif x in (13, 14):
                c = "cy2" if (y // 4) % 2 == 0 else "cy1"
            elif x == 3:
                c = "cy1"
            else:
                c = "p3" if K.hsh(x, y, 2) % 6 else "p2"
            B.px(64 + x, y, c)
    _wall_cell(B, 64, 16, 1, "M")
    for y in range(16):
        B.px(64, 16 + y, "ink")
        B.px(79, 16 + y, "ink")
        B.px(65, 16 + y, "cy4")
        B.px(78, 16 + y, "cy1")
    for x in range(64, 80):
        B.px(x, 16, "cy3" if 64 < x < 79 else "ink")
    # the tower: battlements seen from above, then two face rows with a slit
    for y in range(16):
        for x in range(32):
            if x in (0, 31) or y == 0:
                c = "ink"
            elif y >= 13:
                c = ("cy1", "cy4", "cy3")[y - 13]
            elif x < 4 or x > 27 or y < 4:
                merlon = ((x // 4) % 2 == 0) if y < 4 else ((y // 4) % 2 == 0)
                c = ("cy4" if x < 16 else "cy3") if merlon else "cy0"
            else:
                c = "p2" if K.hsh(x, y, 3) % 5 else "p3"
            B.px(80 + x, y, c)
    for row in (1, 2):
        _wall_cell(B, 80, row * 16, 0 if row == 1 else 1, "L")
        _wall_cell(B, 96, row * 16, 0 if row == 1 else 1, "R")
    for x in range(80, 112):
        B.px(x, 16, "cy2")
        B.px(x, 17, "cy2" if x % 2 else "cy1")
    K.put(B, 80 + 14, 21, ["K4K", "K0K", "K0K", "K0K", "K0K", "K0K", "K0K", "KcK"],
          {"K": "cy1", "4": "cy4", "0": "ink", "c": "cy3"})
    # the gate: jambs (L, R) in both rows, the lintel over the passage
    for row in (0, 1):
        _wall_cell(B, 0, 32 + row * 16, row, "L")
        _wall_cell(B, 32, 32 + row * 16, row, "R")
        for y in range(16):
            # the jambs' inner faces: a single huge upright stone each
            for x in range(11, 16):
                B.px(x, 32 + row * 16 + y, ("cy4", "cy3", "cy3", "cy2", "ink")[x - 11])
            for x in range(32, 37):
                B.px(x, 32 + row * 16 + y, ("ink", "cy1", "cy1", "cy2", "cy2")[x - 32])
    # passage floor: dark inside the gate, lighter toward the court
    for y in range(32):
        for x in range(16):
            c = "cy0" if y < 18 else ("cy1" if y < 25 else ("p2" if (x + y) % 5 else "p3"))
            if x in (0, 15):
                c = "cy0"
            B.px(16 + x, 32 + y, c)
    # the lintel, over the player
    for y in range(9):
        for x in range(16):
            c = "ink" if y in (0, 8) else ("cy4" if y < 3 else ("cy3" if y < 6 else "cy2"))
            T.px(16 + x, 32 + y, c)
    # the court: the parade ground's beaten earth
    for y in range(16):
        for x in range(16):
            h = K.hsh(x, y, 8) % 11
            B.px(48 + x, 32 + y, "p3" if h < 7 else ("p2" if h < 10 else "cy2"))
    # unused corners of the sheet: plain wall so there are no holes
    for (cx, cy) in ((3, 3), (4, 2), (4, 3), (5, 3), (6, 3)):
        _wall_cell(B, cx * 16, cy * 16, 1, "M")
    return s


# --------------------------------------------------------------------------
# The god's old temple
# --------------------------------------------------------------------------

def temple():
    """Columns on borrowed paving (aethos's limestone patch is the floor), a
    broken stump, a fallen drum, and the plinth with nothing on it."""
    names = {"col_top": (0, 0), "col": (0, 1), "stump": (1, 1), "drum": (2, 1),
             "plinth": (3, 1), "col_top_g": (4, 0), "col_g": (4, 1), "stump_g": (5, 1),
             "drum_g": (6, 1), "broom": (7, 1)}
    s = K.struct("temple", "The god's roofless temple: columns and the empty plinth", 8, 2, SEC,
                 walk=["T...T...", "XXXXXXX."], names=names,
                 notes="On borrowed road paving (the floor is aethos's limestone patch), "
                       "with `_g` copies on grass for the columns that stand outside it. "
                       "A standing column is `col_top` over `col` (its capital drawn over "
                       "the player). `plinth` is the empty plinth (beat 27): put its sign "
                       "there. `broom` is Oinoe's swept step with her broom leaning on it.")
    K.ground(s, "path", [(c, r) for c in range(4) for r in range(2)] + [(7, 1)])
    K.ground(s, "grass", [(c, r) for c in range(4, 7) for r in range(2)] + [(7, 0)])
    for base in (0, 4):
        M, T = s.M, s.T
        ox = base * 16
        # capital (top layer): a worn Doric echinus and abacus
        K.put(T, ox + 3, 6, [
            "KKKKKKKKKK",
            "K44443333K",
            ".K443331K.",
            "..K4331K..",
            "..K4331K..",
        ], {"K": "ink", "4": "cy4", "3": "cy3", "1": "cy1"})
        for y in range(11, 16):
            for x in range(5, 11):
                T.px(ox + x, y, "cy4" if x < 7 else ("cy3" if x < 9 else "cy2"))
            T.px(ox + 4, y, "ink")
            T.px(ox + 11, y, "ink")
        # shaft with flutes, a base on the floor
        for y in range(16, 30):
            for x in range(5, 11):
                c = ("cy4", "cy3", "cy4", "cy3", "cy2", "cy1")[x - 5]
                if y % 7 == 3 and x > 6:
                    c = "cy1"
                M.px(ox + x, y, c)
            M.px(ox + 4, y, "ink")
            M.px(ox + 11, y, "ink")
        K.put(M, ox + 3, 28, ["KKKKKKKKKK", "K33333331K", "KKKKKKKKKK"],
              {"K": "ink", "3": "cy3", "1": "cy1"})
        # a stump: the shaft broken off at knee height, snapped edge lit
        K.put(M, ox + 16 + 3, 18, [
            "..K4K.K...",
            ".K44433K..",
            "K4333321K.",
            "K4332211K.",
            "K4332211K.",
            "K4332211K.",
            "K4332211K.",
            "K4332211K.",
            "KKKKKKKKKK",
            "K33333331K",
            "KKKKKKKKKK",
        ], {"K": "ink", "4": "cy4", "3": "cy3", "2": "cy2", "1": "cy1"})
        # a fallen drum lying on its side, its flutes showing
        K.put(M, ox + 32 + 1, 20, [
            ".KKKKKKKKKKKK.",
            "K434343434341K",
            "K3434343434311K"[:14],
            "K434343434341K",
            "K3332323232311K"[:14],
            ".KKKKKKKKKKKK.",
        ], {"K": "ink", "4": "cy4", "3": "cy3", "2": "cy2", "1": "cy1"})
        K.put(M, ox + 32 + 12, 21, ["KK", "K1K", "K1K", "KK"], {"K": "ink", "1": "cy2"})
        for x in range(ox + 34, ox + 47):
            if x % 2:
                M.px(x, 27, "gd" if base else "p2")
    # the plinth: a stepped block, swept clean, the dedication cut in its face
    K.put(s.M, 48 + 1, 16 + 1, [
        ".KKKKKKKKKKKK.",
        "K444444444443K",
        "K433333333331K",
        "K433333333331K",
        "KKKKKKKKKKKKKK",
        ".K4333333331K.",
        ".K4100100101K.",
        ".K4333333331K.",
        ".K4101001011K.",
        ".K4333333331K.",
        "KKKKKKKKKKKKKK",
        "K444444444443K",
        "K333333333331K",
        ".KKKKKKKKKKKK.",
    ], {"K": "ink", "4": "cy4", "3": "cy3", "1": "cy1", "0": "cy0"})
    # Oinoe's broom against the step (on grass: the step's edge)
    M = s.M
    for y in range(3, 15):
        M.px(112 + 10 - y // 3, 16 + y, "l0")
    K.put(M, 112 + 3, 16 + 11, [".33.", "3333", "3.33", ".3.3"], {"3": "cy3"})
    for x in range(112 + 1, 112 + 15):
        M.px(x, 16 + 15, "cy1")
    return s


# --------------------------------------------------------------------------
# Troughs, the fold, boundary stones, the great herm, the ivy shrine
# --------------------------------------------------------------------------

def trough():
    s = K.struct("trough", "Stone trough with spring water", 2, 1, SEC, walk=["XX"], on="sea",
                 names={"W": (0, 0), "E": (1, 0)},
                 notes="A long stone trough on borrowed (animated) water, fed by a spout at "
                       "its west end: Eleutherai's spring, Phorbas's fold. Blocks.")
    M = s.M
    g = K.aethos(K.GRASS)
    for y in range(16):
        for x in range(32):
            inside = 4 <= x <= 28 and 5 <= y <= 11
            if not inside:
                M.rgb(x, y, g[y % 16, x % 16])
    for y in range(3, 14):
        for x in range(2, 31):
            inside = 4 <= x <= 28 and 5 <= y <= 11
            if inside:
                continue
            c = "cy4" if y in (3, 4) or x in (2, 3) else ("cy1" if y > 12 or x > 29 else "cy3")
            M.px(x, y, c)
    M.hline(2, 30, 2, "ink")
    M.hline(2, 30, 14, "ink")
    M.vline(1, 3, 13, "ink")
    M.vline(31, 3, 13, "ink")
    # the spout: a little lion's head on a post at the west end
    K.put(M, 0, 0, ["KKK.", "K4K.", "K3K.", "K1K."], {"K": "ink", "4": "cy4", "3": "cy3", "1": "cy1"})
    for x in range(4, 31):
        if x % 2:
            M.px(x, 15, "gd")
    return s


def fold():
    """Phorbas's lean-to: brush thatch on poles over a heap of straw."""
    s = K.struct("leanto", "The shepherds' lean-to", 2, 2, SEC, walk=["XX", "XX"], on="grass",
                 notes="Brush thatch on four poles over straw and a sheepskin, against the "
                       "fold wall. Phorbas sits on the wall beside it.")
    M = s.M
    for y in range(2, 18):
        for x in range(1, 31):
            k = (x * 3 + y * 7) % 5
            c = ("wdy", "wdx", "wdy", "pl1", "wdx")[k]
            if y < 4:
                c = "wdy" if x % 3 else "pl2"
            if y > 15:
                c = "wd0"
            M.px(x, y, c)
    M.hline(1, 30, 1, "ink")
    M.vline(0, 2, 17, "ink")
    M.vline(31, 2, 17, "ink")
    M.hline(1, 30, 18, "ink")
    for y in range(19, 30):
        for x in range(2, 30):
            M.px(x, y, "wd0" if y < 21 else ("pl1" if (x + y) % 3 else "pl2"))
    for px in (2, 28):
        for y in range(18, 31):
            M.px(px, y, "wdx")
            M.px(px + 1, y, "wd0")
    K.put(M, 9, 23, [".pppp.", "p0pp0p", ".pppp."], {"p": "pl3", "0": "pl1"})
    for x in range(2, 30):
        M.px(x, 30, "ink")
        if x % 2:
            M.px(x, 31, "pl0")
    return s


def _place(s, layer, cx, cy, src, rows=1):
    """Copy a 16 x 16*rows temp layer into struct s at cell (cx, cy)."""
    s.layers[layer].a[cy * 16:(cy + rows) * 16, cx * 16:cx * 16 + 16] = src.a


def _shadow(L, x0, x1, y):
    for x in range(x0, x1):
        if x % 2 and not L.a[y, x, 3]:
            L.px(x, y, "gd")


def markers():
    """Boundary stones, the great herm, the ivy shrine clean and desecrated,
    the maenads' drums, Aktaion's rock seat, a boulder, scree and dig spots."""
    names = {"herm_top": (0, 0), "herm": (0, 1), "shrine_top": (1, 0), "shrine": (1, 1),
             "shrine_bad_top": (2, 0), "shrine_bad": (2, 1), "dig": (3, 0), "boundary": (3, 1),
             "dig_cave": (4, 0), "seat": (4, 1), "scree_b": (5, 0), "scree": (5, 1),
             "drum_b": (6, 0), "drum": (6, 1), "boulder": (7, 0)}
    s = K.struct("markers", "Stones and shrines of the mountain", 8, 2, SEC,
                 walk=["TTT...XX", "XXXXX.X."], names=names,
                 notes="On borrowed grass. `herm_top` over `herm`: the great herm, hung with "
                       "ivy. `shrine_top` over `shrine`: the little rock shrine of Dionysus "
                       "with its stone cup; `shrine_bad_*` the same with a sickle scratched "
                       "across the cup (desecrated). `boundary` a worn boundary stone, "
                       "`seat` Aktaion's rock seat, `boulder` a grey rock, `scree`/`scree_b` "
                       "loose stones (walkable), `drum`/`drum_b` the maenads' frame drums, "
                       "`dig` turned earth on grass and `dig_cave` on the cave floor "
                       "(walkable).")
    K.ground(s, "grass", [(c, r) for c in range(8) for r in range(2) if (c, r) != (4, 0)])
    rk = {"K": "ink", "5": "rk5", "4": "rk4", "3": "rk3", "2": "rk2", "1": "rk1", "0": "rk0",
          "i": "iv1", "j": "iv2"}

    # the great herm: a square pillar, a bearded head, garlands of ivy
    top, bot = K.Layer(16, 16), K.Layer(16, 16)
    K.put(top, 4, 3, [
        "..KKKK..",
        ".K5544K.",
        "K554443K",
        "K5K44K3K",
        "K544443K",
        ".K2222K.",
        ".K2222K.",
        "..K22K..",
        ".KK55KK.",
        ".K5443K.",
        ".K5443K.",
        "iK5443Ki",
        ".jiiiij.",
    ], rk)
    for y in range(16):
        for x in range(5, 11):
            bot.px(x, y, ("rk5", "rk4", "rk4", "rk3", "rk3", "rk2")[x - 5])
        bot.px(4, y, "ink")
        bot.px(11, y, "ink")
    K.put(bot, 2, 12, ["KKKKKKKKKKKK", "K5544433322K", "KKKKKKKKKKKK"], rk)
    for (x, y) in ((4, 2), (6, 4), (9, 3), (10, 6), (5, 7), (8, 8)):
        bot.px(x, y, "iv1")
        bot.px(x + 1, y + 1, "iv2")
    _shadow(bot, 3, 14, 15)
    _place(s, "top", 0, 0, top)
    _place(s, "middle", 0, 1, bot)

    # the ivy shrine, clean and desecrated
    for k, cx in ((0, 1), (1, 2)):
        top, bot = K.Layer(16, 16), K.Layer(16, 16)
        K.put(top, 2, 5, [
            "...KKKKKK...",
            "..K554433K..",
            ".K5jjjjjj3K.",
            "K5j4433332jK",
            "K5j4KKKK32jK",
        ], rk)
        for y in range(10, 16):
            for x in range(2, 14):
                top.px(x, y, "rk4" if x < 5 else ("rk3" if x < 11 else "rk2"))
            top.px(1, y, "ink")
            top.px(14, y, "ink")
        K.put(top, 5, 9, ["KKKKKK", "K0000K", "K0000K", "K0000K", "K0000K", "K0000K", "K0440K"],
              {"K": "rk1", "0": "rk0", "4": "rk4"})
        for y in range(0, 14):
            for x in range(2, 14):
                bot.px(x, y, "rk4" if x < 5 else ("rk3" if x < 11 else "rk2"))
            bot.px(1, y, "ink")
            bot.px(14, y, "ink")
        bot.hline(1, 14, 14, "ink")
        K.put(bot, 5, 0, ["K0330K", "K0220K", "KKKKKK"], {"K": "rk1", "0": "rk0", "3": "rk4", "2": "rk3"})
        for (x, y) in ((3, 4), (4, 6), (3, 9), (12, 3), (11, 6), (12, 9), (5, 11), (9, 11)):
            bot.px(x, y, "iv2")
            bot.px(x + 1, y + 1, "iv1")
        _shadow(bot, 2, 15, 15)
        if k:
            # a sickle scratched right across the cup
            for (x, y) in ((4, 14), (5, 13), (6, 13), (7, 13), (8, 14), (9, 15)):
                top.px(x, y, "rk5")
            for (x, y) in ((9, 0), (8, 1), (7, 2), (6, 3), (5, 4)):
                bot.px(x, y, "rk5")
        _place(s, "top", cx, 0, top)
        _place(s, "middle", cx, 1, bot)

    # dig spots: turned earth on grass, and on the cave floor (its own bottom)
    dig = K.Layer(16, 16)
    cave = K.Layer(16, 16)
    for y in range(16):
        for x in range(16):
            cave.px(x, y, G.cave_floor(x, y))
            d = ((x - 7.5) / 6) ** 2 + ((y - 8) / 4.5) ** 2
            if d <= 1:
                h = K.hsh(x, y, 4) % 5
                dig.px(x, y, "rk1" if h == 0 else ("rk2" if h < 3 else "rk3"))
                cave.px(x, y, "rk0" if h == 0 else ("rk1" if h < 3 else "rk3"))
    for (x, y) in ((3, 6), (11, 9), (6, 11)):
        dig.px(x, y, "rk4")
    _place(s, "middle", 3, 0, dig)
    _place(s, "bottom", 4, 0, cave)

    # a boundary stone, worn, with letters cut in it
    b = K.Layer(16, 16)
    K.put(b, 4, 1, [
        ".KKKKKK.",
        "K555543K",
        "K544432K",
        "K4K1K32K",
        "K444432K",
        "K41K132K",
        "K444432K",
        "K4K11K2K",
        "K444432K",
        "K433322K",
        "K432222K",
        "K432221K",
        "KKKKKKKK",
    ], rk)
    _shadow(b, 3, 14, 14)
    _place(s, "middle", 3, 1, b)

    # Aktaion's rock seat: a flat rock worn smooth
    seat = K.Layer(16, 16)
    K.put(seat, 1, 5, [
        "..KKKKKKKKKK..",
        ".K5555544443K.",
        "K555444443332K",
        "K544444333332K",
        "K333333322221K",
        ".K2222222111K.",
        "..KKKKKKKKKK..",
    ], rk)
    _shadow(seat, 2, 14, 12)
    _place(s, "middle", 4, 1, seat)

    # scree: loose stones in the grass, two scatters
    for cy, pts in ((0, ((3, 2), (10, 4), (5, 7), (12, 9), (2, 12), (8, 12))),
                    (1, ((2, 3), (8, 2), (12, 6), (4, 9), (10, 11), (6, 13), (13, 13)))):
        sc = K.Layer(16, 16)
        for (x, y) in pts:
            K.put(sc, x, y, ["54", "32"], rk)
        _place(s, "middle", 5, cy, sc)

    # the maenads' frame drums (polish pass: they read as pale stones before).
    # A tympanon: a skin stretched over a deep wooden hoop, painted with a ring
    # of ochre, bronze jingles set in the hoop, ribbons; one lying on its back,
    # one stood on its rim with a beater against it.
    def tympanon(d, cx, cy, rx, ry, depth, upright=False):
        """A frame drum: a dark wooden hoop round a pale skin with an ochre
        ring and an ivy leaf painted on it, bronze jingles in the hoop. Lying
        flat (an ellipse over the hoop's side) or stood on its rim."""
        h, w = 16, 16
        yy, xx = np.mgrid[0:h, 0:w]
        top = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
        side = np.zeros((h, w), bool)
        for k in range(1, depth + 1):
            side |= ((xx - cx) / rx) ** 2 + ((yy - cy - k) / ry) ** 2 <= 1.0
        side &= ~top
        skin = ((xx - cx) / (rx - 2.0)) ** 2 + ((yy - cy) / (ry - 1.6)) ** 2 <= 1.0
        ring = (((xx - cx) / (rx - 3.4)) ** 2 + ((yy - cy) / (ry - 2.4)) ** 2 <= 1.0) & \
            ~(((xx - cx) / (rx - 4.4)) ** 2 + ((yy - cy) / (ry - 3.1)) ** 2 <= 1.0)
        for y, x in np.argwhere(side):
            d.px(x, y, "wd1" if (x + y) % 5 else "l0")
            if (x - int(cx)) % 3 == 0 and y == int(cy + ry) + depth // 2:
                d.px(x, y, "tg")                      # jingles in the hoop's side
        for y, x in np.argwhere(top & ~skin):
            d.px(x, y, "l1" if (x - cx) + (y - cy) < 0 else "l0")   # the hoop's rim
        for y, x in np.argwhere(skin):
            u = (x - cx) / rx + (y - cy) / ry
            d.px(x, y, "p3" if u < -0.3 else ("p2" if u < 0.5 else "p1"))
        for y, x in np.argwhere(ring & skin):
            d.px(x, y, "tg")
        # an ivy leaf at the skin's heart
        d.px(int(cx), int(cy), "t1")
        d.px(int(cx) - 1, int(cy), "t3")
        d.px(int(cx), int(cy) - 1, "t3")
        d.outline("ink")

    for cy, upright in ((1, False), (0, True)):
        d = K.Layer(16, 16)
        if upright:
            tympanon(d, 7.0, 7.0, 5.6, 6.2, 2)       # stood on its rim, facing you
            for (x, y) in ((12, 13), (13, 12), (14, 11), (15, 10)):
                d.px(x, y, "l1")                     # the beater, leaning on it
            d.px(15, 9, "p2")
        else:
            tympanon(d, 7.5, 6.0, 7.0, 4.2, 3)       # lying on its back
            for (x, y) in ((1, 11), (0, 12), (0, 13), (1, 14)):
                d.px(x, y, "t3")                     # a ribbon trailing from the hoop
        for y in (14, 15):
            for x in range(2, 15):
                if not d.a[y, x, 3] and (x + y) % 2 == 0:
                    d.px(x, y, "gd")
        _place(s, "middle", 6, cy, d)

    # a boulder
    bo = K.Layer(16, 16)
    m = K.ellipse_mask(16, 16, 7.5, 8.0, 6.5, 5.5)
    for y, x in np.argwhere(m):
        u = (x - 7.5) / 6.5 + (y - 8.0) / 5.5
        bo.px(x, y, "rk5" if u < -0.9 else ("rk4" if u < -0.1 else ("rk3" if u < 0.7 else "rk2")))
    bo.outline("ink")
    _shadow(bo, 2, 15, 14)
    _place(s, "middle", 7, 0, bo)
    return s


# --------------------------------------------------------------------------
# Crag detail, ivy on rock, cave mouths and the cave's props
# --------------------------------------------------------------------------

def _crag_cell(L, ox, oy, key, floor=G.grass_floor):
    G.paint_crag_cell(L, ox, oy, key, floor)


def crag_detail():
    """Interior crag cells with something on them (the map builder scatters
    these through big crags), and south-face cells with ivy, the marked ivy
    of the Thyrsus walls, and a cave mouth."""
    full = "1|11111111"
    names = {"crack": (0, 0), "boulders": (1, 0), "tuft": (2, 0), "juniper": (3, 0),
             "ivy_top": (4, 0), "ivy_face": (5, 0), "marked_face": (6, 0), "mouth": (7, 0),
             "cave_carving_L": (0, 1), "cave_carving_R": (1, 1), "cave_shelf": (2, 1),
             "cave_marked": (3, 1), "cave_crack": (4, 1)}
    s = K.struct("crag_detail", "Crag detail: cracks, boulders, ivy, marked ivy, mouths", 8, 2,
                 SEC, walk=["XXXXXXXD", "XXXXX..."], names=names,
                 notes="Interior crag cells (`crack`, `boulders`, `tuft`, `juniper`, "
                       "`ivy_top`) to scatter through a big crag; south-face cells "
                       f"(blob key `{SOUTH_EDGE}`): `ivy_face` ivy over the face, "
                       "`marked_face` the marked ivy of the Thyrsus (gift II), `mouth` a cave "
                       "mouth (MB_NON_ANIMATED_DOOR: put the warp there). The `cave_*` cells "
                       "are the same on Antiope's cave walls: the twins' carving (2 wide), "
                       "a rock shelf, marked ivy, a crack.")
    B = s.B
    for cx in range(5):
        _crag_cell(B, cx * 16, 0, full)
    for cx in (5, 6, 7):
        _crag_cell(B, cx * 16, 0, SOUTH_EDGE)
    for cx in (0, 1, 2, 3, 4):
        _crag_cell(B, cx * 16, 16, SOUTH_EDGE, G.cave_floor)
    # a long crack
    for i, (x, y) in enumerate(((2, 3), (3, 4), (4, 4), (5, 5), (6, 6), (7, 6), (8, 7), (9, 8),
                                 (10, 9), (10, 10), (11, 11), (12, 12))):
        B.px(x, y, "rk1")
        B.px(x, y - 1, "rk4")
        if i % 3 == 0:
            B.px(x + 1, y + 1, "rk2")
    # boulders on the rock
    for (cx, cy, r) in ((5, 6, 4), (11, 10, 3), (4, 12, 2)):
        m = K.ellipse_mask(16, 16, cx, cy, r + 0.5, r)
        for y, x in np.argwhere(m):
            u = (x - cx) / r + (y - cy) / r
            B.px(16 + x, y, "rk5" if u < -0.8 else ("rk4" if u < 0 else ("rk3" if u < 0.8 else "rk2")))
        for y, x in np.argwhere(K.halo(m)):
            if y >= cy:
                B.px(16 + x, y, "rk1")
    # a tuft of grass in a crack
    K.put(B, 32 + 3, 4, [
        "..1.1...",
        ".121.1..",
        "1221212.",
        ".K2222K.",
        "..KKKK..",
    ], {"1": "g3", "2": "g2", "K": "rk1"})
    K.put(B, 32 + 9, 9, [".1.1", "1212", "KKKK"], {"1": "g3", "2": "g1", "K": "rk1"})
    # a mountain juniper clinging to the rock (dark ivy greens)
    m = K.ellipse_mask(16, 16, 8, 7, 6.5, 5)
    for y, x in np.argwhere(m):
        u = (x - 8) / 6.5 + (y - 7) / 5
        B.px(48 + x, y, "iv2" if u < -0.6 else ("iv1" if u < 0.5 else "iv0"))
    for y, x in np.argwhere(K.halo(m)):
        B.px(48 + x, y, "rk1" if y > 7 else "rk0")
    for y in range(12, 15):
        B.px(48 + 8, y, "rk0")
    # ivy creeping over the rock's top
    _ivy(B, 64, 0, 0.45, seed=3)
    # ivy hanging down the face; marked ivy with gold berries
    _ivy(B, 80, 0, 0.55, seed=5, rows=range(1, 16))
    _ivy(B, 96, 0, 0.75, seed=7, rows=range(0, 16), marked=True)
    # the cave mouth in a face: a dark arch, lit lip
    K.put(B, 112 + 2, 2, [
        "...KKKKKKK..",
        "..K0000000K.",
        ".K000000000K",
        "K00000000000K"[:12],
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "K00000000000",
        "KKKKKKKKKKKK",
    ], {"K": "rk1", "0": "rk0"})
    for y in range(3, 15):
        B.px(112 + 13, y, "rk1")
    s.behaviors[(7, 0)] = "MB_NON_ANIMATED_DOOR"
    # the twins carved in the cave wall: a boy with a lyre, a boy with a club
    for ox, which in ((0, "lyre"), (16, "club")):
        fig = [
            "...44...",
            "..4334..",
            "..4334..",
            "...33...",
            ".333333.",
            "3.3333.3",
            "3.3333.3",
            "..3333..",
            "..3..3..",
            "..3..3..",
        ]
        K.put(B, ox + 4, 18, fig, {"4": "rk5", "3": "rk4"})
        if which == "lyre":
            K.put(B, ox + 0, 21, ["3.3", "333", ".3."], {"3": "rk4"})
        else:
            K.put(B, ox + 12, 19, [".33", "33.", "3..", "3.."], {"3": "rk4"})
    for x in range(14, 18):
        B.px(x, 30, "rk1")
    # a rock shelf: a ledge jutting from the wall
    K.put(B, 32 + 1, 23, [
        "KKKKKKKKKKKKKK",
        "K555544443333K",
        "K444433332222K",
        "KKKKKKKKKKKKKK",
        ".K1111111111K.",
    ], {"K": "ink", "5": "rk5", "4": "rk4", "3": "rk3", "2": "rk2", "1": "rk0"})
    _ivy(B, 48, 16, 0.75, seed=9, rows=range(0, 16), marked=True)
    for (x, y) in ((3, 20), (4, 21), (5, 22), (5, 23), (6, 24), (7, 25), (8, 26)):
        B.px(64 + x, 16 + y - 16, "rk0")
    s.behaviors[(5, 1)] = None
    s.behaviors.pop((5, 1), None)
    for c in ((5, 1), (6, 1), (7, 1)):
        for y in range(16):
            for x in range(16):
                B.px(c[0] * 16 + x, 16 + y, G.cave_floor(x, y))
    return s


def _ivy(L, ox, oy, density, seed, rows=range(0, 16), marked=False):
    for y in rows:
        for x in range(16):
            h = K.hsh(x, y, seed) % 100
            hang = (x * 7 + seed) % 5 < 3 and y < 4 + (x * 13 + seed) % 12
            if (h < density * 100 * (0.6 if not hang else 1.0)) and (hang or h < 25):
                u = (x + y) % 4
                c = "iv2" if u == 0 else ("iv1" if u < 3 else "iv0")
                L.px(ox + x, oy + y, c)
    if marked:
        for (x, y) in ((3, 4), (9, 6), (12, 11), (5, 12), (7, 2), (13, 3)):
            L.px(ox + x, oy + y, "mk")
            L.px(ox + x + 1, oy + y, "mk")
            L.px(ox + x, oy + y + 1, "iv0")


def cave_props():
    """Antiope's cave: the bronze brazier, cold and lit, on the cave floor."""
    s = K.struct("brazier", "The bronze brazier, cold and lit", 2, 2, SEC,
                 walk=["XX", "XX"],
                 names={"cold_top": (0, 0), "cold": (0, 1), "lit_top": (1, 0), "lit": (1, 1)},
                 notes="A bronze bowl on a tripod, on the cave floor: `cold_top` over `cold`, "
                       "and lit (`lit_top` over `lit`). Swap both cells to light it: "
                       "METATILE_Kithairon_Brazier_*.")
    for cx in range(2):
        for cy in range(2):
            for y in range(16):
                for x in range(16):
                    s.B.px(cx * 16 + x, cy * 16 + y, G.cave_floor(x, y))
    M = s.M
    for ox in (0, 16):
        K.put(M, ox + 1, 20, [
            ".KKKKKKKKKKKK.",
            "K222222211110K"[:14],
            ".K2211111100K.",
            "..KK111100KK..",
            "....K1100K....",
            "....K1K0K.....",
            "...K1K.K0K....",
            "..K1K...K0K...",
            ".K1K.....K0K..",
            ".KK.......KK..",
        ], {"K": "ink", "2": "au2", "1": "au1", "0": "au0"})
    # embers / flames
    K.put(M, 3, 16 + 2, ["..0.0.0.0...", ".0000000000."], {"0": "au0"})
    K.put(M, 16 + 2, 2, [
        "......1.....",
        ".....121....",
        "..1..121.1..",
        "..121232121.",
        ".12123332121",
        ".1233333321.",
        "..12333321..",
    ], {"1": "rd1", "2": "au2", "3": "cn1"})
    K.put(M, 16 + 2, 16, [
        ".1233333321.",
        ".1123333211.",
        "..11222211..",
        "...111111...",
    ], {"1": "rd1", "2": "au2", "3": "cn1"})
    return s


def trampled():
    """The maenads' dancing floor: grass trampled to bare earth in a soft ring."""
    import kithairon_ground as GG

    def paint(s, ox, oy, key):
        V = K.soft(key, margin=1.5, radius=3.5, amp=1.6, seed=6.1, jag=0.8)
        c = np.s_[16:32, 16:32]
        v = V[c]
        g = K.aethos(K.GRASS)
        for y in range(16):
            for x in range(16):
                if v[y, x]:
                    h = K.hsh(x, y, 21) % 9
                    col = "l1" if h < 6 else ("p1" if h < 8 else "l0")
                    if h == 3 and (x + y) % 3 == 0:
                        col = "g1"
                else:
                    col = GG.A_name(g[y, x])
                s.B.px(ox + x, oy + y, col)
        for y, x in np.argwhere(K.ring(V)[c] & v):
            s.B.px(ox + x, oy + y, "g1" if (x + y) % 2 else "l0")
    return K.shape_set("trampled", "The dancing floor: trampled earth with soft edges", SEC,
                       GG.wanted("trampled"), paint, ".",
                       "Grass beaten to bare earth by dancing feet. Walkable; names are blob "
                       "shape keys.")


def build():
    return [fort(), temple(), trough(), fold(), markers(), crag_detail(), cave_props(), trampled()]
