"""The climb's set pieces: the fallen temple of Artemis and its drums, the
charcoal kiln, the broken plank bridge and its ravine, the shepherd's cave,
the side waterfall and the Styx's thread, the terraces' north rims and
ledges, Nonakris's houses, the shrine of Artemis, herms, the Oath Stone,
Kyllene's tortoise boulders and the hawk's nest, springs and runnels.

Light from the top left. Pieces on grass or road borrow aethos's ground.
"""
from __future__ import annotations

import numpy as np

import heights_ground as G
import heights_lib as H

SEC = "props"
STONE = {"K": "ink", "5": "qm2", "4": "qm2", "3": "qm3", "2": "qm4", "1": "qm5", "0": "qr1"}
ROCK = {"K": "ink", "5": "qr5", "4": "qr4", "3": "qr3", "2": "qr2", "1": "qr1", "0": "qr0",
        "v": "qv1", "w": "qv2", "d": "wd1", "k": "k1", "g": "gd", "G": "g1"}


def _recolor(L, m):
    for y in range(L.h):
        for x in range(L.w):
            c = L.get(x, y)
            if c in m:
                L.px(x, y, m[c])


def L16(h=16, w=16):
    return H.Layer(w, h)


def place(s, layer, cx, cy, src):
    h, w = src.a.shape[:2]
    s.layers[layer].a[cy * 16:cy * 16 + h, cx * 16:cx * 16 + w] = src.a


def shadow(L, x0, x1, y0, y1=None, color="gd"):
    for y in range(y0, (y1 or y0) + 1):
        for x in range(x0, x1):
            if 0 <= x < L.w and 0 <= y < L.h and not L.a[y, x, 3] and (x + y) % 2 == 0:
                L.px(x, y, color)


def grass_fill(L, x0=0, y0=0, w=16, h=16):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, H.grass_px(x, y))


def rock_fill(L, ramp=G.GREY):
    for y in range(L.h):
        for x in range(L.w):
            L.px(x, y, G.rock_top(x, y, ramp))


def face_fill(L, ramp=G.GREY, ferns=True, variant=0):
    for y in range(L.h):
        for x in range(L.w):
            L.px(x, y, G.face_px(x, y, ramp, ferns, variant))


def blob(L, cx, cy, rx, ry, ramp, outline="ink"):
    """A rounded stone, lit from the top left."""
    m = H.ellipse_mask(L.w, L.h, cx, cy, rx, ry)
    for y, x in np.argwhere(m):
        u = (x - cx) / rx + (y - cy) / ry
        L.px(x, y, ramp[3] if u < -0.9 else (ramp[2] if u < -0.1 else (ramp[1] if u < 0.7 else ramp[0])))
    edge = m & ~(np.pad(m, 1)[:-2, 1:-1] & np.pad(m, 1)[2:, 1:-1] & np.pad(m, 1)[1:-1, :-2]
                 & np.pad(m, 1)[1:-1, 2:])
    for y, x in np.argwhere(edge):
        L.px(x, y, outline)
    return m


# --------------------------------------------------------------------------
# The fallen temple of Artemis: drums, rubble, the broken shelf
# --------------------------------------------------------------------------

def _drum_side(L, x0, y0):
    """A column drum lying on its side, seen from above: a fluted cylinder
    running east-west, its round end to the west."""
    for y in range(y0, y0 + 10):
        for x in range(x0 + 2, x0 + 14):
            t = (y - y0) / 9
            c = "qm2" if t < 0.3 else ("qm3" if t < 0.65 else "qm4")
            if (y - y0) in (2, 5, 8) and x % 2:
                c = "qm4" if t < 0.6 else "qm5"          # the flutes
            L.px(x, y, c)
    for y in range(y0, y0 + 10):
        L.px(x0 + 1, y, "qm3" if 1 < y - y0 < 8 else "ink")
        L.px(x0 + 14, y, "ink")
    L.hline(x0 + 2, x0 + 13, y0, "ink")
    L.hline(x0 + 2, x0 + 13, y0 + 9, "ink")
    # the round end: a disc with a dowel hole
    for y in range(y0 + 1, y0 + 9):
        L.px(x0 + 2, y, "qm2")
        L.px(x0 + 3, y, "qm3")
    L.px(x0 + 2, y0 + 4, "qm5")
    L.px(x0 + 2, y0 + 5, "qm5")


def _drum_face(L, cx, cy, r=6.5, wedged=False):
    """A drum seen end-on from above: a fluted disc."""
    m = H.ellipse_mask(L.w, L.h, cx, cy, r, r * 0.9)
    for y, x in np.argwhere(m):
        u = (x - cx) / r + (y - cy) / r
        ang = np.arctan2(y - cy, x - cx)
        flute = (int((ang + np.pi) / (2 * np.pi) * 16) % 2 == 0) and ((x - cx) ** 2 + (y - cy) ** 2) > (r - 2) ** 2
        c = "qm2" if u < -0.5 else ("qm3" if u < 0.6 else "qm4")
        if flute:
            c = "qm4" if u < 0.3 else "qm5"
        L.px(x, y, c)
    edge = m & ~(np.pad(m, 1)[:-2, 1:-1] & np.pad(m, 1)[2:, 1:-1] & np.pad(m, 1)[1:-1, :-2]
                 & np.pad(m, 1)[1:-1, 2:])
    for y, x in np.argwhere(edge):
        L.px(x, y, "qm5" if wedged else "ink")
    L.px(int(cx), int(cy), "qm5")
    L.px(int(cx) + 1, int(cy), "qm5")


