"""Shared pixel-art toolkit for Pokemon Ichor's character sprites.

A sprite is built as a stack of *parts*. Each part is a flat shape (polygon,
ellipse, rect, row spans or an ASCII mask) that carries a material: a short
shading ramp from the sprite's 16-color palette. Rendering then does what a
Gen 3 artist does by hand:

* a 1 px outline on the inside of the silhouette edge (light from top left
  gets a softer outline on the lit side when a material asks for it),
* a 1 px line where a part sits behind a part drawn over it,
* top-left lighting: each part is shaded by where a pixel sits in its own
  horizontal and vertical run, plus cast shadow under anything above it,
* hand-placed detail patches (faces, hands, folds) on top.

Colors must be multiples of 8 so they map exactly to GBA BGR555.
"""
from __future__ import annotations

import os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

TRANSPARENT = (112, 192, 160)  # color 0, never drawn


def check_rgb(c):
    assert len(c) == 3 and all(0 <= v <= 248 and v % 8 == 0 for v in c), c
    return tuple(c)


class Palette:
    """16 named colors; index 0 is transparent."""

    def __init__(self, named, transparent=TRANSPARENT):
        assert len(named) <= 15, f"{len(named)} colors > 15"
        self.names = ["_"] + [n for n, _ in named]
        self.colors = [check_rgb(transparent)] + [check_rgb(c) for _, c in named]
        while len(self.colors) < 16:
            self.colors.append((0, 0, 0))
            self.names.append(f"_pad{len(self.names)}")
        self.index = {n: i for i, n in enumerate(self.names)}

    def __getitem__(self, name):
        return self.index[name]

    def rgb(self, name):
        return self.colors[self.index[name]]

    def flat(self):
        out = []
        for c in self.colors:
            out.extend(c)
        return out

    def write_jasc(self, path):
        with open(path, "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n16\n")
            for c in self.colors:
                f.write("%d %d %d\n" % c)


class Mat:
    """A material: a ramp of palette names, dark -> light.

    line:    color of the line drawn where this part is overlapped
    outline: color of the silhouette edge (default 'ink')
    wx, wy:  how much horizontal / vertical position darkens (0..1)
    """

    def __init__(self, ramp, line=None, outline="ink", wx=0.8, wy=0.25,
                 cuts=None):
        self.ramp = list(ramp)
        self.line = line or outline
        self.outline = outline
        self.wx, self.wy = wx, wy
        self.cuts = cuts


DEFAULT_CUTS = {
    1: [],
    2: [0.58],
    3: [0.22, 0.66],
    4: [0.12, 0.42, 0.74],
    5: [0.1, 0.3, 0.55, 0.8],
}


# --------------------------------------------------------------------------
# Figure
# --------------------------------------------------------------------------

class Part:
    def __init__(self, pid, mat, z, group, bias, noline, nooutline, flat, wx, wy):
        self.pid, self.mat, self.z, self.group = pid, mat, z, group
        self.bias, self.noline, self.nooutline, self.flat = bias, noline, nooutline, flat
        self.wx, self.wy = wx, wy


