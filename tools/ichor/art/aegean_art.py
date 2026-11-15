#!/usr/bin/env python3
"""The Aegean islands' furnishings: the pieces Kythera's and Melos's homes need
that gTileset_Oikia doesn't have (design/phase4/ROOMS_aegean.md).

The pieces are drawn in oikia's style and palettes (oikia_art.py): character
grids, one character per color, '.' clear, a 1 px ink outline, light from the
top left. cloth, the one palette with free slots, takes three roses (the
perfumer's petals, Paphia's flowers); every other palette is full (15 colors),
so a piece that needs a color its palette lacks keeps that color to its own 8x8
tiles in another palette (the golden apple is drawn in wood's bronze among
olive leaves; the obsidian mirror in clay's soot and stone). These are region
secondaries (interiors_lib.py), compiled against an empty primary, so the new
colors needn't avoid aethos's.

This module holds the palettes, a small canvas for pieces drawn partly in code,
the new floor (grass, for the yards), and STAMPS, the registry. The pieces
themselves are in aegean_skandeia.py, aegean_paphia.py and aegean_melos.py
(the halls' pieces, in civic's style, are in aegean_civic.py); load() imports
them all.
"""
import numpy as np

import oikia_art as A

PALETTES = {k: dict(v) for k, v in A.PALETTES.items()}
PALETTES["cloth"].update({
    "p": (216, 96, 120),   # rose
    "P": (248, 168, 176),  # rose, light
    "e": (152, 48, 72),    # rose, dark
})
for _n, _p in PALETTES.items():
    assert len(_p) <= 15, f"{_n} has {len(_p)} colors"

STAMPS = {}


def grid(pal, text, w=None, h=None):
    """A character grid in one of PALETTES, as (h, w, 4) RGBA ('.' clear)."""
    rows = [r.rstrip() for r in text.strip("\n").split("\n")]
    w = w or max(len(r) for r in rows)
    h = h or len(rows)
    assert len(rows) <= h, f"{len(rows)} rows > {h}"
    out = np.zeros((h, w, 4), np.uint8)
    colors = PALETTES[pal]
    for y, row in enumerate(rows):
        assert len(row) <= w, f"row {y} is {len(row)} wide > {w}: {row!r}"
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in colors:
                raise ValueError(f"{pal}: unknown char {ch!r} at ({x},{y}) in {row!r}")
            out[y, x, :3] = colors[ch]
            out[y, x, 3] = 255
    return out


def stamp(name, pal, art, w, h, top=None, walk=(), behavior=None, flatten=False, note="",
          top_pal=None):
    """As oikia_art.stamp: w, h in metatiles; walk lists the cells (cx, cy) the
    player may stand on; top art is drawn over the player. art and top may be
    text or a Canvas."""
    assert name not in STAMPS and name not in A.STAMPS, f"duplicate stamp {name}"
    if isinstance(art, Canvas):
        art = art.text()
    if isinstance(top, Canvas):
        top = top.text()
    STAMPS[name] = {
        "pal": pal,
        "img": grid(pal, art, w * 16, h * 16),
        "top": grid(top_pal or pal, top, w * 16, h * 16) if top else None,
        "w": w,
        "h": h,
        "walk": set(walk),
        "behavior": dict(behavior or {}),
        "flatten": flatten,
        "note": note,
    }
    return STAMPS[name]


def variant(name, base, img=None, note=None, **kw):
    """A copy of a stamp (oikia's or ours) with new art or attributes."""
    src = STAMPS[base] if base in STAMPS else A.STAMPS[base]
    assert name not in STAMPS and name not in A.STAMPS, f"duplicate stamp {name}"
    STAMPS[name] = dict(src, img=src["img"] if img is None else img,
                        note=src["note"] if note is None else note, **kw)
    return STAMPS[name]


def recolor(img, pal, mapping):
    colors = PALETTES[pal]
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == colors[a]).all(-1) & (img[..., 3] > 0)
        out[m, :3] = colors[b]
    return out


def hflip(img):
    return img[:, ::-1].copy()


