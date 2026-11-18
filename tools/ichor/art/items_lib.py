"""Small pixel-art toolkit for Ichor's 24x24 item icons and the ground jar.

An icon is an index map (0 = transparent) over a list of *roles*: short names
such as "K" (outline) or "c2" (clay, mid). A role list fixes the palette
order, so an icon pic shared by several items (Potion, Super Potion, Hyper
Potion) is drawn once and recolored by one palette per item, exactly as the
game does it.

Drawing is shape-first, then hand detail, the way a Gen 3 artist works:
  * fill shapes (ellipses, polygons, rects) with a material ramp, shaded by a
    light from the top left (sphere or cylinder shading),
  * outline the silhouette 1 px inside its edge,
  * finish with ASCII patches: highlights, motifs, seals and knots.

Colors are RGB multiples of 8, so they map exactly to GBA BGR555.
"""
from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
W = H = 24
TRANSPARENT = (112, 192, 160)  # color 0, never drawn

# --------------------------------------------------------------------------
# The master palette (design/phase1/PLAN.md), plus the few extra hues the
# icons need to stay readable for what they do (status colors, fruit, wax).
# --------------------------------------------------------------------------
C = dict(
    ink=(32, 24, 24),
    # Aegean blue
    ae_d=(24, 56, 120), ae_m=(48, 104, 176), ae_l=(112, 168, 224), ae_p=(176, 216, 240),
    # marble
    mb_d=(168, 160, 152), mb_m=(216, 208, 192), mb_l=(248, 248, 240),
    # olive and cypress
    ol_d=(56, 72, 32), ol_m=(96, 112, 48), ol_l=(144, 160, 72), ol_s=(168, 184, 136),
    cy_d=(24, 56, 40), cy_m=(40, 88, 56),
    # terracotta
    tc_d=(120, 48, 24), tc_m=(184, 88, 48), tc_l=(224, 136, 88), tc_p=(240, 176, 128),
    # sun-gold and bronze
    sg_d=(200, 144, 40), sg_l=(240, 192, 64), sg_p=(248, 224, 136),
    br_d=(104, 64, 32), br_m=(152, 96, 40),
    # limestone / parchment / linen
    lp_d=(176, 144, 96), lp_m=(208, 184, 136), lp_l=(232, 216, 176),
    ln_l=(248, 240, 216),
    # wood and charcoal
    wd_d=(72, 40, 24), wd_m=(120, 72, 40), wd_l=(168, 112, 64),
    ch_d=(48, 40, 40), ch_m=(80, 72, 72), ch_l=(120, 112, 112),
)


def rgb(c):
    c = C[c] if isinstance(c, str) else tuple(c)
    assert len(c) == 3 and all(0 <= v <= 248 and v % 8 == 0 for v in c), c
    return c


def mix(a, b, t):
    """a..b at t, snapped to multiples of 8."""
    a, b = rgb(a), rgb(b)
    return tuple(int(round((a[i] + (b[i] - a[i]) * t) / 8)) * 8 for i in range(3))


def ramp4(base):
    """dark, mid, light, highlight from one mid color."""
    b = rgb(base)
    return [mix(b, (0, 0, 0), 0.42), b, mix(b, (248, 248, 248), 0.38), mix(b, (248, 248, 248), 0.7)]


# --------------------------------------------------------------------------
# Icon canvas
# --------------------------------------------------------------------------

