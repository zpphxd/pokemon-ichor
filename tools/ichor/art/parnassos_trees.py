"""Parnassos's trees: bay laurels, wild olives, plane trees, scrub and flowers.

Light from the top left. Every tree stands on borrowed aethos grass, so its
grass costs no tiles. A tree's top row is a walk-behind cell (top layer), as
aethos's olives are.

  laurel        Apollo's bay laurel, 2 x 3: a dense dark egg of glossy leaves
  laurel_young  a young laurel, 1 x 2, for gaps in the scrub
  wild_olive    the oleaster of the terraces, 2 x 2: a gnarled two-stemmed trunk
                under thin silver-green leaves
  plane         the oriental plane of Lebadeia's grove, 3 x 3: a great spreading
                crown over a pale mottled trunk; its lower corners are walk-behind
  scrub         a kermes oak bush, 1 x 1, for laurel-scrub edges
  meadow        walkable flowers: broom, white asphodel, a tussock
"""
from __future__ import annotations

import numpy as np

import parnassos_lib as P

SEC = "trees"
LAUREL = ["lr0", "lr1", "lr2", "lr3"]


def _trunk(L, x0, y0, y1, w=3, dark="k1", lit="k2"):
    for y in range(y0, y1):
        for x in range(x0, x0 + w):
            L.px(x, y, lit if x == x0 else dark)


def laurels():
    out = []
    s = P.struct("laurel", "Bay laurel (2 x 3)", 2, 3, SEC, walk=["TT", "XX", "XX"], on="grass",
                 notes="Apollo's tree: a dense dark egg of glossy leaves on a slim grey trunk. "
                       "The top row is drawn over the player.")
    tmp = P.Layer(32, 48)
    _trunk(tmp, 15, 34, 44, 3)
    tmp.px(14, 43, "k1"); tmp.px(18, 43, "k1")
    P.blobs_crown(tmp, 0, 0, 32, 48,
                  [(16, 12, 9, 9), (10, 20, 8, 9), (22, 20, 8, 9), (16, 27, 11, 8), (12, 31, 7, 5),
                   (21, 31, 7, 5), (16, 6, 6, 6)],
                  LAUREL, "lr0", speck="lr3")
    # glossy leaf glints, high on the lit side
    for (x, y) in ((11, 9), (14, 6), (8, 17), (12, 14), (17, 10), (6, 23), (10, 26), (15, 20),
                   (20, 15), (9, 31)):
        tmp.px(x, y, "lr3")
        tmp.px(x + 1, y, "lr2")
    P.shadow_alpha(tmp, 16, 44.5, 12, 3.2, 2, 40, 31, 48)
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:48] = tmp.a[16:48]
    out.append(s)

    # a laurel's base row with the next laurel's crown top over it, for woods
    # where laurels stand one behind another: a column repeats crown, stack,
    # crown, stack... and ends with a base
    st = P.struct("laurel_stack", "A laurel's base with the next laurel's crown over it", 2, 1, SEC,
                  walk=["XX"], on="grass",
                  notes="Between two laurels in a column: the upper laurel's base row, the "
                        "lower laurel's crown top over it. Blocks.")
    st.M.a[:] = tmp.a[32:48]
    top = tmp.a[0:16]
    msk = top[..., 3] > 0
    st.M.a[msk] = top[msk]
    out.append(st)

    y = P.struct("laurel_young", "Young laurel (1 x 2)", 1, 2, SEC, walk=["T", "X"], on="grass",
                 notes="A sapling laurel for gaps in the scrub. Its top half is drawn over the "
                       "player.")
    tmp = P.Layer(16, 32)
    _trunk(tmp, 7, 22, 29, 2)
    P.blobs_crown(tmp, 0, 0, 16, 32, [(8, 9, 5, 6), (8, 17, 6, 6), (8, 4, 3, 3)], LAUREL, "lr0",
                  speck="lr3")
    P.shadow_alpha(tmp, 8, 29.5, 6, 2.2, 1, 27, 15, 32)
    y.T.a[0:16] = tmp.a[0:16]
    y.M.a[16:32] = tmp.a[16:32]
    out.append(y)
    return out


def wild_olive():
    s = P.struct("wild_olive", "Wild olive (2 x 2)", 2, 2, SEC, walk=["TT", "XX"], on="grass",
                 notes="The oleaster of Parnassos's terraces: a gnarled two-stemmed trunk under "
                       "thin silver-green leaves. The top row is drawn over the player.")
    tmp = P.Layer(32, 32)
    # two twisting stems from one root
    for i, (x, y) in enumerate([(15, 29), (15, 28), (14, 27), (14, 26), (13, 25), (13, 24), (12, 23),
                                (12, 22), (11, 21), (11, 20)]):
        tmp.px(x, y, "k1"); tmp.px(x + 1, y, "k2"); tmp.px(x + 2, y, "k1")
    for (x, y) in [(17, 27), (18, 26), (18, 25), (19, 24), (19, 23), (20, 22), (20, 21), (21, 20)]:
        tmp.px(x, y, "k2"); tmp.px(x + 1, y, "k1")
    tmp.px(14, 30, "k1"); tmp.px(18, 30, "k1"); tmp.px(13, 30, "k1")
    m = P.blobs_crown(tmp, 0, 0, 32, 32,
                      [(10, 11, 8, 6), (21, 9, 8, 6), (16, 5, 7, 4), (6, 16, 5, 4), (25, 15, 5, 4),
                       (15, 15, 7, 4)],
                      ["lr1", "lr2", "o4", "o5"], "lr0")
    # the thin crown lets light and branches through
    for (x, y) in ((9, 12), (13, 9), (19, 13), (23, 10), (17, 7), (7, 15), (26, 14), (12, 16),
                   (20, 16), (15, 12)):
        tmp.px(x, y, "k1")
        tmp.px(x + 1, y + 1, "lr1")
    for (x, y) in ((8, 8), (12, 6), (18, 5), (22, 6), (5, 13), (14, 3), (25, 12), (10, 13)):
        tmp.px(x, y, "o5")
    P.shadow_alpha(tmp, 16, 29.5, 11, 2.6, 2, 26, 31, 32)
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:32] = tmp.a[16:32]
    return s


