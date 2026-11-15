"""64x64 dialogue portraits of the Theoxenia's two gods drawn from life, in
their disguises: Sam (Apollo, the herdsman with the lyre) and Cami (Demeter
by the Maiden's Well). See design/SYSTEMS.md §10.

Usage:
    python3 tools/ichor/art/portraits_theoxenia.py [--write] [--preview DIR]

--write    writes graphics/trainers/front_pics/sam.png and cami.png (64x64,
           4bpp indexed, color 0 transparent, Gen 3 trainer-pic format).
           Nothing displays them yet; they sit with the trainer front pics
           until a dialogue portrait window is routed.
--preview  writes DIR/<name>_x8.png and an 8x pixel grid for editing

Each portrait is painted in layers: flat masses (hair, face, ears, neck,
clothes) with PIL shapes, then shading shapes clipped to a mass, then a dark
outline round the silhouette and where hair meets skin, then the hand-placed
features (brows, eyes, nose, mouth, stubble, hair locks) as ASCII patches.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402

FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")
N = 64


class Canvas:
    """A 64x64 index map painted in named colors from a Palette."""

    def __init__(self, pal, legend):
        self.pal = pal
        self.legend = legend
        self.a = np.zeros((N, N), np.int32)

    def _mask(self, fn):
        im = Image.new("L", (N, N), 0)
        fn(ImageDraw.Draw(im))
        return np.array(im) > 0

    def _paint(self, m, color, clip):
        if clip is not None:
            clip = [clip] if isinstance(clip, str) else clip
            m &= np.isin(self.a, [self.pal[c] for c in clip])
        self.a[m] = 0 if color == "_" else self.pal[color]

    def poly(self, pts, color, clip=None):
        self._paint(self._mask(lambda d: d.polygon([tuple(p) for p in pts], fill=255, outline=255)),
                    color, clip)

    def ellipse(self, box, color, clip=None):
        self._paint(self._mask(lambda d: d.ellipse(box, fill=255, outline=255)), color, clip)

    def dither(self, pts, color, clip=None, phase=0):
        """Paint every other pixel of a polygon, in a checker: stubble."""
        m = self._mask(lambda d: d.polygon([tuple(p) for p in pts], fill=255, outline=255))
        yy, xx = np.mgrid[0:N, 0:N]
        self._paint(m & ((xx + yy) % 2 == phase), color, clip)

    def line(self, pts, color, width=1, clip=None):
        self._paint(self._mask(lambda d: d.line([tuple(p) for p in pts], fill=255, width=width)),
                    color, clip)

    def patch(self, x0, y0, rows, legend=None, clip=None):
        """ASCII patch: '.' and ' ' leave a pixel alone, '_' clears it.
        With `clip`, only pixels already in those colors change."""
        legend = legend or self.legend
        keep = None if clip is None else {self.pal[c] for c in clip}
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in ". ":
                    continue
                x, y = x0 + i, y0 + j
                if 0 <= x < N and 0 <= y < N and (keep is None or self.a[y, x] in keep):
                    self.a[y, x] = 0 if ch == "_" else self.pal[legend[ch]]

    def outline(self, color, inside=None):
        """Gen 3 silhouette line: every figure pixel touching transparency
        (4-neighbour) takes `color`, unless it is already in `inside`."""
        a = self.a
        fig = a > 0
        edge = np.zeros_like(fig)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.zeros_like(fig)
            ys = slice(max(dy, 0), N + min(dy, 0))
            yd = slice(max(-dy, 0), N + min(-dy, 0))
            xs = slice(max(dx, 0), N + min(dx, 0))
            xd = slice(max(-dx, 0), N + min(-dx, 0))
            sh[yd, xd] = ~fig[ys, xs]
            edge |= sh
        edge &= fig
        # the frame's own bottom edge is a crop, not a silhouette
        edge[N - 1, :] = False
        if inside:
            edge &= ~np.isin(a, [self.pal[c] for c in inside])
        a[edge] = self.pal[color]

    def border(self, inner, outer, color):
        """Pixels of `inner` colors with a 4-neighbour in `outer` colors take `color`."""
        a = self.a
        ins = np.isin(a, [self.pal[c] for c in inner])
        out = np.isin(a, [self.pal[c] for c in outer])
        nb = np.zeros_like(out)
        nb[1:] |= out[:-1]
        nb[:-1] |= out[1:]
        nb[:, 1:] |= out[:, :-1]
        nb[:, :-1] |= out[:, 1:]
        a[ins & nb] = self.pal[color]

    def seam(self, upper, lower, color):
        """Line the pixels of `upper` colors that sit directly on `lower`
        colors (a hair edge over skin, say) in `color`."""
        a = self.a
        up = np.isin(a, [self.pal[c] for c in upper])
        lo = np.isin(a, [self.pal[c] for c in lower])
        m = np.zeros_like(up)
        m[:-1] = up[:-1] & lo[1:]
        a[m] = self.pal[color]


def legend_of(colors):
    return {ch: name for ch, name, _ in colors}


def palette_of(colors):
    return Palette([(name, rgb) for _, name, rgb in colors])


# ==========================================================================
# Sam
# ==========================================================================

SAM_COLORS = [
    ("k", "ink", (40, 24, 24)),
    ("h", "hair_d", (56, 32, 32)),
    ("H", "hair_m", (88, 56, 48)),
    ("j", "hair_l", (128, 88, 64)),
    ("S", "skin_l", (248, 216, 192)),
    ("m", "skin_m", (240, 184, 152)),
    ("d", "skin_d", (208, 136, 112)),
    ("D", "skin_dd", (160, 96, 80)),
    ("b", "stub_l", (184, 136, 112)),
    ("B", "stub_d", (128, 88, 72)),
    ("W", "white", (248, 248, 240)),
    ("c", "cloth", (224, 208, 176)),
    ("C", "cloth_d", (176, 160, 136)),
    ("g", "cloak", (128, 112, 96)),
    ("o", "gold", (232, 184, 72)),
]


def sam():
    pal = palette_of(SAM_COLORS)
    c = Canvas(pal, legend_of(SAM_COLORS))
    # --- clothes: an undyed wool tunic, the grey-brown cloak over his right
    # shoulder, pinned with a plain bronze pin
    c.poly([(3, 63), (7, 54), (14, 49), (24, 46), (32, 50), (40, 46), (50, 49), (57, 54), (61, 63)], "cloth")
    c.poly([(29, 48), (35, 48), (32, 56)], "cloth_d", clip="cloth")
    c.poly([(44, 52), (52, 50), (58, 55), (61, 63), (47, 63)], "cloth_d", clip="cloth")
    c.poly([(3, 63), (6, 55), (12, 50), (22, 47), (26, 50), (22, 56), (20, 63)], "cloak")
    c.poly([(6, 58), (9, 55), (14, 63), (9, 63)], "hair_m", clip="cloak")
    c.poly([(15, 56), (19, 52), (21, 63), (17, 63)], "hair_m", clip="cloak")
    # the lyre's gold horns rising past his left arm: too fine for a herdsman
    c.poly([(48, 63), (49, 56), (51, 52), (53, 52), (52, 56), (51, 63)], "gold")
    c.poly([(56, 63), (56, 56), (58, 52), (60, 52), (59, 56), (59, 63)], "gold")
    c.poly([(50, 57), (59, 57), (59, 58), (50, 58)], "gold")
    # --- neck, in the jaw's shadow
    c.poly([(26, 37), (38, 37), (39, 48), (32, 51), (25, 48)], "skin_m")
    c.poly([(25, 37), (39, 37), (39, 45), (25, 43)], "skin_d")
    # --- ears, set low beside short sides
    c.ellipse((16, 21, 22, 32), "skin_m")
    c.ellipse((42, 21, 48, 32), "skin_d")
    c.patch(17, 24, ["mdd", "mDd", "mDd", ".md"])
    c.patch(44, 24, ["dDd", "dDD", "dDd", "dd."])
    # --- face: broad, full round cheeks, a wide jaw
    face = [(22, 14), (28, 13), (36, 13), (42, 15), (44, 19), (45, 24), (45, 30), (44, 34), (42, 38),
            (39, 41), (35, 43), (29, 43), (25, 41), (22, 38), (20, 34), (19, 30), (19, 24), (20, 18)]
    c.poly(face, "skin_m")
    c.ellipse((21, 14, 37, 32), "skin_l", clip="skin_m")
    c.poly([(40, 16), (44, 19), (45, 24), (45, 30), (44, 34), (42, 38), (39, 41), (35, 43), (34, 41),
            (39, 35), (41, 28), (41, 21)], "skin_d", clip=["skin_m", "skin_l"])
    # --- stubble: a short beard over the jaw and chin and on the lip, its
    # upper edge broken up where it fades into the cheeks
    skin = ["skin_m", "skin_l", "skin_d"]
    beard = [(19, 30), (21, 34), (24, 37), (27, 38), (37, 38), (40, 37), (43, 34), (45, 30), (45, 31),
             (44, 34), (42, 38), (39, 41), (35, 43), (29, 43), (25, 41), (22, 38), (20, 34)]
    c.poly(beard, "stub_l", clip=skin)
    c.dither([(19, 29), (23, 34), (27, 37), (37, 37), (41, 34), (45, 29), (45, 31), (41, 36), (37, 38),
              (27, 38), (23, 36), (19, 31)], "stub_l", clip=skin)
    c.poly([(26, 30), (38, 30), (38, 32), (26, 32)], "stub_l", clip=skin)
    c.dither([(25, 29), (39, 29), (39, 30), (25, 30)], "stub_l", clip=skin, phase=1)
    # the beard's shadow: the far side of the jaw and under the chin
    c.poly([(36, 38), (41, 35), (45, 30), (44, 34), (42, 38), (39, 41), (35, 43), (29, 43), (28, 42),
            (34, 41)], "stub_d", clip=["stub_l"])
    c.dither([(33, 37), (40, 33), (44, 29), (44, 32), (41, 36), (36, 39)], "stub_d", clip=["stub_l"])
    # --- hair: short at the sides, full and curling on top, the fringe pushed up
    hair = [(19, 24), (18, 19), (18, 14), (20, 11), (22, 9), (24, 9), (25, 7), (28, 6), (29, 4), (32, 4),
            (33, 3), (36, 3), (38, 4), (40, 4), (42, 6), (44, 8), (45, 11), (47, 14), (46, 19), (45, 23),
            (44, 22), (43, 18), (41, 16), (38, 15), (36, 16), (34, 15), (31, 16), (29, 18), (27, 17),
            (25, 16), (23, 18), (21, 20), (20, 24)]
    c.poly(hair, "hair_d")
    # --- outline
    c.border(["gold"], ["cloth", "cloth_d"], "hair_m")
    c.patch(49, 53, ["W", "W"], {"W": "white"})
    c.patch(57, 53, ["W"], {"W": "white"})
    c.outline("ink")
    c.seam(["hair_d", "hair_m", "hair_l"], ["skin_m", "skin_l", "skin_d"], "ink")
    # curls: little rings, lit on their upper left, dark where they turn under
    curl = [".jH.", "j..H", "H..k", ".kk."]
    for cx, cy in ((27, 5), (32, 4), (37, 5), (22, 9), (29, 8), (34, 8), (40, 8), (25, 12), (31, 12),
                   (37, 12), (43, 12), (20, 15), (28, 15), (44, 16)):
        c.patch(cx - 1, cy - 1, curl, clip=["hair_d"])
    # --- features: thick dark brows, eyes narrowed to crescents by the grin
    c.patch(22, 19, [
        "..hhhhhhh.....hhhhhhh..",
        ".khhhhhhhk...khhhhhhhk.",
        "...kk.............kk...",
        "..kkkkkkk.....kkkkkkk..",
        ".kkhhWhhkk...kkhhWhhkk.",
        ".d.ddddd.d...d.ddddd.d.",
        "..dmSSSmd.....dmmmmdd..",
    ])
    # nose: broad at the tip, a lit left side
    c.patch(28, 22, [
        "....md...",
        "....md...",
        "....Smd..",
        "....Smd..",
        "...mSmd..",
        "...mSSmd.",
        "..mSSSmd.",
        ".dmSSSmdd",
        "dDdmmmdDd",
        ".DkdddkD.",
    ])
    # the big open grin: a row of upper teeth, corners pushed up into the cheeks
    c.patch(24, 31, [
        "dd.............dd",
        ".Dk...........kD.",
        "..kkkkkkkkkkkkk..",
        "..kWWWWWWWWWWWk..",
        "...kWWWWWWWWWk...",
        "....kDDDDDDDk....",
        ".....kdddddk.....",
    ])
    return c, pal


# ==========================================================================
# Cami
# ==========================================================================

CAMI_COLORS = [
    ("k", "ink", (48, 24, 24)),
    ("h", "hair_d", (72, 48, 40)),
    ("H", "hair_m", (120, 80, 64)),
    ("j", "hair_l", (168, 120, 88)),
    ("S", "skin_l", (248, 224, 208)),
    ("m", "skin_m", (240, 192, 168)),
    ("d", "skin_d", (216, 152, 136)),
    ("D", "skin_dd", (176, 104, 96)),
    ("r", "blush", (232, 160, 152)),
    ("W", "white", (248, 248, 240)),
    ("l", "lip", (208, 120, 112)),
    ("g", "shawl", (136, 120, 104)),
    ("G", "shawl_d", (96, 80, 72)),
    ("c", "peplos", (224, 216, 192)),
    ("o", "gold", (224, 176, 64)),
]


def cami():
    pal = palette_of(CAMI_COLORS)
    c = Canvas(pal, legend_of(CAMI_COLORS))
    # --- the shawl over her shoulders, the peplos at the neck
    c.poly([(4, 63), (8, 55), (15, 51), (24, 49), (32, 53), (40, 49), (49, 51), (56, 55), (60, 63)], "shawl")
    c.poly([(26, 51), (38, 51), (35, 59), (29, 59)], "peplos")
    c.poly([(41, 51), (49, 52), (56, 56), (60, 63), (45, 63)], "shawl_d", clip="shawl")
    for x in (10, 17, 23):
        c.line([(x, 56), (x - 2, 63)], "shawl_d", clip="shawl")
    # the ear of wheat caught in the shawl's fringe, ripe out of season:
    # grains up a stalk, awns standing off the top
    c.patch(16, 53, [
        "k.k.k",
        ".kOk.",
        "kOook",
        ".koOk",
        "kOook",
        ".koOk",
        "kOook",
        ".kook",
        "..ok.",
        "..o..",
        "..o..",
        "..o..",
    ], {"o": "gold", "O": "white", "k": "shawl_d"})
    # --- hair behind: the bob's back, falling straight past the jaw
    c.poly([(15, 20), (18, 12), (24, 7), (32, 6), (40, 7), (46, 12), (49, 20), (49, 38), (50, 53),
            (44, 54), (40, 48), (24, 48), (20, 52), (14, 51), (15, 38)], "hair_d")
    # --- neck, between the bob's sides, in the chin's shadow
    c.poly([(27, 42), (37, 42), (37, 51), (32, 54), (27, 51)], "skin_m")
    c.poly([(27, 42), (37, 42), (37, 48), (27, 46)], "skin_d")
    # --- face: slim, soft cheeks lifted by the smile, a narrow chin
    face = [(22, 19), (42, 19), (44, 25), (45, 31), (44, 36), (41, 41), (37, 45), (32, 46), (27, 45),
            (23, 41), (20, 36), (19, 31), (20, 25)]
    c.poly(face, "skin_m")
    c.ellipse((21, 20, 38, 41), "skin_l", clip="skin_m")
    c.poly([(39, 24), (44, 25), (45, 31), (44, 36), (41, 41), (37, 45), (35, 44), (39, 38), (41, 31)],
           "skin_d", clip=["skin_m", "skin_l"])
    # --- the bob's front: wispy bangs to the brows, parted left of centre, the
    # longer side sweeping down over her left brow
    bangs = [(16, 20), (18, 13), (23, 9), (31, 8), (39, 8), (45, 12), (48, 19), (47, 24), (45, 24),
             (43, 25), (41, 24), (39, 25), (37, 24), (35, 24), (33, 22), (31, 18), (30, 18),
             (29, 22), (27, 23), (25, 22), (23, 23), (21, 22), (19, 22)]
    c.poly(bangs, "hair_m")
    # the sides fall straight to below the jaw, framing the cheeks
    c.poly([(15, 20), (21, 21), (21, 30), (22, 38), (24, 44), (23, 50), (15, 50), (14, 38)], "hair_m")
    c.poly([(44, 21), (49, 20), (50, 38), (50, 52), (42, 52), (41, 44), (43, 38), (44, 30)], "hair_m")
    # chestnut where the light falls, darker strands down the far side
    for pts in ([(19, 14), (24, 10), (29, 9), (24, 12), (20, 17)],
                [(17, 22), (19, 22), (19, 40), (17, 46)],
                [(25, 14), (30, 11), (33, 11), (28, 14)],
                [(22, 17), (24, 16), (23, 22), (22, 21)]):
        c.poly(pts, "hair_l", clip="hair_m")
    for pts in ([(40, 11), (45, 14), (47, 22), (43, 19)],
                [(46, 24), (48, 24), (49, 50), (46, 48)],
                [(38, 17), (39, 17), (40, 24), (39, 24)]):
        c.poly(pts, "hair_d", clip="hair_m")
    for pts in ([(33, 12), (36, 11), (35, 14), (34, 20)], [(26, 15), (27, 15), (25, 22), (24, 21)]):
        c.poly(pts, "hair_l", clip="hair_m")
    # --- outline
    c.outline("ink")
    c.seam(["hair_m", "hair_l", "hair_d"], ["skin_m", "skin_l", "skin_d"], "hair_d")
    # --- features: brows under the bangs, eyes narrowed by the smile
    c.patch(22, 24, [
        "..hhhh.........hhhh...",
        "......................",
        "..kkkk.........kkkk...",
        ".kkWhhk.......kWhhkk..",
        "..dmmd.........dmmd...",
        ".rrrr...........rrrr..",
    ])
    # the smile lifts her cheeks: soft creases at the mouth's corners
    c.patch(24, 35, ["d...............d", "d...............d", ".d.............d."])
    # a small straight nose
    c.patch(30, 29, [
        "..m..",
        "..md.",
        "..md.",
        "..Smd",
        ".mSmd",
        ".dDdD",
    ])
    # a warm smile, the upper teeth just showing
    c.patch(26, 38, [
        "D...........D",
        ".lllllllllll.",
        ".lWWWWWWWWWl.",
        "..lWWWWWWWl..",
        "...lllllll...",
        "....ddddd....",
    ])
    return c, pal


PORTRAITS = {"sam": sam, "cami": cami}


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    for name, fn in PORTRAITS.items():
        c, pal = fn()
        if "--write" in args:
            save_indexed(c.a, pal, os.path.join(FRONT, name + ".png"))
        if pv:
            os.makedirs(pv, exist_ok=True)
            im = to_rgba(c.a, pal)
            bg = Image.new("RGBA", im.size, (200, 220, 200, 255))
            bg.alpha_composite(im)
            upscale(bg, 8).save(os.path.join(pv, name + "_x8.png"))
            grid_preview(im, 10).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