def ruins():
    names = {"drum_rest": (0, 0), "drum_wedged": (1, 0), "lip": (2, 0), "gap": (3, 0),
             "rubble": (4, 0), "rubble_b": (5, 0), "stump": (6, 0), "capital": (7, 0),
             "jars": (0, 1), "hoofcups": (1, 1), "column_top": (2, 1), "column": (3, 1),
             "slabs": (4, 1), "drum_lie": (5, 1), "steps_W": (6, 1), "steps_E": (7, 1)}
    s = H.struct("ruins", "The fallen temple of Artemis on the gorge shelf", 8, 2, SEC,
                 walk=["X...XXXX", "XXTX.X.."], names=names,
                 notes="The shelf's fallen Doric temple. `drum_rest` a drum at rest against the "
                       "cliff, `drum_wedged` a drum flush in the road's gap (walkable), `lip` the "
                       "shelf's crumbling edge (walkable: put drum 1's button there), `gap` the "
                       "broken edge (walkable only at elevation 1: drum 2's button), `rubble`, "
                       "`rubble_b` tumbled blocks, `stump` a column's stump, `capital` a fallen "
                       "capital, `drum_lie` a drum fallen in the grass. `column_top` over `column`: "
                       "the one column still standing. `slabs` the stylobate's paving, `steps_W`/"
                       "`_E` its worn steps. `jars` the muleteer's empty jars, `hoofcups` the "
                       "hoof-cups at Styx Falls.")
    H.ground(s, "path", [(0, 0), (1, 0), (2, 0), (4, 1), (6, 1), (7, 1)])
    H.ground(s, "grass", [(4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (5, 1)])
    # drum at rest against the cliff (the cliff lies west of it)
    d = L16()
    _drum_side(d, 0, 3)
    shadow(d, 2, 15, 13, 14)
    place(s, "middle", 0, 0, d)
    # drum wedged flush in the gap: its end set into the road
    d = L16()
    for y in range(16):
        for x in range(16):
            if (x - 7.5) ** 2 + (y - 8) ** 2 < 64:
                d.px(x, y, "qr1")
    _drum_face(d, 7.5, 8.0, 6.6, wedged=True)
    place(s, "middle", 1, 0, d)
    # the lip: the road's crumbling east edge, the gorge beyond
    d = L16()
    for y in range(16):
        e = 11 + (1 if (y // 3) % 2 else 0) - (1 if y in (6, 7, 13) else 0)
        for x in range(e, 16):
            d.px(x, y, "ink" if x > e + 1 else "qr1")
        d.px(e - 1, y, "qm4")
    for (x, y) in ((5, 3), (6, 4), (7, 4), (4, 10), (5, 11)):
        d.px(x, y, "qm5")
    place(s, "middle", 2, 0, d)
    # the gap: the shelf broken away, the river's roar below
    d = L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, "ink" if (x + y * 3) % 7 else "qr1")
    for x in range(16):
        d.px(x, 0, "qm4")
        d.px(x, 1, "qm5" if x % 3 else "qr1")
        d.px(x, 15, "qm5")
    for y in range(2, 15):
        d.px(0, y, "qm4")
        d.px(15, y, "qr1")
    for (x, y) in ((4, 6), (9, 9), (11, 4)):
        d.px(x, y, "qm5")
    place(s, "bottom", 3, 0, d)
    # tumbled blocks
    for cx, seed in ((4, 0), (5, 1)):
        d = L16()
        blocks = [((2, 4, 7, 6), 0), ((8, 2, 6, 5), 1), ((6, 9, 8, 6), 2)] if seed == 0 else \
            [((1, 7, 8, 7), 0), ((7, 3, 7, 6), 1), ((10, 9, 5, 5), 2)]
        for (x0, y0, w, h), k in blocks:
            for y in range(y0, min(16, y0 + h)):
                for x in range(x0, min(16, x0 + w)):
                    top = y < y0 + h // 2
                    c = ("qm2" if x < x0 + w // 2 else "qm3") if top else ("qm4" if x < x0 + w - 1 else "qm5")
                    d.px(x, y, c)
            d.hline(x0, min(15, x0 + w - 1), y0, "ink")
            d.vline(min(15, x0 + w - 1), y0, min(15, y0 + h - 1), "ink")
            d.vline(x0, y0, min(15, y0 + h - 1), "ink")
            d.hline(x0, min(15, x0 + w - 1), min(15, y0 + h - 1), "ink")
        shadow(d, 1, 16, 15)
        place(s, "middle", cx, 0, d)
    # a column stump, fluted
    d = L16()
    _drum_face(d, 7.5, 7.0, 6.0)
    for y in range(11, 15):
        for x in range(2, 14):
            d.px(x, y, "qm4" if x < 8 else "qm5")
    d.hline(2, 13, 15, "ink")
    shadow(d, 1, 15, 15)
    place(s, "middle", 6, 0, d)
    # a fallen capital: an echinus and abacus on its side
    d = L16()
    H.put(d, 1, 3, [
        "KKKKKKKKKKKKK.",
        "K55555544443K.",
        "K54444443332K.",
        ".K444443332K..",
        "..K3333322K...",
        "..K3333321K...",
        "..K3322221K...",
        "...KKKKKKK....",
    ], STONE)
    shadow(d, 2, 15, 11, 12)
    place(s, "middle", 7, 0, d)
    # the muleteer's empty jars
    d = L16()
    for jx in (1, 6, 11):
        H.put(d, jx, 4, [".KK.", "K21K", "K21K", "KccK", "KccK", "KcCK", ".KK."],
              {"K": "ink", "2": "qm3", "1": "qm4", "c": "qc2", "C": "qc1"})
    shadow(d, 1, 16, 11)
    place(s, "middle", 0, 1, d)
    # hoof-cups on a flat stone, each tied with a linen scrap
    d = L16()
    H.put(d, 1, 8, ["KKKKKKKKKKKKKK", "K3333333333332", "K2222222222221", "KKKKKKKKKKKKKK"], STONE)
    for hx in (2, 6, 10):
        H.put(d, hx, 4, [".dd.", "dDDd", "dDDd", ".55."], {"d": "wd1", "D": "qm5", "5": "qm2"})
    shadow(d, 1, 16, 12, 13)
    place(s, "middle", 1, 1, d)
    # the one column still standing: shaft and capital
    top, bot = L16(), L16()
    H.put(top, 2, 6, ["KKKKKKKKKKKK", "K5555544443K", "KKKKKKKKKKKK", ".K55443322K.",
                      "..K544332K..", "..K544332K.."], STONE)
    for y in range(16):
        H.put(bot, 4, y, ["K5" + ("4" if y % 2 else "3") + "43" + ("2" if y % 2 else "1") + "2K"], STONE)
    H.put(bot, 2, 13, ["KKKKKKKKKKKK", "K5544433221K", "KKKKKKKKKKKK"], STONE)
    place(s, "top", 2, 1, top)
    place(s, "middle", 3, 1, bot)
    # the stylobate's paving: big worn marble slabs (on the road)
    d = L16()
    for y in range(16):
        for x in range(16):
            c = "qm3" if (x // 8 + y // 8) % 2 == 0 else "qm2"
            if x % 8 == 7 or y % 8 == 7:
                c = "qm4"
            if (x * 5 + y * 3) % 23 == 0:
                c = "qm4"
            d.px(x, y, c)
    place(s, "middle", 4, 1, d)
    # a drum fallen in the grass, half sunk
    d = L16()
    _drum_side(d, 0, 4)
    for (x, y) in ((3, 12), (8, 13), (12, 12)):
        d.px(x, y, "g1")
    shadow(d, 2, 15, 14, 15)
    place(s, "middle", 5, 1, d)
    # worn steps up onto the stylobate (west and east halves)
    for cx in (6, 7):
        d = L16()
        for y in range(16):
            for x in range(16):
                band = y // 5
                c = ("qm2", "qm3", "qm4", "qm3")[band]
                if y % 5 == 4:
                    c = "qm5"
                d.px(x, y, c)
        if cx == 6:
            d.vline(0, 0, 15, "qm5")
        else:
            d.vline(15, 0, 15, "qm5")
        place(s, "middle", cx, 1, d)
    return s


# --------------------------------------------------------------------------
# The charcoal kiln
# --------------------------------------------------------------------------

def kiln():
    s = H.struct("kiln", "A charcoal kiln, smoking", 2, 3, SEC, walk=["TT", "XX", "XX"], on="grass",
                 names={"smoke_L": (0, 0), "smoke_R": (1, 0)},
                 notes="A charcoaler's earth-covered kiln mound, smoke leaking from its vents. "
                       "The top row is the smoke, drawn over the player.")
    L = H.Layer(32, 48)
    m = H.ellipse_mask(32, 48, 15.5, 33.0, 14.0, 11.0)
    m[44:] = False
    for y, x in np.argwhere(m):
        u = (x - 15.5) / 14 + (y - 33) / 11
        h = H.hsh(x, y, 5) % 9
        c = "qc2" if u < -0.6 else ("qc1" if u < 0.4 else "qm5")
        if h == 0:
            c = "qm4"
        L.px(x, y, c)
    L.outline("ink")
    for y in range(40, 44):
        for x in range(4, 28):
            if m[y, x]:
                L.px(x, y, "qm5" if (x + y) % 2 else "qr1")
    # vents with a glow, and the stacked wood at the door
    for (vx, vy) in ((10, 27), (20, 26), (15, 31)):
        L.px(vx, vy, "ink"); L.px(vx + 1, vy, "ink")
        L.px(vx, vy + 1, "qc1"); L.px(vx + 1, vy + 1, "qc2")
    H.put(L, 11, 37, ["KKKKKKKKK", "KddDddDdK", "KDddDddDK", "KKKKKKKKK"],
          {"K": "ink", "d": "wd2", "D": "wd1"})
    # smoke: soft wisps rising from the vents into the row above
    for (x, y) in ((10, 24), (11, 22), (10, 20), (11, 18), (12, 16), (13, 14), (13, 12), (14, 10),
                   (14, 8), (15, 6), (20, 23), (21, 21), (21, 19), (22, 17), (21, 15), (22, 13),
                   (23, 11), (23, 9), (24, 7), (24, 5)):
        L.px(x, y, "qm3")
        L.px(x + 1, y, "qm2")
        if y < 20:
            L.px(x - 1, y + 1, "qm3")
    for y in range(44, 48):
        for x in range(3, 29):
            if not L.a[y, x, 3] and (x + y) % 2 == 0:
                L.px(x, y, "gd")
    s.T.a[0:16] = L.a[0:16]
    s.M.a[16:48] = L.a[16:48]
    return s


# --------------------------------------------------------------------------
# Ravines, the plank bridge, the cliff split, the shepherd's cave
# --------------------------------------------------------------------------

def chasm():
    names = {"void": (0, 0), "plank": (1, 0), "plank_gap": (2, 0), "plank_face": (3, 0),
             "split": (4, 0), "mouth_L": (0, 1), "mouth_R": (1, 1), "in_L": (2, 1), "in_R": (3, 1),
             "in_dark": (4, 1)}
    s = H.struct("chasm", "Ravines, the plank bridge, the cliff split, the shepherd's cave", 5, 2,
                 SEC, walk=["X.XXX", "TT..."], names=names,
                 notes="`void` a ravine's dark floor, far below (blocks). `plank_face` and `plank` "
                       "the plank bridge over a ravine's lit face and its dark floor (walkable); "
                       "`plank_gap` its broken planks (MB_ICHOR_GAP: the Winged Talaria leap it). "
                       "`split` a split in the cliff path (MB_ICHOR_GAP). The shepherd's cave: "
                       "`mouth_L`/`_R` its arch, drawn over the player, `in_L`/`_R` the floor "
                       "under the back wall, `in_dark` the floor deeper in.")
    # the ravine's floor: darkness with a glimmer of the stream
    v = L16()
    for y in range(16):
        for x in range(16):
            v.px(x, y, "qr0" if (x * 3 + y) % 11 else "qr1")
    for x in range(5, 11):
        v.px(x, 8 + (x % 2), "qr1")
    place(s, "bottom", 0, 0, v)
    # planks over the dark floor, and over the lit face
    for cx, under in ((1, "void"), (2, "void"), (3, "face")):
        d = L16()
        if under == "void":
            for y in range(16):
                for x in range(16):
                    d.px(x, y, "qr0" if (x * 3 + y) % 11 else "qr1")
        else:
            face_fill(d, variant=1)
        broken = cx == 2
        for y in range(16):
            for x in range(4, 12):
                if broken and 5 <= y <= 10 and x not in (4, 11):
                    continue
                c = "wd1" if x in (4, 11) else ("wd1" if y % 4 == 3 else "k1")
                if y % 4 == 3:
                    c = "qr1" if broken and 4 < y < 11 else "k1"
                d.px(x, y, c if x in (4, 11) else ("wd1" if y % 4 != 3 else "k1"))
            d.px(3, y, "ink" if y % 4 else "k1")
            d.px(12, y, "ink" if y % 4 else "k1")
        if broken:
            for (x, y) in ((6, 4), (7, 5), (9, 11), (8, 11)):
                d.px(x, y, "wd1")
            for x in range(5, 11):
                d.px(x, 7, "qr0")
        place(s, "bottom", cx, 0, d)
    s.behaviors[(2, 0)] = "MB_ICHOR_GAP"
    # the cliff split: a crack across the goat path, too wide to step
    d = L16()
    grass_fill(d)
    for y in range(16):
        for x in range(16):
            if 5 + (1 if (y // 4) % 2 else 0) <= x <= 10 - (1 if y % 5 == 0 else 0):
                d.px(x, y, "qr0")
    for y in range(16):
        d.px(4 + (1 if (y // 4) % 2 else 0), y, "qr4")
        d.px(11 - (1 if y % 5 == 0 else 0), y, "qr1")
    place(s, "bottom", 4, 0, d)
    s.behaviors[(4, 0)] = "MB_ICHOR_GAP"
    # the shepherd's cave: an arch in the cliff face, darkness inside
    for cx, side in ((0, "L"), (1, "R")):
        arch, floor = L16(), L16()
        for y in range(16):
            for x in range(16):
                floor.px(x, y, "qr0" if (x + y) % 5 else "qr1")
        face_fill(arch, variant=2)
        for y in range(16):
            for x in range(16):
                # the opening: rounded at its outer top corner
                ox = x if side == "L" else 15 - x
                inside = (y >= 7 and ox >= 4) or (y >= 4 and ox >= 8) or (y >= 2 and ox >= 12)
                if inside:
                    arch.a[y, x] = 0
        for y in range(16):
            for x in range(16):
                if arch.a[y, x, 3] and ((y + 1 < 16 and not arch.a[y + 1, x, 3])
                                        or (x + 1 < 16 and not arch.a[y, x + 1, 3])
                                        or (x - 1 >= 0 and not arch.a[y, x - 1, 3])):
                    arch.px(x, y, "qr0")
        place(s, "bottom", cx, 1, floor)
        place(s, "top", cx, 1, arch)
    for cx in (2, 3):
        d = L16()
        for y in range(16):
            for x in range(16):
                d.px(x, y, "qr0" if (x + y) % 5 else "qr1")
        for y in range(4):
            for x in range(16):
                d.px(x, y, "qr1" if y < 3 else "qr0")
        for (x, y) in ((3, 9), (10, 12), (6, 13)):
            d.px(x, y, "qr2")
        place(s, "bottom", cx, 1, d)
    d = L16()
    for y in range(16):
        for x in range(16):
            d.px(x, y, "qr0" if (x * 7 + y) % 9 else "qr1")
    place(s, "bottom", 4, 1, d)
    return s


# --------------------------------------------------------------------------
# Falling water: the side waterfall and the Styx's thread
# --------------------------------------------------------------------------

def falls():
    names = {"fall_top": (0, 0), "fall": (1, 0), "fall_ledge": (2, 0), "fall_foot": (3, 0),
             "thread_top": (0, 1), "thread": (1, 1), "thread_b": (2, 1), "thread_foot": (3, 1)}
    s = H.struct("falls", "Falling water: the side waterfall and the Styx", 4, 2, SEC,
                 walk=["XXXX", "XXXX"], names=names,
                 notes="Cliff faces with a slit where aethos's animated waterfall shows through. "
                       "`fall_top`, `fall`, `fall_ledge` (a ledge halfway up, something "
                       "glinting on it), `fall_foot`: the side waterfall down the gorge wall "
                       "(Route 11; the Horn of Achelous, Act III). `thread_top` (in mist), "
                       "`thread`, `thread_b`, `thread_foot` (into the black pool): the Styx, one "
                       "long thread down the black cliff.")
    H.ground(s, "fall")
    for cx, kind in enumerate(("top", "mid", "ledge", "foot")):
        d = L16()
        face_fill(d, variant=cx % 3)
        lo, hi = 4, 11
        for y in range(16):
            a = lo + (1 if (y // 5) % 2 else 0)
            b = hi - (1 if (y // 6) % 2 else 0)
            if kind == "top" and y < 4:
                for x in range(16):
                    d.px(x, y, H.grass_px(x, y))
                continue
            for x in range(a, b + 1):
                d.a[y, x] = 0
            d.px(a - 1, y, "qr0")
            d.px(b + 1, y, "qr1")
        if kind == "top":
            for x in range(16):
                d.px(x, 4, "gd" if x < 3 or x > 12 else "qr4")
        if kind == "ledge":
            H.put(d, 11, 9, ["44444", "32221", "K1110"], {**ROCK, "K": "qr0"})
            d.px(13, 8, "qr5")
            d.px(14, 7, "qr5")
        if kind == "foot":
            for y in range(11, 16):
                for x in range(16):
                    if d.a[y, x, 3]:
                        d.px(x, y, "qr1" if (x + y) % 3 else "qr0")
                    elif y > 12:
                        d.px(x, y, "qs1" if (x + y) % 2 else "qm1")
            _recolor(d, {"qr0": "ink", "qr5": "qr4", "qv1": "qv2"})
        place(s, "middle", cx, 0, d)
    for cx, kind in enumerate(("top", "mid", "midb", "foot")):
        d = L16()
        face_fill(d, G.BLACK, ferns=False, variant=(cx + 1) % 3)
        for y in range(16):
            sway = 0 if kind != "midb" else (1 if (y // 8) % 2 else 0)
            a, b = 7 + sway, 9 + sway
            if kind == "foot" and y > 9:
                break
            for x in range(a, b + 1):
                d.a[y, x] = 0
            d.px(a - 1, y, "qb0")
            d.px(b + 1, y, "qb1")
        if kind == "top":
            for y in range(6):
                for x in range(16):
                    if (x * 3 + y * 5) % 7 < 4 - y // 2:
                        d.px(x, y, "qm0" if (x + y) % 2 else "qm1")
        if kind == "foot":
            for y in range(10, 16):
                for x in range(16):
                    d.px(x, y, "qk0" if (x + 3 * y) % 17 else "qk1")
            for (x, y) in ((5, 11), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 11), (6, 12),
                           (10, 12), (8, 13)):
                d.px(x, y, "qm0")
            d.hline(0, 15, 10, "qb1")
            for x in range(6, 11):
                d.px(x, 10, "qm1")
        place(s, "middle", cx, 1, d)
    for cx in range(4):
        s.behaviors[(cx, 0)] = "MB_WATERFALL"
        s.behaviors[(cx, 1)] = "MB_WATERFALL"
    return s


# --------------------------------------------------------------------------
# Terraces: north rims, north ledges, rock-cut stairs
# --------------------------------------------------------------------------

def _stones_row(L, y0, h, light=True, seed=0):
    """A row of rough stones, seen from above, along a terrace's lip."""
    x = 0
    k = seed
    while x < 16:
        w = 3 + (H.hsh(x, k, 13) % 3)
        for yy in range(y0, y0 + h):
            for xx in range(x, min(16, x + w)):
                top = yy < y0 + h // 2
                c = ("qr4" if light else "qr3") if top else "qr2"
                if xx == x + w - 1 or yy == y0 + h - 1:
                    c = "qr1"
                if yy == y0:
                    c = "qr5" if light and xx % 3 else "qr4"
                L.px(xx, yy, c)
        L.vline(min(15, x + w - 1), y0, y0 + h - 1, "qr0")
        x += w
        k += 1


def terraces():
    names = {"rim_L": (0, 0), "rim": (1, 0), "rim_R": (2, 0), "nl_L": (3, 0), "nl": (4, 0),
             "nl_R": (5, 0), "stair": (6, 0), "under": (7, 0)}
    s = H.struct("terraces", "Terrace rims and north ledges", 8, 1, SEC, walk=["XXXJJJ.."],
                 names=names,
                 notes="Where a terrace stands higher to the south, its north edge: `rim_L`, "
                       "`rim`, `rim_R` a rough rocky lip (blocks); `nl_L`, `nl`, `nl_R` a "
                       "dry-stone ledge the player hops north off (MB_JUMP_NORTH), so the way "
                       "back toward Aigion is quick. `stair` rock-cut steps up through a rim. "
                       "`under` the grass in the rim's shadow, for the row north of it.")
    H.ground(s, "grass", [(c, 0) for c in range(8) if c != 6])
    for cx, kind in enumerate(("L", "M", "R")):
        d = L16()
        # the drop: a dark crevice along the top, then the lip of stones, grass above
        for x in range(16):
            for y in range(0, 3):
                d.px(x, y, H.grass_px(x, y) if y < 1 else "gd")
            d.px(x, 3, "qr0")
        _stones_row(d, 4, 7, seed=cx * 3)
        for x in range(16):
            d.px(x, 11, "qr1")
            if x % 3 == 0:
                d.px(x, 12, "qv1")
        if kind == "L":
            for y in range(16):
                for x in range(0, 4 - (y // 5)):
                    d.a[y, x] = 0
        if kind == "R":
            for y in range(16):
                for x in range(12 + (y // 5), 16):
                    d.a[y, x] = 0
        place(s, "middle", cx, 0, d)
    for cx, kind in enumerate(("L", "M", "R")):
        d = L16()
        for x in range(16):
            d.px(x, 2, "gd")
            d.px(x, 3, "qr0")
        for y in range(4, 9):
            for x in range(16):
                c = "qr4" if y == 4 else ("qr3" if y < 7 else "qr2")
                if (x + (y // 2) * 4) % 8 == 7:
                    c = "qr1"
                d.px(x, y, c)
        for x in range(16):
            d.px(x, 9, "qr1")
            d.px(x, 10, "gd" if x % 2 else "g1")
        if kind == "L":
            for y in range(16):
                for x in range(0, 3):
                    d.a[y, x] = 0
        if kind == "R":
            for y in range(16):
                for x in range(13, 16):
                    d.a[y, x] = 0
        place(s, "middle", 3 + cx, 0, d)
    for cx in (3, 4, 5):
        s.behaviors[(cx, 0)] = "MB_JUMP_NORTH"
    # rock-cut stairs: steps rising southward
    d = L16()
    for y in range(16):
        for x in range(16):
            step = y // 4
            c = ("qr2", "qr3", "qr3", "qr4")[step]
            if y % 4 == 0:
                c = "qr1"
            if x in (0, 15):
                c = "qr1"
            if x in (1, 14):
                c = "qr2"
            d.px(x, y, c)
    place(s, "bottom", 6, 0, d)
    # the grass under a rim, in its shadow
    d = L16()
    for y in range(12, 16):
        for x in range(16):
            if (x + y) % 2 == 0 or y > 13:
                d.px(x, y, "gd" if y > 13 else "g1")
    place(s, "middle", 7, 0, d)
    return s


# --------------------------------------------------------------------------
# Nonakris: low stone houses roofed with slabs
# --------------------------------------------------------------------------

def _slab_roof(L, row, side):
    """Grey schist slabs overlapping like scales; the ridge row, then the eave."""
    for y in range(16):
        for x in range(16):
            band = (y + (8 if row == 1 else 0)) // 4
            off = (band % 2) * 4
            c = "qr2" if ((x + off) % 8) < 6 else "qr1"
            if (y % 4) == 0:
                c = "qr3" if ((x + off) % 8) < 6 else "qr2"   # each slab's lit lower lip
            if (y % 4) == 3:
                c = "qr0"
            if ((x + off) % 8) == 7:
                c = "qr0"
            if row == 0 and y < 3:
                c = "qr4" if y == 0 else ("qr3" if y == 1 else "qr0")   # the ridge capping
            if row == 1 and y > 12:
                c = "qr0" if y >= 14 else "qr1"         # the eave's shadow line
            L.px(x, y, c)
    if side == "L":
        for y in range(16):
            L.px(0, y, "qr0")
            L.px(1, y, "qr4" if y % 2 else "qr3")
    if side == "R":
        for y in range(16):
            L.px(15, y, "qr0")
            L.px(14, y, "qr1")


def _rubble_wall(L, side):
    for y in range(16):
        for x in range(16):
            row = y // 4
            off = (row % 2) * 3
            c = "qr4" if ((x + off) % 6) < 5 else "qr2"
            if y % 4 == 3:
                c = "qr2"
            if (x * 7 + y * 3) % 17 == 0:
                c = "qr5"
            if (x * 5 + y) % 13 == 0:
                c = "qr3"
            L.px(x, y, c)
    for x in range(16):
        L.px(x, 0, "qr1")                          # the eave's shadow on the wall's head
        L.px(x, 14, "qr2")
        L.px(x, 15, "qr1")
    if side == "L":
        L.vline(0, 0, 15, "qr0")
    if side == "R":
        L.vline(15, 0, 15, "qr0")
        L.vline(14, 0, 15, "qr1")


def houses():
    names = {"R0_L": (0, 0), "R0_M": (1, 0), "R0_R": (2, 0), "R1_L": (0, 1), "R1_M": (1, 1),
             "R1_R": (2, 1), "W_L": (0, 2), "W_M": (1, 2), "W_R": (2, 2),
             "door": (3, 2), "door_hoof": (4, 2), "window": (5, 2), "lean_to": (6, 2),
             "sledge": (7, 2), "cups": (3, 1), "lamp": (4, 1), "chimney": (3, 0)}
    s = H.struct("houses", "Nonakris: low stone houses with slab roofs", 8, 3, SEC,
                 walk=["XXXX....", "XXXXX...", "XXXDDXXX"], names=names,
                 notes="A roof is R0 (the ridge) over R1 (the eave), L, M repeated, R; under it "
                       "a wall row W_L, W_M..., W_R, with any W cell swapped for `door` (a plank "
                       "door), `door_hoof` (the inn's, a horse's hoof nailed over it), `window`, "
                       "`lean_to` (Kepheus's lean-to of crowbars), `sledge` (his stone-sledge on "
                       "runners). Doors are MB_NON_ANIMATED_DOOR: put the warps there. `chimney` "
                       "an R0 cell with a smoke hole, `cups` an R1 cell with hoof-cups on the sill "
                       "(Horkia's), `lamp` an R1 cell with the never-dark lamp in a niche.")
    for cx, side in enumerate("LMR"):
        for row in (0, 1):
            d = L16()
            _slab_roof(d, row, side)
            place(s, "bottom", cx, row, d)
        d = L16()
        _rubble_wall(d, side)
        place(s, "bottom", cx, 2, d)
    # chimney on a ridge cell
    d = L16()
    _slab_roof(d, 0, "M")
    H.put(d, 5, 2, ["KKKKKK", "K1001K", "K1001K", "KKKKKK"], {**ROCK})
    for (x, y) in ((7, 1), (8, 0), (6, 0)):
        d.px(x, y, "qr4")
    place(s, "bottom", 3, 0, d)
    # eave with hoof-cups on the sill; eave with a lamp niche
    for cx, what in ((3, "cups"), (4, "lamp")):
        d = L16()
        _slab_roof(d, 1, "M")
        if what == "cups":
            for hx in (2, 7, 12):
                H.put(d, hx, 9, ["kk", "11", "kk"], ROCK)
        else:
            H.put(d, 5, 6, ["KKKKKK", "K0000K", "K0dd0K", "K0kk0K", "KKKKKK"], ROCK)
            d.px(7, 7, "qr5")
            d.px(8, 7, "qr5")
        place(s, "bottom", cx, 1, d)
    # doors: dark plank doors in a stone frame
    for cx, hoof in ((3, False), (4, True)):
        d = L16()
        _rubble_wall(d, "M")
        H.put(d, 3, 2, [
            "KKKKKKKKKK",
            "K44444444K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dk1kdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "K4dkdkdk4K",
            "KKKKKKKKKK",
        ], ROCK)
        if hoof:
            H.put(d, 6, 0, ["kddk", "k11k", ".kk."], ROCK)
        place(s, "bottom", cx, 2, d)
        s.behaviors[(cx, 2)] = "MB_NON_ANIMATED_DOOR"
    # a small window with a shutter
    d = L16()
    _rubble_wall(d, "M")
    H.put(d, 4, 4, ["KKKKKKKK", "K444444K", "K400004K", "K400004K", "K4d00d4K", "K444444K",
                    "KKKKKKKK"], ROCK)
    place(s, "bottom", 5, 2, d)
    # Kepheus's lean-to: crowbars and mattocks against the wall
    d = L16()
    _rubble_wall(d, "M")
    for (x, h) in ((3, 11), (6, 12), (9, 10), (12, 12)):
        for y in range(15 - h, 15):
            d.px(x, y, "qr0" if x != 9 else "wd1")
        d.px(x - 1, 15 - h, "qr1")
    d.hline(8, 11, 5, "qr0")
    place(s, "bottom", 6, 2, d)
    # the stone-sledge on its runners, a block on it
    d = L16()
    _rubble_wall(d, "M")
    H.put(d, 1, 6, [
        "....KKKKKK....",
        "...K544332K...",
        "...K433221K...",
        "KKKKKKKKKKKKKK",
        "KddddddddddddK",
        "KKKKKKKKKKKKKK",
        "k............k",
        "kkkkkkkkkkkkkk",
    ], ROCK)
    place(s, "bottom", 7, 2, d)
    return s


# --------------------------------------------------------------------------
# Markers: herms, the shrine of Artemis, the Oath Stone, tortoise boulders,
# the hawk's nest, springs, runnels, dig spots, scree, meadow flowers
# --------------------------------------------------------------------------

def markers():
    names = {"herm_top": (0, 0), "herm": (0, 1), "oath": (1, 1), "tort": (2, 1), "tort_b": (3, 1),
             "tort_big_L": (4, 1), "tort_big_R": (5, 1), "boulder": (6, 1), "nest": (7, 1),
             "dig": (1, 0), "scree": (2, 0), "scree_b": (3, 0), "spring_W": (4, 0),
             "spring_E": (5, 0), "runnel": (6, 0), "runnel_g": (7, 0)}
    s = H.struct("markers", "Herms, stones, springs and runnels", 8, 2, SEC,
                 walk=["T...XX..", "XXXXXXXX"], names=names,
                 notes="On borrowed grass. `herm_top` over `herm`: a great herm, Hermes's bearded "
                       "head on a square pillar, hung with a garland. `oath` the Oath Stone, a "
                       "flat-topped boulder worn smooth by hands. `tort`, `tort_b`, `tort_big_L` + "
                       "`_R`: Kyllene's gray tortoise-shell boulders. `boulder` a grey rock. `nest` "
                       "the hawk's stick nest on its pinnacle (rock all round). `dig` turned earth "
                       "(walkable). `scree`/`scree_b` loose stones (walkable). `spring_W` + `_E` "
                       "Pelasgos's spring: a stone trough fed by a spout (blocks). `runnel` "
                       "snowmelt across the road, `runnel_g` across grass (walkable).")
    H.ground(s, "grass", [(c, r) for c in range(8) for r in range(2)
                          if (c, r) not in ((6, 0), (4, 0), (5, 0), (7, 1))])
    H.ground(s, "path", [(6, 0)])
    H.ground(s, "sea", [(4, 0), (5, 0)])
    # the great herm
    top, bot = L16(), L16()
    H.put(top, 4, 3, [
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
        "wK5443Kw",
        ".vwwwwv.",
    ], ROCK)
    for y in range(16):
        for x in range(5, 11):
            bot.px(x, y, ("qr5", "qr4", "qr4", "qr3", "qr3", "qr2")[x - 5])
        bot.px(4, y, "ink")
        bot.px(11, y, "ink")
    H.put(bot, 2, 12, ["KKKKKKKKKKKK", "K5544433322K", "KKKKKKKKKKKK"], ROCK)
    for (x, y) in ((4, 1), (6, 2), (9, 1), (10, 3), (5, 4), (8, 4)):
        bot.px(x, y, "qv1")
        bot.px(x + 1, y + 1, "qv2")
    shadow(bot, 3, 14, 15)
    place(s, "top", 0, 0, top)
    place(s, "middle", 0, 1, bot)
    # the Oath Stone: flat, worn smooth, palm-polished in the middle
    d = L16()
    H.put(d, 1, 4, [
        "...KKKKKKKK...",
        ".KK55555544KK.",
        "K555555544443K",
        "K554455444332K",
        "K544444443332K",
        "K333333333221K",
        ".K22222222211K",
        "..KKKKKKKKKKK.",
    ], ROCK)
    d.px(7, 6, "qr5"); d.px(8, 6, "qr5"); d.px(7, 7, "qr5")
    shadow(d, 2, 15, 12, 13)
    place(s, "middle", 1, 1, d)
    # tortoise boulders: domed grey shells with scute-like cracks
    for cx, (w, h) in ((2, (6.0, 5.0)), (3, (5.0, 4.2))):
        d = L16()
        m = blob(d, 7.5, 8.0, w, h, ("qr2", "qr3", "qr4", "qr5")[::-1][::-1], "qr0")
        for y, x in np.argwhere(m):
            if (x + y) % 5 == 0 and abs(x - 7.5) < w - 2 and abs(y - 8) < h - 2:
                d.px(x, y, "qr1")
        # a hint of a head poking out, or not
        if cx == 2:
            d.px(13, 9, "qr2"); d.px(14, 9, "qr1")
        shadow(d, 2, 15, 13, 14)
        place(s, "middle", cx, 1, d)
    big = H.Layer(32, 16)
    m = blob(big, 15.5, 8.0, 13.5, 6.0, ("qr2", "qr3", "qr4", "qr5"), "qr0")
    for y, x in np.argwhere(m):
        if ((x // 5) + (y // 4)) % 2 == 0 and (x + y) % 4 == 0:
            big.px(x, y, "qr1")
    shadow(big, 3, 30, 14, 15)
    place(s, "middle", 4, 1, big)
    # a plain boulder
    d = L16()
    blob(d, 7.5, 8.0, 6.5, 5.5, ("qr2", "qr3", "qr4", "qr5"), "ink")
    shadow(d, 2, 15, 14)
    place(s, "middle", 6, 1, d)
    # the hawk's nest on its pinnacle: rock all round, sticks, a glint of paper
    d = L16()
    rock_fill(d)
    m = H.ellipse_mask(16, 16, 7.5, 8.5, 6.0, 4.5)
    for y, x in np.argwhere(m):
        d.px(x, y, "wd1" if (x * 2 + y) % 4 else "k1")
    for (x, y) in ((3, 7), (12, 9), (5, 11), (10, 5), (2, 9), (13, 6)):
        d.line(x, y, x + 2, y - 1, "k1")
    H.put(d, 6, 7, ["KK.", "5K."], {"K": "qr0", "5": "qr5"})
    place(s, "bottom", 7, 1, d)
    # turned earth
    d = L16()
    for y in range(16):
        for x in range(16):
            if ((x - 7.5) / 6) ** 2 + ((y - 8) / 4.5) ** 2 <= 1:
                h = H.hsh(x, y, 4) % 5
                d.px(x, y, "qr1" if h == 0 else ("k1" if h < 3 else "wd1"))
    for (x, y) in ((3, 6), (11, 9), (6, 11)):
        d.px(x, y, "qr3")
    place(s, "middle", 1, 0, d)
    # scree
    for cx, pts in ((2, ((3, 2), (10, 4), (5, 7), (12, 9), (2, 12), (8, 12))),
                    (3, ((2, 3), (8, 2), (12, 6), (4, 9), (10, 11), (6, 13), (13, 13)))):
        d = L16()
        for (x, y) in pts:
            H.put(d, x, y, ["54", "21"], ROCK)
        place(s, "middle", cx, 0, d)
    # Pelasgos's spring: a long stone trough over borrowed water, a spout at the west end
    for cx in (4, 5):
        d = L16()
        for x in range(16):
            for y in (2, 3, 12, 13):
                d.px(x, y, "qr3" if y in (2, 12) else "qr2")
            d.px(x, 1, "qr1")
            d.px(x, 14, "qr0")
            for y in range(15, 16):
                d.px(x, y, "gd" if x % 2 else "g1")
            for y in range(0, 1):
                d.px(x, y, H.grass_px(x, y))
        if cx == 4:
            for y in range(1, 15):
                d.px(0, y, "qr0"); d.px(1, y, "qr3"); d.px(2, y, "qr2")
            H.put(d, 3, 5, ["11", "qq", ".q", ".q"], {"1": "qr1", "q": "qm1"})
        else:
            for y in range(1, 15):
                d.px(15, y, "qr0"); d.px(14, y, "qr2"); d.px(13, y, "qr3")
        for y in range(4, 12):
            for x in range(16):
                if not d.a[y, x, 3] and (x + y) % 9 == 0:
                    d.px(x, y, "qs1")
        _recolor(d, {"qr0": "ink"})
        place(s, "middle", cx, 0, d)
    # runnels: a thread of snowmelt across the road, and across grass
    for cx in (6, 7):
        d = L16()
        for x in range(16):
            yc = 7 + (1 if (x // 4) % 2 else 0)
            for y in range(yc - 1, yc + 2):
                d.px(x, y, "qs0" if y == yc + 1 else ("qs1" if (x + y) % 3 else "qm1"))
            d.px(x, yc - 2, "qr2" if cx == 6 else "qv1")
            d.px(x, yc + 2, "qr3" if cx == 6 else "qv2")
        place(s, "middle", cx, 0, d)
    return s


def shrine():
    """The shrine of Artemis in the cypress glade: a small stone shrine with a
    bronze crescent on its gable, clean and with a sickle scratched across it."""
    names = {"top": (0, 0), "top_R": (1, 0), "base": (0, 1), "base_R": (1, 1),
             "bad_top": (2, 0), "bad_top_R": (3, 0)}
    s = H.struct("shrine", "The forest shrine of Artemis", 4, 2, SEC, walk=["TTTT", "XXXX"],
                 names=names, on="shade",
                 notes="`top`, `top_R` over `base`, `base_R`: the little shrine, its gable with a "
                       "bronze crescent moon. `bad_top`, `bad_top_R`: the gable with a sickle "
                       "scratched across the moon (desecrated); swap them for `top`, `top_R` when "
                       "it's cleansed (METATILE_ArkadiaHeights_Shrine_*). On deep-shade grass.")
    full = H.Layer(32, 32)
    H.put(full, 4, 4, [
        "...........KK...........",
        ".........KK55KK.........",
        ".......KK555544KK.......",
        ".....KK5555444443KK.....",
        "...KK555544444433322KK..",
        ".KK55554444444333322211K",
        "KKKKKKKKKKKKKKKKKKKKKKKK",
        ".K44444444444444433322K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4K1111111111111111K2K.",
        ".K4KKKKKKKKKKKKKKKKKK2K.",
        ".K5444444444444443332K..",
        "KKKKKKKKKKKKKKKKKKKKKKK.",
        "K55554444444433333222K..",
        "KKKKKKKKKKKKKKKKKKKKKK..",
    ], STONE)
    # the crescent on the gable, in bronze
    for (x, y) in ((14, 9), (15, 8), (16, 8), (17, 9), (17, 10), (16, 11), (15, 11), (14, 10)):
        full.px(x, y, "qz")
    full.px(15, 9, "qm3"); full.px(15, 10, "qm3")
    # an offering bowl in the niche
    H.put(full, 13, 17, ["KKKKKK", "K3333K", ".KKKK."], STONE)
    shadow(full, 4, 30, 25, 27)
    bad = H.Layer(32, 16)
    bad.a[:] = full.a[:16]
    for (x, y) in ((12, 7), (13, 8), (14, 9), (15, 10), (16, 11), (17, 11), (18, 10), (19, 9)):
        bad.px(x, y, "qm2")
    s.T.a[0:16, 0:32] = full.a[0:16]
    s.M.a[16:32, 0:32] = full.a[16:32]
    s.T.a[0:16, 32:64] = bad.a
    s.M.a[16:32, 32:64] = full.a[16:32]
    return s


def decor():
    names = {"gentian": (0, 0), "crocus": (1, 0), "thyme": (2, 0), "tuft": (3, 0)}
    s = H.struct("decor", "Kyllene's flowers", 4, 1, SEC, walk=["...."], names=names, on="grass",
                 notes="Walkable, for the open meadow: `gentian` blue gentians, `crocus` yellow "
                       "crocus, `thyme` a cushion of wild thyme, `tuft` a combed tussock.")
    M = s.M
    for (x, y) in ((3, 4), (10, 2), (7, 9), (13, 11), (2, 12)):
        H.put(M, x, y, [".f.", "fFf", ".g."], {"f": "qf1", "F": "qf2", "g": "qg0"})
    for (x, y) in ((4, 3), (11, 6), (6, 11), (13, 13)):
        H.put(M, 16 + x, y, [".y.", "yYy", ".g."], {"y": "qy", "Y": "w0", "g": "qg1"})
    for (x, y) in ((2, 3), (8, 8), (4, 11)):
        H.put(M, 32 + x, y, [".ttt.", "tTtTt", ".ttt."], {"t": "th1", "T": "th2"})
    for (x, y) in ((3, 6), (9, 3), (10, 10)):
        H.put(M, 48 + x, y, ["3.3.3", "23232", "22222", ".1.1."],
              {"3": "qg3", "2": "qg2", "1": "qg0"})
    return s


def rock_detail():
    """Interior cells to scatter through a big rock top: a crack, boulders, a
    juniper, fern, and the same for the Styx's black rock (no plants)."""
    names = {"crack": (0, 0), "boulders": (1, 0), "juniper": (2, 0), "fern": (3, 0),
             "bcrack": (4, 0), "bboulders": (5, 0)}
    s = H.struct("rock_detail", "Rock detail: cracks, boulders, juniper, fern", 6, 1, SEC,
                 walk=["XXXXXX"], names=names,
                 notes="Interior cells (blob key `1|11111111`) to scatter through a big rock top. "
                       "`bcrack`, `bboulders` are the Styx's black rock.")
    for cx, ramp in ((0, G.GREY), (1, G.GREY), (2, G.GREY), (3, G.GREY), (4, G.BLACK), (5, G.BLACK)):
        d = L16()
        rock_fill(d, ramp)
        kind = ("crack", "boulders", "juniper", "fern", "crack", "boulders")[cx]
        if kind == "crack":
            for (x, y) in ((3, 2), (4, 3), (5, 4), (5, 5), (6, 6), (7, 7), (7, 8), (8, 9), (9, 10),
                           (10, 11), (10, 12), (11, 13)):
                d.px(x, y, ramp[0])
                d.px(x + 1, y, ramp[4])
        elif kind == "boulders":
            for (bx, by, r) in ((4, 5, 3.0), (10, 9, 3.5), (5, 12, 2.2)):
                blob(d, bx, by, r, r * 0.85, (ramp[1], ramp[2], ramp[4], ramp[5]), ramp[0])
        elif kind == "juniper":
            m = H.ellipse_mask(16, 16, 7.5, 8, 6, 5)
            for y, x in np.argwhere(m):
                d.px(x, y, "qv1" if (x + y) % 3 else "qv2")
            for y, x in np.argwhere(H.ring(m)):
                d.px(x, y, "qr0")
        elif kind == "fern":
            for (x, y) in ((4, 4), (10, 6), (6, 11), (12, 12)):
                H.put(d, x - 2, y - 1, ["v.v.v", ".www.", "..v.."], ROCK)
        place(s, "bottom", cx, 0, d)
    return s


def build():
    return [ruins(), kiln(), chasm(), falls(), terraces(), houses(), markers(), shrine(), decor(),
            rock_detail()]
