"""The Kronia grounds (beat 29): the feast that never closes.

Long trestle tables under red-and-cream awnings, benches, the great domed
bread oven, a ring of tents, the steward's big tent, the Kronist stage hung
with gold cloth, the painted banner, children's hoops, the gold-painted sign
and the reader's table. Everything here is warm, generous and lovely: that is
the point (SCRIPT.md beat 29's design notes).

Light from the top left; pieces stand on borrowed aethos grass.
"""
from __future__ import annotations

import numpy as np

import kithairon_lib as K

SEC = "camp"
CAMP = {"K": "ink", "r": "rd1", "R": "rd0", "c": "cn1", "C": "cn2", "n": "cn0", "a": "au2",
        "A": "au1", "o": "au0", "p": "pu1", "w": "wd2", "W": "wd1", "t": "tc1", "g": "g1",
        "d": "gd"}


def _stripes(L, ox, oy, w, h, top, period=6):
    """An awning's canopy seen from above: red and cream stripes running down
    the slope, darker toward the hem."""
    for y in range(h):
        for x in range(w):
            red = ((ox + x) // (period // 2)) % 2 == 0
            dark = y > h - 4
            c = ("rd0" if dark else "rd1") if red else ("cn2" if dark else "cn1")
            L.px(ox + x, oy + y, c)
    for x in range(w):
        L.px(ox + x, oy + top, "ink")


def feast_table():
    """A long table under an awning: canopy over the table, 5 parts wide."""
    names = {"C_L": (0, 0), "C_M": (1, 0), "C_M2": (2, 0), "C_M3": (3, 0), "C_R": (4, 0),
             "T_L": (0, 1), "T_bread": (1, 1), "T_figs": (2, 1), "T_jars": (3, 1), "T_R": (4, 1),
             "B_L": (0, 2), "B_M": (1, 2), "B_R": (2, 2), "B_one": (3, 2)}
    s = K.struct("feast_table", "A long table under a striped awning, and benches", 5, 3, SEC,
                 walk=["XXXXX", "XXXXX", "XXXX."], names=names, on="grass",
                 notes="Row 0, the awning: C_L, C_M (repeat, mixing C_M2 and C_M3 for the "
                       "poles' sag), C_R. Row 1, the table under its hem: T_L, then any mix "
                       "of T_bread, T_figs and T_jars, then T_R. Row 2 holds benches for the "
                       "row below a table: B_L, B_M..., B_R, or B_one alone. Everything "
                       "blocks; people sit on the benches (put the objects there).")
    M, T = s.M, s.T
    # canopy: stripes over the whole row, rolled edges at the ends
    _stripes(M, 0, 2, 80, 14, 0)
    for x in range(80):
        M.px(x, 1, "ink")
        M.px(x, 0, None)
    # sag between poles: lighter band
    for x in range(80):
        if (x % 32) in range(10, 22):
            M.px(x, 5, "cn1" if M.get(x, 5) in ("cn1", "cn2") else "rd1")
    for y in range(1, 16):
        M.px(0, y, "ink")
        M.px(79, y, "ink")
    # table row: the hem (scallops) at the top, the table beneath
    for x in range(80):
        for y in range(0, 4):
            red = (x // 3) % 2 == 0
            if y < 3 or (x % 6) in (1, 2, 3, 4):
                T.px(x, 16 + y, ("rd1" if red else "cn1") if y < 3 else ("rd0" if red else "cn2"))
        T.px(x, 16 + 4, "ink" if (x % 6) in (1, 2, 3, 4) else None)
    # poles at the ends, down to the ground
    for px in (2, 77):
        for y in range(16, 32):
            M.px(px, y, "wd2")
            M.px(px + 1, y, "wd1")
    # the table top and its trestles
    for x in range(4, 76):
        M.px(x, 23, "ink")
        for y in range(24, 28):
            M.px(x, y, "wd2" if y < 26 else "wd1")
        M.px(x, 28, "ink")
    for x in range(4, 76, 1):
        if x in (4, 75):
            for y in range(23, 29):
                M.px(x, y, "ink")
    for tx in (8, 38, 70):
        for y in range(29, 32):
            M.px(tx, y, "wd1")
            M.px(tx + 1, y, "ink")
    # shade under the table
    for x in range(4, 76):
        for y in range(29, 32):
            if not M.a[y, x, 3] and (x + y) % 2 == 0:
                M.px(x, y, "gd")
    # food: bread loaves (T_bread), figs and cheese (T_figs), wine jars and cups (T_jars)
    for bx in (18, 24):
        K.put(M, bx, 20, [".KKKK.", "KaaAAK", "KAAAoK", ".KKKK."], CAMP)
    K.put(M, 22, 21, ["KK", "Ka"], CAMP)
    for (fx, fy) in ((34, 22), (37, 21), (40, 22), (43, 21)):
        K.put(M, fx, fy, [".K.", "KpK", ".K."], CAMP)
    K.put(M, 39, 24, ["KKKK", "KccK"], CAMP)
    for jx in (51, 57):
        K.put(M, jx, 17, [".KK.", "KttK", "KttK", "KttK", ".KK."], CAMP)
    K.put(M, 55, 22, ["KK", "Ko"], CAMP)
    K.put(M, 61, 22, ["KK", "Ko"], CAMP)
    # benches (row 2): planks on stone legs
    for i, kind in enumerate(("L", "M", "R", "one")):
        ox = i * 16
        x0 = 3 if kind in ("L", "one") else 0
        x1 = 13 if kind in ("R", "one") else 16
        for x in range(ox + x0, ox + x1):
            M.px(x, 32 + 5, "ink")
            M.px(x, 32 + 6, "wd2")
            M.px(x, 32 + 7, "wd1")
            M.px(x, 32 + 8, "ink")
        for lx in ([ox + x0 + 1] if kind in ("L", "one") else []) + \
                  ([ox + x1 - 3] if kind in ("R", "one") else []) + ([ox + 7] if kind == "M" else []):
            for y in range(32 + 9, 32 + 12):
                M.px(lx, y, "wd1")
                M.px(lx + 1, y, "ink")
        for x in range(ox + x0, ox + x1):
            if x % 2:
                M.px(x, 32 + 12, "gd")
    # the table row keeps two layers of its own (the table under the hem), so
    # it can't borrow: paint the grass into its bottom with the table over it
    # (the grass under the awning is in its shade: g1 and gd only)
    for x in range(80):
        for y in range(16, 32):
            if M.a[y, x, 3]:
                s.B.a[y, x] = M.a[y, x]
            else:
                s.B.px(x, y, "gd" if (x + y) % 3 == 0 or y < 23 else "g1")
    M.a[16:32] = 0
    for cx in range(5):
        s.ground.pop((cx, 1), None)
    return s


def oven():
    s = K.struct("oven", "The great domed bread oven", 3, 3, SEC, walk=["XXX", "XXX", "XXX"],
                 on="grass", notes="A beehive oven of whitewashed daub on a stone ring, its "
                 "mouth glowing, loaves on a board beside it. The baker stands by it. Its "
                 "ash holds a hidden Charcoal (\"still warm\").")
    M = s.M
    for y in range(48):
        for x in range(48):
            d = ((x - 23.5) / 20.5) ** 2 + ((y - 27) / 21) ** 2
            if d <= 1 and y < 41:
                u = (x - 23.5) / 20.5 + (y - 27) / 21
                c = "cn1" if u < -0.6 else ("cn2" if u < 0.3 else ("cn0" if u < 0.9 else "wd1"))
                if K.hsh(x, y, 2) % 23 == 0 and c != "wd1":
                    c = "cn0"
                M.px(x, y, c)
    M.outline("ink")
    for y in range(39, 46):
        for x in range(4, 44):
            M.px(x, y, "cn0" if (x // 5 + y) % 2 else "wd1")
    M.hline(4, 43, 46, "ink")
    M.vline(3, 39, 46, "ink")
    M.vline(44, 39, 46, "ink")
    K.put(M, 15, 26, [
        "...KKKKKKKKKKKK...",
        "..KooooooooooooK..",
        ".KoAAAAAAAAAAAAoK.",
        "KoAaaAAaaaAAaaAAoK",
        "KoAaaaaarraaaaaAoK",
        "KoArraarrrraarrAoK",
        "KorrrrrrrrrrrrrroK",
        "KKKKKKKKKKKKKKKKKK",
    ], CAMP)
    K.put(M, 21, 4, ["KKKKK", "KnnnK", ".KKK."], CAMP)
    # smoke drifting from the vent
    for (x, y) in ((23, 2), (24, 1), (22, 0)):
        M.px(x, y, "cn1")
    # loaves on a board by the east side
    K.put(M, 37, 40, ["KKKKKKKKKK", "KaAKaAKaAK", "KWWWWWWWWK", "KKKKKKKKKK"], CAMP)
    for x in range(6, 46):
        if x % 2:
            M.px(x, 47, "gd")
    return s


def tent():
    s = K.struct("tent", "A Kronist tent", 2, 2, SEC, walk=["XX", "XX"], on="grass",
                 notes="A round canvas tent with a striped crown and a pennant, its flap "
                       "tied shut. Ring them round the stage.")
    M = s.M
    for y in range(4, 31):
        half = 3 + (y - 4) * 12 // 22 if y < 26 else 15
        for x in range(16 - half, 16 + half):
            if y < 12:
                c = "rd1" if ((x - 16) // 3 + 8) % 2 == 0 else "cn1"
            else:
                c = "cn1" if x < 13 else ("cn2" if x < 24 else "cn0")
                if y > 27:
                    c = "cn0"
            M.px(x, y, c)
    M.outline("ink")
    K.put(M, 13, 18, ["KccK", "KcnK", "KcnK", "KcnK", "KcnK", "KcnK", "KccK", "KKKK"], CAMP)
    for y in range(18, 26):
        M.px(16, y, "ink")
    for y in range(0, 6):
        M.px(16, y, "wd1")
    K.put(M, 17, 0, ["rr.", "rrr", "r.."], CAMP)
    for x in range(4, 29):
        if x % 2:
            M.px(x, 31, "gd")
    return s


def big_tent():
    s = K.struct("big_tent", "The stewards' big tent", 4, 3, SEC, walk=["XXXX", "XXXX", "XXXX"],
                 on="grass", notes="The stewards' tent behind the stage: wide cream canvas "
                 "trimmed in gold, a gold sickle painted over the flap, which is shut. "
                 "\"Nobody goes in.\" The flap (bottom row, middle) is never a door.")
    M = s.M
    for y in range(3, 47):
        if y < 18:
            half = 6 + (y - 3) * 26 // 15
        else:
            half = 31
        for x in range(32 - half, 32 + half):
            if not (0 <= x < 64):
                continue
            if y < 18:
                c = "cn1" if ((x - 32) // 4 + 16) % 2 else "cn2"
                if y > 15:
                    c = "au1"
            else:
                c = "cn1" if x < 20 else ("cn2" if x < 48 else "cn0")
                if y == 18:
                    c = "au2"
                if y > 44:
                    c = "cn0"
            M.px(x, y, c)
    M.outline("ink")
    # the flap, shut, and the sickle over it
    K.put(M, 26, 26, [
        "KKKKKKKKKKKK",
        "KccccKKnnnnK",
        "KcccK..KnnnK",
        "KccK....KnnK",
        "KcK......KnK",
        "KK........KK",
    ], CAMP)
    for y in range(31, 46):
        for x in range(26, 38):
            M.px(x, y, "cn0" if x > 31 else "cn2")
        M.px(25, y, "ink")
        M.px(38, y, "ink")
        M.px(31, y, "ink")
    K.put(M, 26, 20, [
        "...AAAAA..",
        "..A....oA.",
        ".A.......A",
        ".A........",
        "..AA......",
        "....AAAA..",
    ], CAMP)
    for y in range(0, 5):
        M.px(32, y, "wd1")
    K.put(M, 33, 0, ["aaa", "aa."], CAMP)
    for x in range(2, 62):
        if x % 2:
            M.px(x, 47, "gd")
    return s


def stage():
    s = K.struct("stage", "The Kronist stage hung with gold cloth", 5, 3, SEC,
                 walk=["XXXXX", "XXXXX", "XXXXX"], on="grass",
                 notes="A raised wooden stage: a backdrop of gold cloth on posts with a "
                       "golden sun-and-sickle, the planked floor where the Kronist speaks "
                       "(put him on the middle row), steps down the middle of its front.")
    M = s.M
    # posts and the gold cloth backdrop
    for y in range(2, 22):
        for x in range(4, 76):
            fold = (x // 4) % 3
            c = ("au2", "au1", "au0")[fold] if y > 4 else "au0"
            if y in (2, 3):
                c = "rd1"
            M.px(x, y, c)
    for x in range(4, 76):
        M.px(x, 1, "ink")
        if (x // 6) % 2:
            M.px(x, 22, "au1")
            M.px(x, 23, "au0")
    for px in (3, 39, 75):
        for y in range(0, 26):
            M.px(px, y, "wd2")
            M.px(px + 1, y, "wd1")
    # the sun with a sickle across it
    for y in range(6, 20):
        for x in range(30, 50):
            d = ((x - 39.5) / 8) ** 2 + ((y - 12.5) / 6) ** 2
            if d <= 1:
                M.px(x, y, "au2" if d < 0.6 else "cn1")
    K.put(M, 34, 9, ["..KKKK..", ".K....K.", "K.......", "K.......", ".KK.....", "...KKKKK"], CAMP)
    # the planked floor
    for y in range(24, 38):
        for x in range(2, 78):
            M.px(x, y, "wd2" if (y - 24) % 4 else "wd1")
    for x in range(2, 78):
        M.px(x, 38, "ink")
    # the front: plank face with a little skirt of gold cloth, steps in the middle
    for y in range(39, 46):
        for x in range(2, 78):
            M.px(x, y, "wd1" if (x // 8) % 2 else "wd2")
            if y == 39:
                M.px(x, y, "au1" if (x // 3) % 2 else "au2")
    K.put(M, 32, 38, [
        "KKKKKKKKKKKKKKKK",
        "KwwwwwwwwwwwwwwK",
        "KWWWWWWWWWWWWWWK",
        "KwwwwwwwwwwwwwwK",
        "KWWWWWWWWWWWWWWK",
        "KwwwwwwwwwwwwwwK",
        "KKKKKKKKKKKKKKKK",
    ], CAMP)
    M.hline(2, 77, 46, "ink")
    for y in range(24, 47):
        M.px(1, y, "ink")
        M.px(78, y, "ink")
    for x in range(3, 78):
        if x % 2:
            M.px(x, 47, "gd")
    return s


def banner():
    s = K.struct("banner", "The painted banner: NO MORE HOURS", 3, 2, SEC,
                 walk=["XXX", "XXX"], on="grass",
                 notes="A big banner on two poles: a golden field, people dancing, no one "
                       "old, a smashed water clock in the corner and gold letters along the "
                       "foot (beat 29). Its sign is on the bottom middle cell.")
    M = s.M
    for y in range(2, 24):
        for x in range(5, 43):
            c = "au2" if y < 8 else ("au1" if y < 18 else "au0")
            if y >= 19:
                c = "rd0"
            M.px(x, y, c)
    for x in range(5, 43):
        M.px(x, 1, "ink")
        M.px(x, 24, "ink")
    for y in range(1, 25):
        M.px(4, y, "ink")
        M.px(43, y, "ink")
    # dancers: little figures holding hands across the field
    for i, fx in enumerate(range(9, 33, 6)):
        K.put(M, fx, 9 + (i % 2), [".K.", "KrK", ".r.", "K.K"], CAMP)
        if i < 3:
            M.px(fx + 3, 11 + (i % 2), "ink")
            M.px(fx + 4, 11, "ink")
    # the smashed water clock in the corner, its water running out
    K.put(M, 34, 12, ["KcK.", "KcK.", ".KccK", "..Kcc"], CAMP)
    # gold letters along the foot
    for x in range(8, 40, 3):
        M.px(x, 21, "au2")
        M.px(x + 1, 21, "au2")
        M.px(x, 22, "au1")
    for px in (3, 44):
        for y in range(0, 31):
            M.px(px, y, "wd2")
            M.px(px + 1, y, "wd1")
        M.px(px, 0, "au2")
        M.px(px + 1, 0, "au1")
    for x in range(3, 46):
        if x % 2:
            M.px(x, 31, "gd")
    return s


def small():
    names = {"hoop": (0, 0), "board": (1, 0), "reader_L": (2, 0), "reader_R": (3, 0)}
    s = K.struct("camp_small", "Hoops, the gold sign and the reader's table", 4, 1, SEC,
                 walk=["XXXX"], names=names, on="grass",
                 notes="`hoop` a child's hoop and stick lying in the grass (it blocks; put "
                       "them out of the road), `board` the gold-painted sign on its post, "
                       "`reader_L` + `reader_R` the reader's little table with wax tablets "
                       "and his painted sign (TRUE READINGS. FREE.).")
    M = s.M
    m = K.ellipse_mask(16, 16, 7.5, 9, 6, 4.5)
    inner = K.ellipse_mask(16, 16, 7.5, 9, 4.5, 3)
    for y, x in np.argwhere(m & ~inner):
        M.px(x, y, "wd2" if y < 9 else "wd1")
    for i in range(8):
        M.px(10 + i // 2, 3 + i, "wd1")
    # the gold-painted board on its post
    K.put(M, 16 + 1, 1, [
        "KKKKKKKKKKKKKK",
        "KaaaaaaaaaaaaK",
        "KaAAaAaAAaAaaK",
        "KaaaaaaaaaaaaK",
        "KaAaAAaAaAAaaK",
        "KaaaaaaaaaaaaK",
        "KooooooooooooK",
        "KKKKKKKKKKKKKK",
    ], CAMP)
    for y in range(9, 15):
        M.px(16 + 7, y, "wd2")
        M.px(16 + 8, y, "wd1")
    for x in range(16 + 3, 16 + 13):
        if x % 2:
            M.px(x, 15, "gd")
    # the reader's table: wax tablets on a cloth, a painted sign leaning on it
    for x in range(32 + 2, 64 - 2):
        M.px(x, 6, "ink")
        for y in range(7, 11):
            M.px(x, y, "rd1" if y < 9 else "rd0")
        M.px(x, 11, "ink")
    for tx in (36, 42, 48):
        K.put(M, tx, 4, ["KKKK", "KnnK", "KKKK"], CAMP)
    for lx in (35, 58):
        for y in range(12, 15):
            M.px(lx, y, "wd1")
    K.put(M, 52, 0, ["KKKKKKKKK", "KcccccccK", "KcRcRRcRK", "KcccccccK", "KKKKKKKKK"], CAMP)
    for x in range(34, 62):
        if x % 2:
            M.px(x, 15, "gd")
    return s


def build():
    return [feast_table(), oven(), tent(), big_tent(), stage(), banner(), small()]