class Fig:
    def __init__(self, pal: Palette, w=64, h=64):
        self.pal = pal
        self.w, self.h = w, h
        self.pid = np.zeros((h, w), np.int32)
        self.parts = [None]
        self.shade_adj = np.zeros((h, w), float)
        self.post = []  # detail ops applied after render

    # ---- shape helpers -------------------------------------------------
    def _mask_from_draw(self, fn):
        im = Image.new("L", (self.w, self.h), 0)
        fn(ImageDraw.Draw(im))
        return np.array(im) > 0

    def add(self, mask, mat, group=None, under=False, clip=None, bias=0.0,
            noline=False, nooutline=False, flat=None, wx=None, wy=None,
            erase=False):
        mask = mask.copy()
        if erase:
            self.pid[mask] = 0
            return 0
        if under:
            mask &= self.pid == 0
        if clip is not None:
            clip = clip if isinstance(clip, (list, tuple, set)) else [clip]
            mask &= np.isin(self.pid, list(clip))
        pid = len(self.parts)
        part = Part(pid, mat, pid, group if group is not None else pid, bias,
                    noline, nooutline, flat, wx, wy)
        if under:
            part.z = -pid  # sits behind everything already drawn
        self.parts.append(part)
        self.pid[mask] = pid
        return pid

    def poly(self, pts, mat, **kw):
        m = self._mask_from_draw(lambda d: d.polygon([tuple(p) for p in pts], fill=255, outline=255))
        return self.add(m, mat, **kw)

    def ellipse(self, box, mat, **kw):
        m = self._mask_from_draw(lambda d: d.ellipse(box, fill=255, outline=255))
        return self.add(m, mat, **kw)

    def rect(self, x0, y0, x1, y1, mat, **kw):
        m = np.zeros((self.h, self.w), bool)
        m[y0:y1 + 1, x0:x1 + 1] = True
        return self.add(m, mat, **kw)

    def spans(self, y0, spans, mat, **kw):
        """spans: list of (x0, x1) inclusive per row starting at y0;
        None skips a row; a list of pairs gives several runs."""
        m = np.zeros((self.h, self.w), bool)
        for i, s in enumerate(spans):
            if s is None:
                continue
            runs = s if isinstance(s[0], (list, tuple)) else [s]
            for a, b in runs:
                m[y0 + i, a:b + 1] = True
        return self.add(m, mat, **kw)

    def ascii_mask(self, x0, y0, rows, mat, ch="#", **kw):
        m = np.zeros((self.h, self.w), bool)
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                if c in ch:
                    m[y0 + j, x0 + i] = True
        return self.add(m, mat, **kw)

    def thick_line(self, pts, width, mat, **kw):
        m = self._mask_from_draw(lambda d: d.line([tuple(p) for p in pts], fill=255, width=width, joint="curve"))
        return self.add(m, mat, **kw)

    # ---- shading adjustments (before quantizing) -------------------------
    def shade_poly(self, pts, delta):
        m = self._mask_from_draw(lambda d: d.polygon([tuple(p) for p in pts], fill=255, outline=255))
        self.shade_adj[m] += delta

    def shade_px(self, pts, delta):
        for x, y in pts:
            self.shade_adj[y, x] += delta

    # ---- detail ops (after render) ---------------------------------------
    def px(self, x, y, color):
        self.post.append(("px", x, y, color))

    def pxs(self, pts, color):
        for x, y in pts:
            self.px(x, y, color)

    def line(self, pts, color):
        self.post.append(("line", [tuple(p) for p in pts], color))

    def patch(self, x0, y0, rows, legend):
        """ASCII patch; '.' and ' ' leave pixels alone, '0' clears."""
        self.post.append(("patch", x0, y0, rows, legend))

    def erase_px(self, pts):
        for x, y in pts:
            self.post.append(("px", x, y, "_"))

    # ---- rendering -----------------------------------------------------------
    def render(self):
        h, w = self.h, self.w
        pid = self.pid
        out = np.zeros((h, w), np.int32)
        zmap = np.full((h, w), -10 ** 9)
        gmap = np.zeros((h, w), np.int32)
        for p in self.parts[1:]:
            m = pid == p.pid
            zmap[m] = p.z
            gmap[m] = p.group

        # shading value per pixel, by group runs
        s = np.zeros((h, w), float)
        for g in np.unique(gmap[pid > 0]):
            gm = (gmap == g) & (pid > 0)
            part = self.parts[g] if g < len(self.parts) and self.parts[g] is not None else None
            # material of the group's first part sets weights
            members = [p for p in self.parts[1:] if p.group == g]
            base = members[0]
            wx = base.wx if base.wx is not None else base.mat.wx
            wy = base.wy if base.wy is not None else base.mat.wy
            u = np.zeros((h, w))
            v = np.zeros((h, w))
            for y in range(h):
                row = gm[y]
                x = 0
                while x < w:
                    if row[x]:
                        x1 = x
                        while x1 + 1 < w and row[x1 + 1]:
                            x1 += 1
                        n = x1 - x
                        for k in range(x, x1 + 1):
                            u[y, k] = (k - x) / n if n else 0.5
                        x = x1 + 1
                    else:
                        x += 1
            for x in range(w):
                col = gm[:, x]
                y = 0
                while y < h:
                    if col[y]:
                        y1 = y
                        while y1 + 1 < h and col[y1 + 1]:
                            y1 += 1
                        n = y1 - y
                        for k in range(y, y1 + 1):
                            v[k, x] = (k - y) / n if n else 0.5
                        y = y1 + 1
                    else:
                        y += 1
            raw = np.where(gm, (wx * u + wy * v) / max(wx + wy, 1e-6), 0.0)
            # smooth inside the group so shade bands follow the form, not the
            # jaggies of the silhouette (normalized 3x3 box blur, twice)
            wgt = gm.astype(float)
            for _ in range(2):
                num = np.zeros_like(raw)
                den = np.zeros_like(raw)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        num += np.roll(np.roll(raw * wgt, dy, 0), dx, 1)
                        den += np.roll(np.roll(wgt, dy, 0), dx, 1)
                raw = np.where(gm, num / np.maximum(den, 1e-6), 0.0)
            s[gm] = raw[gm]
            for p in members:
                s[pid == p.pid] += p.bias

        # cast shadow from parts drawn over this one, above or to the left
        for y in range(h):
            for x in range(w):
                if pid[y, x] == 0:
                    continue
                z, g = zmap[y, x], gmap[y, x]
                acc = 0.0
                for dx, dy, wgt in ((0, -1, 0.3), (-1, -1, 0.15), (0, -2, 0.15), (-1, 0, 0.12), (-1, -2, 0.08)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and pid[yy, xx] and zmap[yy, xx] > z and gmap[yy, xx] != g:
                        acc += wgt
                s[y, x] += acc
        s += self.shade_adj

        # quantize
        lvl = np.zeros((h, w), np.int32)
        for p in self.parts[1:]:
            m = pid == p.pid
            if not m.any():
                continue
            ramp = p.mat.ramp
            n = len(ramp)
            if p.flat is not None:
                lvl[m] = p.flat
                continue
            cuts = p.mat.cuts or DEFAULT_CUTS[n]
            sv = s[m]
            li = np.full(sv.shape, 0)
            # light index: n-1 for s < cuts[0], ... 0 for s >= cuts[-1]
            idx = np.searchsorted(np.array(cuts), sv, side="right")
            li = (n - 1) - idx
            lvl[m] = np.clip(li, 0, n - 1)

        # despeckle: a lone pixel takes its neighbors' level
        for y in range(h):
            for x in range(w):
                p = pid[y, x]
                if not p:
                    continue
                nb = []
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and gmap[yy, xx] == gmap[y, x] and pid[yy, xx]:
                        nb.append(lvl[yy, xx])
                if len(nb) >= 3 and lvl[y, x] not in nb:
                    vals, counts = np.unique(nb, return_counts=True)
                    lvl[y, x] = vals[np.argmax(counts)]

        for p in self.parts[1:]:
            m = pid == p.pid
            for i, name in enumerate(p.mat.ramp):
                out[m & (lvl == i)] = self.pal[name]

        # lines and outline
        line = out.copy()
        for y in range(h):
            for x in range(w):
                p = pid[y, x]
                if not p:
                    continue
                part = self.parts[p]
                edge_out = False
                edge_in = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < w and 0 <= yy < h) or pid[yy, xx] == 0:
                        edge_out = True
                    elif gmap[yy, xx] != gmap[y, x] and zmap[yy, xx] < zmap[y, x]:
                        # this part sits in front of its neighbour: outline it
                        edge_in = True
                if edge_out and not part.nooutline:
                    line[y, x] = self.pal[part.mat.outline]
                elif edge_in and not part.noline:
                    line[y, x] = self.pal[part.mat.line]
        out = line

        # detail ops
        for op in self.post:
            if op[0] == "px":
                _, x, y, c = op
                if 0 <= x < w and 0 <= y < h:
                    out[y, x] = 0 if c == "_" else self.pal[c]
            elif op[0] == "line":
                _, pts, c = op
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    for x, y in bresenham(x0, y0, x1, y1):
                        if 0 <= x < w and 0 <= y < h:
                            out[y, x] = self.pal[c]
            elif op[0] == "patch":
                _, x0, y0, rows, legend = op
                for j, row in enumerate(rows):
                    for i, ch in enumerate(row):
                        if ch in ". ":
                            continue
                        x, y = x0 + i, y0 + j
                        if 0 <= x < w and 0 <= y < h:
                            c = legend[ch]
                            out[y, x] = 0 if c == "_" else self.pal[c]
        return out


