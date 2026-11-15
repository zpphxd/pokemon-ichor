"""Skiron flora: Aleppo pines in four shapes, kermes oak and lentisk scrub,
thyme in flower, dry grass, and the terrace orchard's pomegranate.

Aleppo pines (Pinus halepensis) are the pines of the Isthmus and the
Skironian cliffs: an open, uneven crown of grey-green needle clumps with sky
between them, a grey trunk going red where the bark has split, often leaning
away from the wind. Light falls from the top left; clumps are lit on their
upper left and dark underneath.

Trees are painted whole (trunk, crown, shadow) and then split into cells:
crown in a walk-behind (T) cell goes to the top layer, crown in a blocked (X)
cell to the middle layer, trunk to the bottom layer over painted grass. Cells
with no trunk borrow aethos grass, so a crown over open grass costs no ground
tiles.
"""
from __future__ import annotations

import numpy as np

import agros_flora as AF
from skiron_lib import GRASS, Layer, Struct, ground, oval_shadow

SEC = "flora"
NEEDLES = ["pn0", "pn1", "pn2", "pn3"]


def branch(L, pts, color="rb", width=1):
    """A trunk or limb through points [(x, y, r)], grey bark with red splits,
    lit on its west side."""
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0)) * 2 + 1
        for t in np.linspace(0, 1, n):
            cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r) - 1, int(cy + r) + 2):
                for x in range(int(cx - r) - 1, int(cx + r) + 2):
                    d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                    if d <= r + 0.3:
                        u = (x - cx) / max(r, 0.5)
                        c = "k3" if u < -0.3 else ("rb" if (y + x) % 5 and u < 0.5 else "k1")
                        if r < 1.0:
                            c = "rb"
                        L.px(x, y, c)
    return L


def outline_trunk(L):
    a = L.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if L.get(x, y) != "k3":
            L.px(x, y, "ink")


def compose(s, trunk, crown, shadow=None):
    """Split a tree painted on whole-structure canvases into its cells' layers.

    Every cell borrows aethos grass. A blocked (X) cell flattens shadow, trunk
    and crown into the middle layer: one layer of tiles. A walk-behind (T)
    cell puts its crown in the top layer; if a trunk passes through it too,
    the trunk goes in the bottom layer over painted grass instead."""
    for cy in range(s.h):
        for cx in range(s.w):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            has_trunk = (trunk.a[sl][..., 3] > 0).any()
            code = s.walk[cy][cx]
            layers = [shadow, trunk, crown] if shadow is not None else [trunk, crown]
            if code != "T":
                ground(s, "grass", [(cx, cy)])
                for L in layers:
                    m = L.a[sl][..., 3] > 0
                    s.M.a[sl][m] = L.a[sl][m]
                continue
            if has_trunk:
                s.B.texture(GRASS, cx * 16, cy * 16, 16, 16)
                for L in layers[:-1]:
                    m = L.a[sl][..., 3] > 0
                    s.B.a[sl][m] = L.a[sl][m]
            else:
                ground(s, "grass", [(cx, cy)])
            m = crown.a[sl][..., 3] > 0
            s.T.a[sl][m] = crown.a[sl][m]
    return s


def needle_clumps(L, clumps, rng_seed=0):
    """Open crown: each clump an uneven dome of needle tufts, rim dark,
    lit top left, flecked with light needle tips."""
    AF.foliage(L, clumps, NEEDLES, "pn0", speck="pn3")
    # needle tufts bristling out of the crown's whole edge
    a = L.a[..., 3] > 0
    for y in range(1, L.h - 1):
        for x in range(1, L.w - 1):
            if not a[y, x]:
                continue
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                if not a[y + dy, x + dx] and (x * 5 + y * 3 + rng_seed + dx * 7) % 5 == 0:
                    L.px(x + dx, y + dy, "pn0" if dy > 0 else "pn1")


def pine_tall():
    s = Struct("pine_tall", "Aleppo pine, tall", 2, 3, SEC, walk=["TT", "XX", "XX"],
               notes="An upright Aleppo pine: two tiers of open, grey-green clumps over a "
                     "straight grey trunk. The top row is crown the player walks behind.")
    tr, cr, sh = Layer(32, 48), Layer(32, 48), Layer(32, 48)
    oval_shadow(sh, 16, 44, 13, 3)
    branch(tr, [(15, 47, 2.8), (16, 39, 2.2), (17, 30, 1.7), (16, 20, 1.1)])
    branch(tr, [(17, 32, 1.0), (24, 26, 0.6)])
    branch(tr, [(16, 35, 0.9), (8, 29, 0.6)])
    outline_trunk(tr)
    needle_clumps(cr, [(10, 7, 6, 5), (21, 6, 6, 5), (16, 3, 5, 3), (5, 15, 5, 5), (15, 13, 7, 5),
                       (26, 15, 5, 5), (9, 23, 6, 4), (22, 23, 6, 4), (15, 28, 5, 3)])
    return compose(s, tr, cr, sh)