class Canvas:
    """A character grid to draw on in code; text() feeds grid()."""

    def __init__(self, w, h, text=None):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]
        if text:
            self.paste(text, 0, 0)

    def px(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h and ch != ".":
            self.g[y][x] = ch

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, ch)

    def hline(self, x0, x1, y, ch):
        self.rect(x0, y, x1, y, ch)

    def vline(self, x, y0, y1, ch):
        self.rect(x, y0, x, y1, ch)

    def line(self, x0, y0, x1, y1, ch):
        n = int(round(max(abs(x1 - x0), abs(y1 - y0), 1)))
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), ch)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, shade=None):
        """A filled ellipse; shade(x, y, nx, ny) may pick each pixel's color from
        its normalized offset (nx, ny) from the center."""
        inside = set()
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                nx, ny = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if nx * nx + ny * ny <= 1.0:
                    inside.add((x, y))
        for (x, y) in inside:
            nx, ny = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            c = shade(x, y, nx, ny) if shade else fill
            if c:
                self.px(x, y, c)
        if outline:
            for (x, y) in inside:
                if any((x + dx, y + dy) not in inside for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.px(x, y, outline)
        return inside

    def paste(self, text, x0, y0, skip="."):
        rows = text.strip("\n").split("\n") if isinstance(text, str) else text
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in skip and ch != " ":
                    self.px(x0 + i, y0 + j, ch)

    def outline(self, ink="k"):
        """Ink every clear pixel that touches a drawn one (4-neighbors)."""
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] != ".":
                    continue
                if any(self.get(x + dx, y + dy) not in (".", ink)
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for x, y in add:
            self.g[y][x] = ink

    def replace(self, mapping, x0=0, y0=0, x1=None, y1=None):
        x1 = self.w - 1 if x1 is None else x1
        y1 = self.h - 1 if y1 is None else y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.g[y][x] = mapping.get(self.g[y][x], self.g[y][x])

    def flip(self):
        self.g = [r[::-1] for r in self.g]
        return self

    def text(self):
        return "\n".join("".join(r) for r in self.g)


# --------------------------------------------------------------------------
# Floors. Grass for the yards (Pygmalion's, the orchard's), in the nature
# palette, with oikia's shadow variants. The composer takes a room's second
# floor from its grid's ',' cells (interiors_lib.OikiaKit.compose).
# --------------------------------------------------------------------------

_GRASS_SHADE = {"V": "v", "v": "g", "g": "G", "w": "V", "p": "G"}


def _grass(seed, flowers=False):
    """Sunny yard grass: a light ground with small tufts, each a lit blade
    over a shaded root, scattered so the tile repeats softly."""
    rnd = np.random.RandomState(seed)
    c = Canvas(16, 16)
    c.rect(0, 0, 15, 15, "v")
    spots = [(2, 3), (9, 1), (13, 6), (5, 9), (11, 12), (1, 13), (7, 14), (14, 15)]
    for (x, y) in spots:
        x = (x + rnd.randint(0, 2)) % 16
        c.px(x, y, "V")
        c.px(x - 1, (y + 1) % 16, "g")
        c.px(x + 1, (y + 1) % 16, "g")
        c.px(x, (y + 1) % 16, "V" if rnd.randint(0, 2) else "v")
    for (x, y) in [(6, 4), (12, 9), (3, 11)]:
        c.px(x, y, "g")
    if flowers:
        for (x, y, ch) in [(4, 5, "w"), (11, 3, "w"), (8, 11, "p"), (13, 13, "w")]:
            c.px(x, y, ch)
            c.px(x, y + 1, "g")
    return grid("nature", c.text())


def grass_variants():
    yy, xx = np.mgrid[0:16, 0:16]
    top = (yy < 4) | ((yy == 4) & (xx % 2 == 0))
    left = (xx < 3) | ((xx == 3) & (yy % 2 == 0))
    base, alt = _grass(1), _grass(2, flowers=True)

    def sh(img, mask):
        dark = recolor(img, "nature", _GRASS_SHADE)
        out = img.copy()
        out[mask] = dark[mask]
        return out
    return {"plain": base, "alt": alt, "top": sh(base, top), "left": sh(base, left),
            "corner": sh(base, top | left)}


FLOORS = {"grass": grass_variants()}


def load():
    """Import every town's pieces (they register into STAMPS)."""
    import aegean_skandeia  # noqa: F401
    import aegean_paphia  # noqa: F401
    import aegean_melos  # noqa: F401
    return STAMPS
