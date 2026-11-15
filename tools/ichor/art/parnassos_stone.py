"""Parnassos's worked stone and timber: markers and shrines, the treasury's ruin,
steps, Lebadeia's bridges and Route 9's broken timber bridge.

  markers   the great herm, the boundary stone, Apollo's altar (and the same
            with a sickle scratched across the god's face), a pilgrims' cairn,
            a stone bench, the stone chair of Mnemosyne, column drums at rest
            on grass and in a gully, a Doric capital, a column stump, rubble,
            feathers on the Sphinx's seat, turned earth
  ruin      the Phokian treasury: its broken ashlar walls (west-east runs with
            their south faces, and north-south runs seen from above)
  steps     pale limestone steps, west-east: the pilgrims' steps
  bridge    Lebadeia's little stone bridges over the Herkyna: the road bridge's
            north and south halves, and a one-row footbridge
  timber    Route 9's broken timber bridge over a gully: planks, and the gap
            where the middle plank fell (MB_ICHOR_GAP: the Winged Talaria leap it)
"""
from __future__ import annotations

import numpy as np

import kithairon_ground as KG
import parnassos_lib as P

SEC = "stone"


def _block_shade(L, x0, y0, w, h, top="mb4", face="mb3", dark="mb1", edge="mb0"):
    """A small block seen from above and the south: a lit top, a face, an outline."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, face)
    for x in range(x0, x0 + w):
        L.px(x, y0, top)
        L.px(x, y0 + 1, top)
    for y in range(y0, y0 + h):
        L.px(x0 + w - 1, y, dark)
    for x in range(x0, x0 + w):
        L.px(x, y0 + h - 1, edge)


def _ground_shadow(L, x0, x1, y, rows=2):
    for yy in range(y, y + rows):
        for x in range(x0, x1):
            if not L.a[yy, x, 3] and (x + yy) % 2 == 0:
                L.px(x, yy, "gd")


def markers():
    names = {"herm_top": (0, 0), "stone_top": (1, 0), "altar_top": (2, 0), "dig": (3, 0),
             "rubble": (4, 0), "feathers": (5, 0), "chair": (6, 0), "bench_L": (7, 0),
             "herm": (0, 1), "boundary": (1, 1), "altar": (2, 1), "altar_bad": (3, 1),
             "cairn": (4, 1), "drum": (5, 1), "capital": (6, 1), "bench_R": (7, 1),
             "stump": (0, 2), "drum_gully": (1, 2), "drum_gully_b": (2, 2), "drum_gully_c": (3, 2),
             "scree": (4, 2), "scree_b": (5, 2), "boulder": (6, 2), "drum_b": (7, 2)}
    s = P.struct("markers", "Stones and shrines of the Split Road", 8, 3, SEC,
                 walk=["TTT...XX", "XXXXXXXX", "XXXX..XX"], names=names,
                 notes="On borrowed grass except the gully drums. `herm_top` over `herm`: the "
                       "great herm. `stone_top` over `boundary`: the old boundary stone of the "
                       "crossroads. `altar_top` over `altar` (or `altar_bad`, the god's face "
                       "scratched with a sickle): Apollo's little marble altar. `cairn` the "
                       "pilgrims' cairn; `bench_L`, `bench_R` the lookout's bench; `chair` "
                       "the stone chair of Mnemosyne (walkable: the reading's seat); `drum` a "
                       "column drum at rest; `drum_gully*` drums fallen into a gully (on the "
                       "gully's floor, for the treasury's push puzzle); `capital`, `stump` "
                       "Doric pieces; `rubble`, `feathers`, `dig`, `scree`, `scree_b` walkable; "
                       "`boulder` a grey rock; `drum_b` a drum lying on its side.")
    P.ground(s, "grass", [c for n, c in names.items() if not n.startswith("drum_gully")])
    M, T = s.M, s.T

    # the great herm: a square pillar, a bearded head, an old garland
    hx = 0
    P.put(T, hx + 4, 3, [
        "..oooooo..",
        ".o433332o.",
        ".o4m4m32o.",
        ".o433331o.",
        ".o4b33b1o.",
        "..obbbbo..",
        "...obbo...",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1", "m": "mb0", "b": "mb2"})
    P.put(M, hx + 4, 16, [
        "..o4331o..",
        "..oG4GGo..",
        ".GgG3GgG..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        "..o4331o..",
        ".oo43311o.",
        ".o444331oo",
        ".o3333221o",
        ".oooooooo.",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1", "G": "lr1", "g": "tc1"})
    _ground_shadow(M, hx + 3, hx + 14, 28, 3)

    # the boundary stone: a squat, worn, rounded stele, lettered
    bx = 16
    P.put(T, bx + 4, 9, [
        "...oooo...",
        "..o4433o..",
        ".o444331o.",
        ".o433332o.",
        ".o433321o.",
        ".o433321o.",
        ".o433321o.",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    P.put(M, bx + 4, 16, [
        ".o4m3m21o.",
        ".o433321o.",
        ".o4m3m21o.",
        ".o433321o.",
        ".o433321o.",
        ".o433221o.",
        "oo4332211o",
        "o44333211o",
        "o33332221o",
        "oooooooooo",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1", "m": "mb1"})
    _ground_shadow(M, bx + 2, bx + 15, 26, 3)

    # Apollo's altar: a marble block, a sun-rayed face on its front; a laurel
    # garland draped over the top
    ax = 32
    P.put(T, ax + 2, 10, [
        "..oooooooooo..",
        ".o4444444443o.",
        "o445555554433o",
        "o4G4GG4G4GG43o",
        "oG3G33G3G33Gro",
        "o3333333333321",
    ], {"o": "mb0", "4": "mb4", "5": "mb5", "3": "mb3", "2": "mb2", "1": "mb1", "G": "lr1",
        "r": "tc1"})

    def altar_body(ox, scratched):
        P.put(M, ox + 2, 16, [
            "o3333333333321",
            "o3332y22y23321",
            "o332y3443y2321",
            "o33y344443y321",
            "o333344443321o",
            "o33y344443y321",
            "o332y3443y2321",
            "o3332y22y23321",
            "o3333333333321",
            "o4444444444431",
            "oooooooooooooo",
        ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1", "y": "mb2"})
        if scratched:
            # a sickle's arc gouged right across the face
            for (x, y) in ((4, 19), (5, 18), (6, 18), (7, 18), (8, 19), (9, 20), (10, 21), (11, 22),
                           (11, 23), (10, 24), (5, 20), (4, 21), (3, 22)):
                M.px(ox + x, y, "ink")
            for (x, y) in ((5, 19), (8, 20), (9, 21), (10, 22), (10, 23)):
                M.px(ox + x, y, "mb5")
        _ground_shadow(M, ox + 1, ox + 16, 27, 3)
    altar_body(ax, False)
    altar_body(48, True)

    # turned earth: a fixed or daily dig spot
    dx = 48
    for (x, y) in ((4, 5), (9, 4), (6, 9), (11, 9), (8, 12)):
        P.put(M, dx + x, y, [".11.", "1221", ".11."], {"1": "p1", "2": "mb1"})
    # rubble: loose broken stone, walkable
    rx = 64
    for (x, y, big) in ((3, 4, 1), (10, 2, 0), (7, 9, 1), (12, 11, 0), (2, 12, 0)):
        if big:
            P.put(M, rx + x, y, [".44.", "4332", "3221", ".11."],
                  {"4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
        else:
            P.put(M, rx + x, y, ["43", "21"], {"4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    # feathers on the Sphinx's seat: big pale primaries, scattered
    fx = 80
    for (x, y, d) in ((3, 4, 1), (10, 3, -1), (6, 10, 1), (12, 11, -1)):
        for i in range(5):
            M.px(fx + x + i * d, y + i // 2, "mb5")
            M.px(fx + x + i * d, y + i // 2 + 1, "mb3")
        M.px(fx + x - d, y - 1, "mb1")
    # the stone chair of Mnemosyne: a high-backed seat, cut from one block
    cx_ = 96
    P.put(M, cx_ + 2, 1, [
        "..oooooooooo..",
        ".o4444444443o.",
        ".o4333333332o.",
        ".o4333333332o.",
        ".o4322222232o.",
        "oo4321111232oo",
        "o44321111232331",
        "o43321111232321",
        "o4444444444432o",
        "o4333333333321o",
        "o4333333333321o",
        "o3222222222211o",
        "oooooooooooooo.",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    _ground_shadow(M, cx_ + 1, cx_ + 16, 14, 2)
    # the lookout's bench: a long slab on two blocks
    for half, ox in (("L", 112), ("R", 112)):
        pass
    for y in range(16):
        for x in range(32):
            pass
    bench = P.Layer(32, 32)
    P.put(bench, 2, 18, [
        "oooooooooooooooooooooooooooo",
        "o44444444444444444444444443o",
        "o44555445544455544554445443o",
        "o33333333333333333333333332o",
        "o22222222222222222222222221o",
        "oooooooooooooooooooooooooooo",
        ".o4331o............o4331o...",
        ".o3321o............o3321o...",
        ".oooooo............oooooo...",
    ], {"o": "mb0", "5": "mb5", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    for y in range(27, 30):
        for x in range(1, 31):
            if not bench.a[y, x, 3] and (x + y) % 2 == 0:
                bench.px(x, y, "gd")
    M.a[0:16, 112:128] = bench.a[16:32, 0:16]
    M.a[16:32, 112:128] = bench.a[16:32, 16:32]

    # the pilgrims' cairn: a heap of small stones, the top one scratched
    kx = 64
    for (x, y, w) in ((3, 12, 10), (4, 9, 8), (5, 6, 6), (6, 3, 4)):
        for i in range(w // 2):
            c = ("mb4", "mb3", "mb2", "mb3", "mb4")[(i + y) % 5]
            P.put(M, kx + x + i * 2, 16 + y, ["43", "21"],
                  {"4": c, "3": "mb3" if c != "mb3" else "mb2", "2": "mb2", "1": "mb1"})
    P.put(M, kx + 6, 16 + 1, [".44.", "4mm3", ".22."], {"4": "mb5", "m": "mb1", "3": "mb3",
                                                       "2": "mb2"})
    _ground_shadow(M, kx + 2, kx + 15, 16 + 14, 2)

    # a column drum at rest on the grass: fluted, seen end-on at a slant
    def drum(L, ox, oy, ramp, floor_shadow=True):
        top, mid, low, dark, out = ramp
        m = P.ellipse_mask(16, 16, 8, 7, 6.5, 6)
        for y, x in np.argwhere(m):
            L.px(ox + x, oy + y, mid)
        for y, x in np.argwhere(P.ellipse_mask(16, 16, 8, 6, 5, 4.5)):
            L.px(ox + x, oy + y, top)
        for y, x in np.argwhere(P.ellipse_mask(16, 16, 8, 6, 2, 1.5)):
            L.px(ox + x, oy + y, low)
        for y, x in np.argwhere(P.ring(m)):
            L.px(ox + x, oy + y, out)
        for x in range(3, 14):
            if x % 2 == 0:
                L.px(ox + x, oy + 12, dark)
        if floor_shadow:
            for x in range(3, 14):
                if (x % 2) == 0:
                    L.px(ox + x, oy + 14, "gd")
    drum(M, 80, 16, ("mb4", "mb3", "mb2", "mb1", "mb0"))
    # a Doric capital lying on its side, and a column stump
    P.put(M, 96 + 1, 16 + 3, [
        "oooooooooooooo",
        "o444444444443o",
        "o333333333332o",
        ".o3333333332o.",
        "..o33333332o..",
        "...o322221o...",
        "...o432221o...",
        "...o432221o...",
        "...oooooooo...",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    _ground_shadow(M, 96 + 2, 96 + 15, 16 + 12, 2)
    m = P.ellipse_mask(16, 16, 8, 6, 5.5, 4)
    for y, x in np.argwhere(m):
        M.px(x, 32 + y, "mb4" if (x + y) % 3 else "mb3")
    for y in range(6, 13):
        for x in range(3, 14):
            if x in (3, 13):
                M.px(x, 32 + y, "mb0")
            elif y >= 6 and not m[y, x]:
                M.px(x, 32 + y, "mb2" if x % 2 else "mb3")
    for y, x in np.argwhere(P.ring(m)):
        if y < 6:
            M.px(x, 32 + y, "mb1")
    for x in range(3, 14):
        M.px(x, 32 + 13, "mb0")
    _ground_shadow(M, 2, 15, 32 + 14, 2)

    # scree, a boulder, a drum on its side
    for (ox, pts) in ((64, ((3, 4), (10, 3), (6, 10), (12, 12), (2, 13))),
                      (80, ((5, 3), (11, 7), (3, 9), (9, 12)))):
        for (x, y) in pts:
            P.put(M, ox + x, 32 + y, ["43", "21"], {"4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    m = P.ellipse_mask(16, 16, 8, 8, 6.5, 5.5)
    for y, x in np.argwhere(m):
        u = (x - 8) / 6.5 + (y - 8) / 5.5
        M.px(96 + x, 32 + y, "mb4" if u < -0.7 else ("mb3" if u < 0.2 else ("mb2" if u < 0.9 else "mb1")))
    for y, x in np.argwhere(P.ring(m)):
        if y >= 7:
            M.px(96 + x, 32 + y, "mb0")
    _ground_shadow(M, 96 + 2, 96 + 15, 32 + 14, 2)
    P.put(M, 112 + 1, 32 + 4, [
        "..oooooooooooo",
        ".o4444444444o3",
        "o43434343434342",
        "o33333333333321",
        "o32323232323221",
        ".o222222222221o",
        "..oooooooooooo.",
    ], {"o": "mb0", "4": "mb4", "3": "mb3", "2": "mb2", "1": "mb1"})
    _ground_shadow(M, 112 + 2, 112 + 15, 32 + 11, 3)

    # drums fallen into a gully: on the gully's dark floor, in Parnassos's rock
    B = s.B
    for i, (ox, shift) in enumerate(((16, 0), (32, 3), (48, -2))):
        for y in range(16):
            for x in range(16):
                B.px(ox + x, 32 + y, "pk1" if P.hsh(x, y, 31) % 11 == 0 else "pk0")
        tmp = P.Layer(16, 16)
        drum(tmp, 0, 0, ("pk4", "pk3", "pk2", "pk1", "pk0"), floor_shadow=False)
        for y in range(16):
            for x in range(16):
                if tmp.a[y, x, 3]:
                    xx = x + shift
                    if 0 <= xx < 16:
                        B.a[32 + y, ox + xx] = tmp.a[y, x]
    return s


# --------------------------------------------------------------------------
# The treasury's ruin: broken ashlar walls
# --------------------------------------------------------------------------

def _ashlar_face(L, ox, oy, h, broken=None):
    """A wall's south face: courses of squared blocks, lit at their tops. The top
    of the wall (its coping) is the first 4 rows; `broken` gives a jagged top as a
    list of 16 heights to drop."""
    drop = broken or [0] * 16
    for x in range(16):
        d = drop[x]
        for y in range(d, 16):
            yy = y - d
            if y < d + 3:
                c = "mb4" if yy == 0 else ("mb5" if yy == 1 and x % 3 else "mb3")
            elif y == d + 3:
                c = "mb1"
            else:
                course = (y - 4) // 4
                joint_y = (y - 4) % 4 == 3
                off = 4 if course % 2 else 0
                joint_x = (x + off) % 8 == 7
                if joint_y or joint_x:
                    c = "mb1"
                elif (y - 4) % 4 == 0:
                    c = "mb4"
                else:
                    c = "mb3" if (x + y) % 5 else "mb2"
            if y >= 15:
                c = "mb0"
            L.px(ox + x, oy + y, c)


def ruin():
    names = {"W_L": (0, 0), "W_M": (1, 0), "W_low": (2, 0), "W_R": (3, 0),
             "NS": (4, 0), "NS_end": (5, 0), "W_stub": (6, 0), "door_L": (7, 0)}
    s = P.struct("ruin", "The treasury's broken walls", 8, 1, SEC, walk=["XXXXXXXX"], names=names,
                 notes="The Phokian treasury's ashlar, on borrowed grass. `W_L`, `W_M`, `W_R`: a "
                       "west-east wall with its coping and south face; `W_low` the same broken "
                       "low; `W_stub` a fallen end; `NS` a north-south wall seen from above, "
                       "`NS_end` its south end with a bit of face; `door_L` a door jamb.")
    P.ground(s, "grass")
    M = s.M
    jag_m = [0] * 16
    jag_low = [6, 6, 7, 7, 8, 8, 8, 7, 6, 6, 7, 9, 9, 8, 7, 7]
    jag_stub = [2, 3, 4, 6, 8, 9, 10, 11, 11, 12, 12, 13, 13, 13, 14, 14]
    _ashlar_face(M, 0, 0, 16)
    _ashlar_face(M, 16, 0, 16, jag_m)
    _ashlar_face(M, 32, 0, 16, jag_low)
    _ashlar_face(M, 48, 0, 16)
    _ashlar_face(M, 96, 0, 16, jag_stub)
    # wall ends: an outline on the open side
    for y in range(16):
        M.px(0, y, "mb1")
        M.px(63, y, "mb0")
    # north-south: the wall's top seen from above, 8 px wide, blocks in a column
    for (ox, end) in ((64, False), (80, True)):
        for y in range(16):
            for x in range(4, 12):
                if x in (4,):
                    c = "mb4"
                elif x == 11:
                    c = "mb1"
                elif y % 5 == 4:
                    c = "mb1"
                else:
                    c = "mb3" if (x + y) % 4 else "mb4"
                M.px(ox + x, y, c)
            if not M.a[y, ox + 12, 3] and y % 2 == 0:
                M.px(ox + 12, y, "gd")
        if end:
            for y in range(10, 16):
                for x in range(4, 12):
                    M.px(ox + x, y, "mb2" if (x + y) % 3 else "mb3")
                M.px(ox + 11, y, "mb0")
            for x in range(4, 12):
                M.px(ox + x, 15, "mb0")
                M.px(ox + x, 10, "mb4")
    # a door jamb: the face, then the doorway's dark edge
    _ashlar_face(M, 112, 0, 16)
    for y in range(4, 16):
        for x in range(12, 16):
            M.px(112 + x, y, "mb0" if x == 12 else None)
    for y in range(4, 16):
        for x in range(12, 16):
            M.a[y, 112 + x] = 0
    _ground_shadow(M, 0, 128, 0, 0)
    return s


# --------------------------------------------------------------------------
# Steps
# --------------------------------------------------------------------------

def steps():
    s = P.struct("steps", "The pilgrims' steps", 3, 1, SEC, walk=["..."],
                 names={"L": (0, 0), "M": (1, 0), "R": (2, 0)},
                 notes="Three pale limestone risers going down to the south: the steps of "
                       "Lebadeia's precinct, where the pilgrims sit. West-east; walkable.")
    B = s.B
    for cx, side in enumerate("LMR"):
        ox = cx * 16
        for y in range(16):
            band = y // 5
            yy = y % 5
            for x in range(16):
                if yy == 0:
                    c = "mb4"
                elif yy == 4:
                    c = "mb1"
                elif yy == 3:
                    c = "mb2"
                else:
                    c = "mb3" if (x * 3 + band) % 11 else "mb2"
                B.px(ox + x, y, c)
            if y == 15:
                for x in range(16):
                    B.px(ox + x, y, "mb0")
        if side == "L":
            for y in range(16):
                B.px(ox, y, "mb0")
                B.px(ox + 1, y, "mb2")
        if side == "R":
            for y in range(16):
                B.px(ox + 15, y, "mb0")
                B.px(ox + 14, y, "mb1")
    return s


# --------------------------------------------------------------------------
# Lebadeia's stone bridges over the Herkyna
# --------------------------------------------------------------------------

def bridge():
    names = {"N_L": (0, 0), "N_R": (1, 0), "S_L": (0, 1), "S_R": (1, 1), "F_L": (2, 0), "F_R": (3, 0),
             "F_L2": (2, 1), "F_R2": (3, 1)}
    s = P.struct("bridge", "Stone bridges over the Herkyna", 4, 2, SEC, walk=["....", "...."],
                 names=names,
                 notes="Over a river two cells wide. The road bridge is two rows: `N_L` `N_R` "
                       "(its north parapet) over `S_L` `S_R` (its south parapet). The "
                       "footbridge is one row, `F_L` `F_R`, parapets both sides. Walkable; count "
                       "these cells as river when tiling the banks, so the water runs under.")
    B = s.B

    def deck(ox, oy):
        for y in range(16):
            for x in range(16):
                c = "mb3" if (x // 4 + y // 4) % 2 == 0 else "mb2"
                if x % 4 == 3 or y % 4 == 3:
                    c = "mb2"
                if P.hsh(x + ox, y + oy, 3) % 13 == 0:
                    c = "mb4"
                B.px(ox + x, oy + y, c)

    def parapet(ox, oy, y0, south):
        for x in range(16):
            B.px(ox + x, oy + y0, "mb4" if not south else "mb3")
            B.px(ox + x, oy + y0 + 1, "mb4")
            B.px(ox + x, oy + y0 + 2, "mb3")
            B.px(ox + x, oy + y0 + 3, "mb1" if not south else "mb0")
            if south:
                B.px(ox + x, oy + y0 + 4, "mb1")

    def post(ox, oy, x0, y0, h):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + 3):
                B.px(ox + x, oy + y, "mb4" if x == x0 else ("mb3" if x == x0 + 1 else "mb1"))
        for x in range(x0, x0 + 3):
            B.px(ox + x, oy + y0 + h - 1, "mb0")
    # road bridge
    for cx in (0, 1):
        deck(cx * 16, 0)
        parapet(cx * 16, 0, 0, False)
        deck(cx * 16, 16)
        parapet(cx * 16, 16, 11, True)
    post(0, 0, 0, 0, 6)
    post(16, 0, 13, 0, 6)
    post(0, 16, 0, 10, 6)
    post(16, 16, 13, 10, 6)
    # footbridge: narrower deck, parapets both sides; and a second copy over the
    # river's lower reach (identical: the build merges it)
    for (oy) in (0, 16):
        for cx in (2, 3):
            deck(cx * 16, oy)
            parapet(cx * 16, oy, 0, False)
            parapet(cx * 16, oy, 11, True)
        post(32, oy, 0, 0, 5)
        post(32, oy, 0, 11, 5)
        post(48, oy, 13, 0, 5)
        post(48, oy, 13, 11, 5)
    return s


# --------------------------------------------------------------------------
# The broken timber bridge over a gully
# --------------------------------------------------------------------------

def timber():
    names = {"W": (0, 0), "gap": (1, 0), "E": (2, 0)}
    s = P.struct("timber", "The broken timber bridge", 3, 1, SEC, walk=["..X"], names=names,
                 notes="A plank bridge over a gully three cells wide: `W`, `gap` (the middle "
                       "planks fell: MB_ICHOR_GAP, so the Winged Talaria leap it at a run), "
                       "`E`. Walkable but the gap. Count these cells as gully when tiling it.")
    s.walk = [".X."]
    s.behaviors[(1, 0)] = "MB_ICHOR_GAP"
    B = s.B
    # the gully's floor under the planks: the gap's in the gully's own colors,
    # the plank cells' edges in the field group's dark
    for x in range(48):
        for y in range(16):
            if 16 <= x < 32:
                B.px(x, y, "pk1" if P.hsh(x, y, 31) % 11 == 0 else "pk0")
            else:
                B.px(x, y, "ink")

    def planks(ox, x0, x1):
        for x in range(x0, x1):
            for y in range(3, 13):
                c = "l1" if (x % 4) else "l0"
                if y in (3, 12):
                    c = "wd1"
                if x % 4 == 0:
                    c = "ink" if y in (3, 12) else "l0"
                B.px(ox + x, y, c)
        # rope rails
        for x in range(x0, x1):
            B.px(ox + x, 2, "l0")
            B.px(ox + x, 13, "l0")
    tmp_rows = (0, 16, 32)
    planks(0, 0, 16)
    planks(32, 0, 16)
    # the gap: two splintered stubs and a sagging rope; the floor far below
    for (x, h) in ((0, 4), (1, 3), (2, 5), (14, 3), (15, 5)):
        for y in range(5, 5 + h):
            B.px(16 + x, y, "bz1" if x % 2 else "pk2")
    for x in range(16):
        sag = 2 + (2 if 4 < x < 12 else (1 if 2 < x < 14 else 0))
        B.px(16 + x, sag, "pk2")
        B.px(16 + x, 13 + sag // 2, "pk2")
    del tmp_rows
    return s


def pmarkers(mk):
    """The herm, the boundary stone and the stone chair again, standing on paving
    (the crossroads' triangle, the precinct) instead of grass."""
    import parnassos_ground as G
    names = ["herm_top", "herm", "stone_top", "boundary", "chair"]
    s = P.crop(mk, "pmarkers", "The herm, the boundary stone and the chair, on paving", names,
               cols=5, notes="`markers`' `herm_top` over `herm`, `stone_top` over `boundary`, and "
                             "`chair`, on the paving's flags instead of grass.")
    s.ground = {}
    s.walk = ["TXTX."]
    for i in range(5):
        for y in range(16):
            for x in range(16):
                s.B.px(i * 16 + x, y, G.pave_px(x, y))
    # a shadow on grass is a darker joint on paving
    for L in (s.M, s.T):
        P.recolor(L, {"gd": "mb1"})
    return s


def build():
    mk = markers()
    return [mk, pmarkers(mk), ruin(), steps(), bridge(), timber()]