def pine_lean():
    s = Struct("pine_lean", "Aleppo pine, leaning", 3, 3, SEC, walk=["TTT", "TXT", "XX."],
               notes="A pine leaning east, its crown thrown out past its roots: for the cliff "
                     "edge (lean it over the drop) and the slopes. `pine_lean_w` leans west. "
                     "Its roots are the bottom-left two cells.")
    tr, cr, sh = Layer(48, 48), Layer(48, 48), Layer(48, 48)
    oval_shadow(sh, 22, 44, 16, 3)
    branch(tr, [(12, 47, 2.6), (14, 39, 2.1), (19, 31, 1.7), (26, 24, 1.3), (33, 17, 1.0)])
    branch(tr, [(21, 29, 1.0), (17, 22, 0.6)])
    branch(tr, [(28, 22, 0.9), (31, 19, 0.6)])
    outline_trunk(tr)
    needle_clumps(cr, [(14, 16, 6, 5), (23, 9, 7, 6), (34, 6, 7, 5), (43, 12, 5, 5), (32, 16, 7, 5),
                       (19, 4, 5, 4), (41, 21, 5, 4), (24, 20, 5, 4)], 3)
    s = compose(s, tr, cr, sh)
    m = Struct("pine_lean_w", "Aleppo pine, leaning west", 3, 3, SEC, walk=["TTT", "TXT", ".XX"],
               notes="The mirror of pine_lean.")
    for ln in ("bottom", "middle", "top"):
        m.layers[ln].a[:] = s.layers[ln].a[:, ::-1]
    m.ground = {(2 - x, y): k for (x, y), k in s.ground.items()}
    return [s, m]


def pine_young():
    s = Struct("pine_young", "Aleppo pine, young", 1, 2, SEC, walk=["T", "X"],
               notes="A young pine, still conical. Scatter among the others and on the "
                     "cliff top.")
    tr, cr, sh = Layer(16, 32), Layer(16, 32), Layer(16, 32)
    oval_shadow(sh, 8, 29, 6, 2)
    branch(tr, [(8, 31, 1.3), (8, 22, 0.8)])
    outline_trunk(tr)
    needle_clumps(cr, [(8, 3, 3, 3), (6, 9, 4, 3), (10, 10, 4, 3), (8, 15, 6, 4), (4, 20, 3, 3),
                       (12, 20, 3, 3), (8, 21, 4, 3)], 1)
    return compose(s, tr, cr, sh)


def pine_wind():
    s = Struct("pine_wind", "Aleppo pine, windswept", 2, 2, SEC, walk=["TT", "XX"],
               notes="A low pine on the cliff top, its flat crown streaming east from the "
                     "sea wind. Its trunk is the bottom-left cell.")
    tr, cr, sh = Layer(32, 32), Layer(32, 32), Layer(32, 32)
    oval_shadow(sh, 16, 29, 13, 2)
    branch(tr, [(8, 31, 2.0), (9, 25, 1.6), (13, 19, 1.2), (20, 15, 0.9)])
    branch(tr, [(12, 21, 0.8), (6, 15, 0.5)])
    outline_trunk(tr)
    needle_clumps(cr, [(8, 11, 5, 3), (17, 9, 7, 4), (27, 11, 5, 3), (23, 15, 5, 3), (12, 6, 4, 2)], 5)
    return compose(s, tr, cr, sh)


# --------------------------------------------------------------------------
# Scrub and herbs
# --------------------------------------------------------------------------

def oak_bush(key, title, clusters, notes):
    s = Struct(key, title, 1, 1, SEC, walk=["X"], notes=notes)
    ground(s, "grass")
    oval_shadow(s.M, 8, 14, 7, 2)
    AF.foliage(s.M, clusters, ["c1", "c2", "c3", "g1"], "c1", speck="g3")
    # the prickly holly-like leaf edge of kermes oak
    a = s.M.a[..., 3] > 0
    for y in range(1, 15):
        for x in range(1, 15):
            if a[y, x] and not a[y - 1, x] and (x + y) % 3 == 0:
                s.M.px(x, y - 1, "c1")
    return s


