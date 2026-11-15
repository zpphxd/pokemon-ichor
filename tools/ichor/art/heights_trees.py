"""The climb's trees: black firs and kermes oak (Kithairon's painters, so the
two mountains share a look), and the cypresses where Kyllene drops toward
Arkadia. Light from the top left; every tree stands on borrowed aethos grass.

  fir, fir_b, fir_stack(_b), fir_young, oak   Kithairon's, verbatim
  *_shade        the same on aethos's deep-shade grass, for inside a wood
  cypress        a tall cypress, 1 x 3: spire (T), crown, foot
  cypress_stack  a cypress's foot with the next cypress's spire over it
"""
from __future__ import annotations

import numpy as np

import heights_lib as H
import kithairon_trees

SEC = "trees"


def _cypress_mask(h=48, w=16, cx=7.5):
    """A cypress's flame: narrow at the tip, fullest two-thirds down."""
    m = np.zeros((h, w), bool)
    for y in range(2, h - 4):
        t = (y - 2) / (h - 8)
        half = 1.0 + 5.6 * (t ** 0.6) * (1.0 - 0.35 * max(0.0, t - 0.75) / 0.25)
        for x in range(w):
            d = abs(x + 0.5 - cx - 0.5)
            jag = 0.6 if (x + y) % 3 == 0 else 0.0
            if d <= half - jag:
                m[y, x] = True
    return m


def paint_cypress(L, ox, oy):
    m = _cypress_mask()
    for y, x in np.argwhere(m):
        d = x + 0.5 - 8.0
        edge = not (0 < y < 47 and 0 < x < 15 and m[y - 1, x] and m[y, x - 1] and m[y, x + 1])
        tuft = (y // 3 + x // 2) % 3
        if edge:
            c = "fr0"
        elif d < -1.5:
            c = "fr2" if tuft else "fr3"
        elif d < 1.5:
            c = "fr1" if tuft != 1 else "fr2"
        else:
            c = "fr0" if tuft == 0 else "fr1"
        L.px(ox + x, oy + y, c)
    for y in range(43, 47):
        for x in range(7, 9):
            L.px(ox + x, oy + y, "k1")
    for y in range(44, 48):
        for x in range(3, 13):
            if not L.a[oy + y, ox + x, 3] and (x + y) % 2 == 0:
                L.px(ox + x, oy + y, "gd")


def cypresses():
    s = H.struct("cypress", "Cypress (1 x 3 with its spire)", 1, 3, SEC, walk=["T", "X", "X"],
                 on="grass", notes="A tall Arkadian cypress. The top row is its spire over the "
                                   "grass of the row above: walkable, drawn over the player.")
    tmp = H.Layer(16, 48)
    paint_cypress(tmp, 0, 0)
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:48] = tmp.a[16:48]
    st = H.struct("cypress_stack", "A cypress's foot with the next one's spire over it", 1, 1, SEC,
                  walk=["X"], on="grass",
                  notes="Between two cypresses in a column: the upper one's foot, the lower one's "
                        "spire over it. Blocks.")
    st.M.a[:] = tmp.a[32:48]
    sp = tmp.a[0:16]
    msk = sp[..., 3] > 0
    st.M.a[msk] = sp[msk]
    return [s, st]


def build():
    out = []
    for s in kithairon_trees.firs() + kithairon_trees.broadleaves()[:1]:
        out.append(s)
    out += cypresses()
    shades = []
    for s in out:
        sh = H.E.on_other_ground(s, s.key + "_shade", "shade", title=s.title + ", in the woods' shade")
        sh.notes = ("The same as `" + s.key + "`, on aethos's deep-shade grass, for inside a wood. "
                    "The spire row stays on plain grass: use `" + s.key + "`'s top row there.")
        shades.append(sh)
    return out + shades