def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return pts


# --------------------------------------------------------------------------
# Index-map helpers (for hand-drawn overworld frames and sheet assembly)
# --------------------------------------------------------------------------

def from_ascii(rows, legend, pal, w=None, h=None):
    h = h or len(rows)
    w = w or max(len(r) for r in rows)
    a = np.zeros((h, w), np.int32)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            a[j, i] = pal[legend[ch]]
    return a


def hflip(a):
    return a[:, ::-1].copy()


def save_indexed(arr, pal: Palette, path):
    from human_classes import ASSETS

    relative = os.path.relpath(os.path.realpath(path), os.path.realpath(ROOT)).replace(os.sep, "/")
    if any(entry["target"] == relative for entry in ASSETS):
        raise ValueError(
            f"Legacy painter cannot overwrite image-led art: {relative}; "
            "use python3 tools/ichor/art/human_classes.py --write"
        )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im = Image.fromarray(arr.astype(np.uint8), "P")
    im.putpalette(pal.flat())
    im.info["transparency"] = 0
    im.save(path, bits=4, transparency=0)


def to_rgba(arr, pal: Palette):
    h, w = arr.shape
    rgba = np.zeros((h, w, 4), np.uint8)
    for i, c in enumerate(pal.colors):
        m = arr == i
        rgba[m, :3] = c
        rgba[m, 3] = 0 if i == 0 else 255
    return Image.fromarray(rgba, "RGBA")