class Icon:
    def __init__(self, roles, w=W, h=H):
        roles = roles.split() if isinstance(roles, str) else list(roles)
        assert len(roles) <= 15, roles
        assert len(set(roles)) == len(roles), roles
        self.roles = roles
        self.idx = {r: i + 1 for i, r in enumerate(roles)}
        self.w, self.h = w, h
        self.a = np.zeros((h, w), np.int32)

    # ---- masks -----------------------------------------------------------
    def ellipse(self, cx, cy, rx, ry):
        y, x = np.mgrid[0:self.h, 0:self.w]
        return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0

    def rect(self, x0, y0, x1, y1):
        m = np.zeros((self.h, self.w), bool)
        m[max(y0, 0):y1 + 1, max(x0, 0):x1 + 1] = True
        return m

    def poly(self, pts):
        from PIL import ImageDraw
        im = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=255, outline=255)
        return np.array(im) > 0

    def spans(self, y0, spans):
        m = np.zeros((self.h, self.w), bool)
        for i, s in enumerate(spans):
            if s is None:
                continue
            runs = s if isinstance(s[0], (list, tuple)) else [s]
            for a, b in runs:
                m[y0 + i, a:b + 1] = True
        return m

    def ascii_mask(self, x0, y0, rows, ch="#"):
        m = np.zeros((self.h, self.w), bool)
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                if c in ch:
                    m[y0 + j, x0 + i] = True
        return m

    # ---- fills -------------------------------------------------------------
    def fill(self, mask, role):
        self.a[mask] = self.idx[role]

    def shade(self, mask, ramp, kind="sphere", light=(-0.75, -0.65), cuts=None,
              center=None, radius=None, bias=0.0):
        """Fill mask with ramp (dark -> light), lit from the top left.
        kind: 'sphere' (both axes), 'cyl' (x only), 'flat' (y only)."""
        ys, xs = np.nonzero(mask)
        if not len(xs):
            return
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        cx = center[0] if center else (x0 + x1) / 2
        cy = center[1] if center else (y0 + y1) / 2
        rx = radius[0] if radius else max((x1 - x0) / 2, 0.5)
        ry = radius[1] if radius else max((y1 - y0) / 2, 0.5)
        # a 3D light from the top left and in front of the picture plane
        lx, ly = light
        lz = 0.9
        ln = math.sqrt(lx * lx + ly * ly + lz * lz)
        lx, ly, lz = lx / ln, ly / ln, lz / ln
        n = len(ramp)
        cuts = cuts or {2: [0.45], 3: [0.3, 0.7], 4: [0.25, 0.62, 0.9], 5: [0.1, 0.35, 0.65, 0.9]}[n]
        for x, y in zip(xs, ys):
            nx = (x + 0.5 - cx) / rx
            ny = (y + 0.5 - cy) / ry
            if kind == "cyl":
                ny = 0.0
            elif kind == "flat":
                nx = 0.0
            r2 = nx * nx + ny * ny
            if r2 > 1:
                nx, ny, r2 = nx / math.sqrt(r2), ny / math.sqrt(r2), 1.0
            nz = math.sqrt(1 - r2)
            # brightness: a normal facing the light is high
            b = (nx * lx + ny * ly + nz * lz) + bias
            lvl = sum(1 for c in cuts if b > c)
            self.a[y, x] = self.idx[ramp[min(lvl, n - 1)]]

    def tube(self, p0, p1, r, ramp=None, light=(-0.75, -0.65), cuts=None, caps=False):
        """A cylinder from p0 to p1 of radius r, shaded across its width.
        Returns its mask; fills it when ramp is given."""
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        ux, uy = dx / ln, dy / ln
        nx, ny = -uy, ux
        y, x = np.mgrid[0:self.h, 0:self.w]
        px, py = x + 0.5 - x0, y + 0.5 - y0
        t = (px * ux + py * uy) / ln
        s = (px * nx + py * ny) / r
        lo, hi = (-r / ln, 1 + r / ln) if caps else (0.0, 1.0)
        mask = (t >= lo) & (t <= hi) & (np.abs(s) <= 1.0)
        if caps:
            mask |= ((x + 0.5 - x0) ** 2 + (y + 0.5 - y0) ** 2 <= r * r)
            mask |= ((x + 0.5 - x1) ** 2 + (y + 0.5 - y1) ** 2 <= r * r)
        if ramp:
            n = len(ramp)
            cuts = cuts or {2: [0.45], 3: [0.3, 0.7], 4: [0.25, 0.62, 0.9], 5: [0.1, 0.35, 0.65, 0.9]}[n]
            lx, ly, lz = light[0], light[1], 0.9
            ll = math.sqrt(lx * lx + ly * ly + lz * lz)
            sc = np.clip(s, -1, 1)
            b = (sc * (nx * lx + ny * ly) + np.sqrt(1 - sc * sc) * lz) / ll
            for yy, xx in zip(*np.nonzero(mask)):
                lvl = sum(1 for c in cuts if b[yy, xx] > c)
                self.a[yy, xx] = self.idx[ramp[min(lvl, n - 1)]]
        return mask

    def tube_coords(self, p0, p1):
        """(t, s, length): position along p0->p1 (0..1) and signed distance
        across it (px; negative is the top-left side for an up-right axis)."""
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        ux, uy = dx / ln, dy / ln
        nx, ny = -uy, ux
        y, x = np.mgrid[0:self.h, 0:self.w]
        px, py = x + 0.5 - x0, y + 0.5 - y0
        return (px * ux + py * uy) / ln, px * nx + py * ny, ln

    def ellipse_rot(self, cx, cy, a, b, angle):
        """Ellipse with semi-axis a along angle (radians) and b across it."""
        y, x = np.mgrid[0:self.h, 0:self.w]
        px, py = x + 0.5 - cx, y + 0.5 - cy
        ca, sa = math.cos(angle), math.sin(angle)
        u = px * ca + py * sa
        v = -px * sa + py * ca
        return (u / a) ** 2 + (v / b) ** 2 <= 1.0

    def leaf(self, base, tip, width, ramp, rib=None, light=(-0.75, -0.65)):
        """A lens-shaped leaf from base to tip. ramp: (shade, lit) halves.
        rib: midrib role. Returns the mask."""
        (x0, y0), (x1, y1) = base, tip
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        mx, my = x0 + dx * 0.42, y0 + dy * 0.42
        a = (mx + nx * width, my + ny * width)
        b = (mx - nx * width, my - ny * width)
        side_a = self.poly([(x0, y0), a, (x1, y1)])
        side_b = self.poly([(x0, y0), b, (x1, y1)])
        lit_a = (nx * light[0] + ny * light[1]) > 0
        self.fill(side_a, ramp[1] if lit_a else ramp[0])
        self.fill(side_b & ~side_a, ramp[0] if lit_a else ramp[1])
        if rib:
            self.line(int(round(x0)), int(round(y0)), int(round(x0 + dx * 0.8)), int(round(y0 + dy * 0.8)), rib)
        return side_a | side_b

    def outline(self, mask, role="K", inner=True):
        """Outline the silhouette of mask, 1 px inside its edge."""
        m = mask
        edge = np.zeros_like(m)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.zeros_like(m)
            ys = slice(max(dy, 0), self.h + min(dy, 0))
            yd = slice(max(-dy, 0), self.h + min(-dy, 0))
            xs = slice(max(dx, 0), self.w + min(dx, 0))
            xd = slice(max(-dx, 0), self.w + min(-dx, 0))
            sh[yd, xd] = m[ys, xs]
            edge |= m & ~sh
        # pixels on the canvas border count as edge too
        edge[0, :] |= m[0, :]
        edge[-1, :] |= m[-1, :]
        edge[:, 0] |= m[:, 0]
        edge[:, -1] |= m[:, -1]
        self.a[edge] = self.idx[role]
        return edge

    def silhouette(self):
        return self.a > 0

    # ---- detail ------------------------------------------------------------
    def px(self, x, y, role):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = 0 if role == "_" else self.idx[role]

    def pxs(self, pts, role):
        for x, y in pts:
            self.px(x, y, role)

    def line(self, x0, y0, x1, y1, role):
        for x, y in bresenham(x0, y0, x1, y1):
            self.px(x, y, role)

    def patch(self, x0, y0, rows, legend):
        """ASCII patch. '.' and ' ' keep the pixel; '_' clears it."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in ". ":
                    continue
                self.px(x0 + i, y0 + j, legend[ch] if ch in legend else ch)

    def art(self, rows, legend):
        """Whole-canvas ASCII art (rows must be w wide)."""
        assert len(rows) == self.h, (len(rows), self.h)
        for j, row in enumerate(rows):
            assert len(row) == self.w, (j, len(row), row)
        self.a[:] = 0
        self.patch(0, 0, rows, legend)

    def recolor(self, mask, mapping):
        """Swap roles inside mask: {from_role: to_role}."""
        for a, b in mapping.items():
            sel = mask & (self.a == self.idx[a])
            self.a[sel] = self.idx[b]

    def used_roles(self):
        inv = {v: k for k, v in self.idx.items()}
        return sorted({inv[v] for v in np.unique(self.a) if v})


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
# Palettes and files
# --------------------------------------------------------------------------

def palette_colors(roles, colors):
    """16 colors: transparent, then each role's color, padded with black."""
    out = [TRANSPARENT]
    for r in roles:
        out.append(rgb(colors[r]))
    while len(out) < 16:
        out.append((0, 0, 0))
    return out