def plane():
    s = P.struct("plane", "Plane tree (3 x 3)", 3, 3, SEC, walk=["TTT", "XXX", "TXT"], on="grass",
                 notes="The oriental plane of Lebadeia's grove: a great spreading crown over a "
                       "pale mottled trunk. The top row and the bottom corners are drawn over "
                       "the player; the trunk and the crown's middle row block.")
    tmp = P.Layer(48, 48)
    # the trunk: pale, peeling, mottled grey-cream and olive-grey
    for y in range(26, 44):
        half = 3 if y < 38 else 3 + (y - 37) // 2
        for x in range(24 - half, 24 + half + 1):
            h = P.hsh(x, y, 5) % 7
            c = "w1" if h < 2 else ("k3" if h < 5 else "k2")
            if x == 24 + half:
                c = "k2"
            if x == 24 - half:
                c = "k3"
            tmp.px(x, y, c)
    for (x, y) in ((22, 30), (25, 34), (23, 39), (26, 29)):
        tmp.px(x, y, "o4")
    # the crown, broad and lobed
    blobs = [(24, 14, 17, 11), (11, 17, 10, 9), (37, 17, 10, 9), (17, 7, 10, 7), (31, 7, 10, 7),
             (24, 24, 14, 7), (8, 24, 7, 5), (40, 24, 7, 5)]
    m = P.blobs_crown(tmp, 0, 0, 48, 48, blobs, ["lr1", "lr2", "lr3", "o5"], "lr0", speck="o4")
    # the crown's underside in shade, over the trunk
    for y in range(20, 33):
        for x in range(48):
            if m[y, x] and (y + 1 >= 48 or not m[min(47, y + 3), x]) and tmp.get(x, y) != "lr0":
                tmp.px(x, y, "lr1" if (x + y) % 3 else "lr0")
    # big palmate leaves: little bright clusters on the lit side
    for (x, y) in ((10, 11), (16, 5), (22, 9), (29, 4), (7, 18), (14, 14), (34, 10), (19, 17),
                   (28, 13), (12, 23)):
        P.put(tmp, x, y, [".3.", "323", ".2."], {"3": "lr3", "2": "lr2"})
    for (x, y) in ((30, 22), (38, 20), (25, 26), (41, 25), (34, 27)):
        P.put(tmp, x, y, [".1.", "101"], {"1": "lr1", "0": "lr0"})
    P.shadow_alpha(tmp, 24, 44.5, 18, 3.4, 2, 40, 47, 48)
    s.T.a[0:16] = tmp.a[0:16]
    s.M.a[16:32] = tmp.a[16:32]
    s.T.a[32:48, 0:16] = tmp.a[32:48, 0:16]
    s.T.a[32:48, 32:48] = tmp.a[32:48, 32:48]
    s.M.a[32:48, 16:32] = tmp.a[32:48, 16:32]
    return s


def scrub():
    s = P.struct("scrub", "Scrub: kermes oak and laurel bushes", 3, 1, SEC, walk=["XXX"], on="grass",
                 names={"oak": (0, 0), "laurel": (1, 0), "pair": (2, 0)},
                 notes="Low bushes for the laurel scrub along the road: `oak` a round kermes "
                       "oak, `laurel` a young bay, `pair` two small bushes. Block.")
    M = s.M
    P.blobs_crown(M, 0, 0, 16, 16, [(8, 8, 7, 5.5), (5, 6, 4, 4), (11, 6, 4, 4)],
                  ["lr1", "lr2", "lr3"], "lr0", speck="o4")
    P.blobs_crown(M, 16, 0, 16, 16, [(8, 7, 5, 6), (8, 10, 6.5, 4.5)], LAUREL, "lr0", speck="lr3")
    P.blobs_crown(M, 32, 0, 16, 16, [(5, 9, 4.5, 4), (11, 7, 4.5, 4.5)], ["lr1", "lr2", "lr3"],
                  "lr0")
    for cx in range(3):
        P.shadow_alpha(M, cx * 16 + 8, 14.5, 7, 1.6, cx * 16, 12, cx * 16 + 16, 16)
    return s


def meadow():
    s = P.struct("meadow", "Mountain flowers and a tussock", 3, 1, SEC, walk=["..."], on="grass",
                 names={"broom": (0, 0), "white": (1, 0), "tuft": (2, 0)},
                 notes="Walkable. Scatter through open grass with aethos's red anemones (0x004): "
                       "`broom` yellow Spanish broom, `white` asphodel, `tuft` a tussock.")
    M = s.M
    for (x, y) in ((3, 3), (10, 2), (6, 9), (12, 11)):
        P.put(M, x, y, [".y.", "yty", ".1.", ".1."], {"y": "tg", "t": "t3", "1": "t1"})
    for (x, y) in ((4, 4), (11, 7), (5, 11)):
        P.put(M, 16 + x, y, [".w.", "wtw", ".w.", ".1.", ".1."], {"w": "p3", "t": "tg", "1": "t1"})
    for (x, y) in ((3, 6), (9, 3), (10, 10)):
        P.put(M, 32 + x, y, ["3.3.3", "13131", "11111", ".t.t."], {"3": "t3", "1": "t1", "t": "t0"})
    return s


def build():
    return laurels() + [wild_olive(), plane(), scrub(), meadow()]