def palette_report(arr, pal: Palette, label=""):
    used = sorted(set(np.unique(arr)) - {0})
    unused = [pal.names[i] for i in range(1, 16) if i not in used and not pal.names[i].startswith("_pad")]
    if unused:
        print(f"  {label}: unused colors {unused}")
    return used


# --------------------------------------------------------------------------
# Preview backgrounds
# --------------------------------------------------------------------------

def battle_bg(w=240, h=112):
    """A Gen 3-ish battle backdrop: sky band, grass field and an oval platform."""
    im = Image.new("RGBA", (w, h), (248, 248, 240, 255))
    d = ImageDraw.Draw(im)
    sky = [(176, 216, 240), (200, 224, 240), (216, 232, 240)]
    for i, c in enumerate(sky):
        d.rectangle([0, i * 14, w, i * 14 + 14], fill=c + (255,))
    d.rectangle([0, 42, w, h], fill=(168, 200, 120, 255))
    d.rectangle([0, 42, w, 46], fill=(144, 176, 96, 255))
    for x in range(0, w, 6):
        d.point((x + (x // 6) % 3, 50 + (x * 7) % 9), fill=(136, 168, 88, 255))
    d.ellipse([w - 128, 78, w - 8, 106], fill=(200, 216, 144, 255), outline=(144, 168, 96, 255))
    d.ellipse([w - 112, 82, w - 24, 102], fill=(216, 224, 160, 255))
    return im


def upscale(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def grid_preview(im, k=10, x0=0, y0=0, x1=None, y1=None):
    """Upscaled crop with a pixel grid and coordinate labels, for placing details."""
    x1 = x1 or im.width
    y1 = y1 or im.height
    crop = im.crop((x0, y0, x1, y1))
    bg = Image.new("RGBA", crop.size, (200, 220, 200, 255))
    bg.alpha_composite(crop)
    big = bg.resize((crop.width * k, crop.height * k), Image.NEAREST)
    pad = 18
    out = Image.new("RGBA", (big.width + pad, big.height + pad), (255, 255, 255, 255))
    out.paste(big, (pad, pad))
    d = ImageDraw.Draw(out)
    for i in range(crop.width + 1):
        x = pad + i * k
        col = (0, 0, 0, 255) if (x0 + i) % 8 == 0 else (150, 150, 150, 255)
        d.line([(x, pad), (x, out.height)], fill=col)
        if i < crop.width and (x0 + i) % 2 == 0:
            d.text((x + 1, 2), str((x0 + i) % 100), fill=(0, 0, 0, 255))
    for j in range(crop.height + 1):
        y = pad + j * k
        col = (0, 0, 0, 255) if (y0 + j) % 8 == 0 else (150, 150, 150, 255)
        d.line([(pad, y), (out.width, y)], fill=col)
        if j < crop.height and (y0 + j) % 2 == 0:
            d.text((1, y + 1), str(y0 + j), fill=(0, 0, 0, 255))
    return out