def write_jasc(path, colors):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in colors:
            f.write("%d %d %d\n" % tuple(c))


def read_jasc(path):
    vals = open(path).read().split()[3:]
    return [tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(16)]


def centre_offset(arr):
    """How far the opaque bounding box's centre sits from the frame's centre,
    in pixels (dx, dy); positive is right and down."""
    ys, xs = np.nonzero(arr)
    h, w = arr.shape
    return (xs.min() + xs.max() + 1) / 2 - w / 2, (ys.min() + ys.max() + 1) / 2 - h / 2


def centred(arr):
    """The icon moved whole pixels so its opaque bounding box is centred in
    the frame to within half a pixel. The bag and shop show every icon in the
    same square plate, so a pic drawn low or to one side looks off-centre
    there, however it was meant to sit."""
    dx, dy = centre_offset(arr)
    sx, sy = -int(dx), -int(dy)          # toward zero: what is left is <= 0.5
    if sx == 0 and sy == 0:
        return arr
    ys, xs = np.nonzero(arr)
    h, w = arr.shape
    assert 0 <= xs.min() + sx and xs.max() + sx < w and 0 <= ys.min() + sy and ys.max() + sy < h
    out = np.zeros_like(arr)
    out[ys + sy, xs + sx] = arr[ys, xs]
    return out


def save_indexed(arr, colors, path):
    im = Image.fromarray(arr.astype(np.uint8), "P")
    flat = [v for c in colors for v in c]
    im.putpalette(flat)
    im.save(path, bits=4, transparency=0)


def to_rgb(arr, colors, bg=None):
    out = np.zeros(arr.shape + (4,), np.uint8)
    for i in range(1, 16):
        out[arr == i, :3] = colors[i]
        out[arr == i, 3] = 255
    if bg is not None:
        base = np.zeros_like(out)
        base[..., :3] = bg
        base[..., 3] = 255
        a = out[..., 3:4] / 255.0
        base[..., :3] = (out[..., :3] * a + base[..., :3] * (1 - a)).astype(np.uint8)
        return base
    return out


def upscale(img, k):
    return np.repeat(np.repeat(img, k, 0), k, 1)