def scrub():
    out = [
        oak_bush("oak", "Kermes oak", [(5, 9, 5, 5), (11, 8, 5, 5), (8, 5, 5, 4)],
                 "A low, prickly kermes oak, the hill scrub of the Isthmus. Impassable."),
        oak_bush("lentisk", "Lentisk bush", [(4, 10, 4, 4), (9, 7, 5, 4), (12, 11, 4, 4), (7, 12, 5, 3)],
                 "Mastic lentisk, rounder and brighter than the oak. Impassable."),
    ]
    s = Struct("thicket", "Scrub thicket, 2 by 2", 2, 2, SEC, walk=["XX", "XX"],
               notes="Oak and lentisk grown together round a grey rock: a hillside wall that "
                     "isn't trees. Impassable.")
    ground(s, "grass")
    oval_shadow(s.M, 16, 28, 15, 3)
    s.M.ellipse(17, 14, 29, 26, "ink")
    s.M.ellipse(18, 15, 28, 25, "k3")
    s.M.ellipse(18, 15, 24, 20, "k3")
    s.M.ellipse(22, 19, 28, 25, "k1")
    AF.foliage(s.M, [(7, 10, 7, 6), (13, 6, 6, 5), (6, 21, 6, 5), (14, 22, 5, 5), (26, 9, 5, 5),
                     (24, 25, 6, 4)], ["c1", "c2", "c3", "g1"], "c1", speck="g3")
    out.append(s)
    for key, title, pts in (("thyme", "Thyme in flower", [(2, 3), (8, 6), (3, 10)]),
                            ("thyme2", "Thyme in flower, sparse", [(6, 2), (1, 9), (9, 10)])):
        t = Struct(key, title, 1, 1, SEC, walk=["."],
                   notes="Low cushions of wild thyme in purple flower; walkable. The bees' "
                         "pasture.")
        ground(t, "grass")
        for (x, y) in pts:
            t.M.blit([" dd ",
                      "dTtd",
                      "dtTtd",
                      " ddd "], {"d": "gd", "t": "th1", "T": "th2"}, x, y)
        out.append(t)
    for key, title, tufts in (("dry_grass", "Dry grass", [(2, 3), (9, 2), (5, 9), (12, 10)]),
                              ("dry_grass2", "Dry grass and bare earth", [(3, 2), (11, 6), (2, 11)])):
        t = Struct(key, title, 1, 1, SEC, walk=["."],
                   notes="Sun-dried tufts and bare earth on the grass; walkable. Breaks up open "
                         "ground on the hills and the cliff top.")
        ground(t, "grass")
        if key == "dry_grass2":
            for (x, y) in ((6, 9), (7, 9), (8, 9), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
                           (6, 11), (7, 11), (8, 11)):
                t.M.px(x, y, "l1" if (x + y) % 3 else "p1")
        for (x, y) in tufts:
            t.M.blit([" t t", "tgtg", " tt "], {"t": "tg", "g": "t3"}, x, y)
        out.append(t)
    return out


def pomegranate():
    s = Struct("pomegranate", "Pomegranate tree", 2, 2, SEC, walk=["TT", "XX"],
               notes="The terrace orchard's tree: a rounded crown of glossy leaves, red fruit "
                     "and scarlet flowers, on a short twisted trunk. Kore's fruit, growing on "
                     "the road to Eleusa. The top row is walk-behind crown.")
    tr, cr, sh = Layer(32, 32), Layer(32, 32), Layer(32, 32)
    oval_shadow(sh, 16, 29, 12, 2)
    for (x0, y0), (x1, y1) in (((15, 31), (16, 22)), ((16, 24), (11, 19)), ((16, 23), (21, 18))):
        tr.line(x0, y0, x1, y1, "k1")
        tr.line(x0 + 1, y0, x1 + 1, y1, "k1")
    AF.foliage(cr, [(9, 10, 7, 6), (20, 9, 7, 6), (15, 5, 6, 4), (7, 17, 5, 4), (24, 17, 5, 4),
                    (15, 15, 7, 5)], ["c1", "c2", "c3", "g3"], "c1", speck="g3")
    for (x, y) in ((8, 9), (19, 6), (24, 12), (12, 15), (20, 17), (5, 16), (16, 11)):
        cr.blit([" r ", "rRr", " r "], {"r": "op1", "R": "op2"}, x - 1, y - 1)
    for (x, y) in ((13, 4), (27, 9), (10, 20)):
        cr.px(x, y, "tg")
    return compose(s, tr, cr, sh)


def build():
    # Held for the tile budget (draw them in a later set if a map needs them):
    # pine_wind(), pomegranate(), the thicket, lentisk, thyme2 and dry_grass2.
    keep = {"oak", "thyme", "dry_grass"}
    return [pine_tall(), *pine_lean(), pine_young(), *[s for s in scrub() if s.key in keep]]
