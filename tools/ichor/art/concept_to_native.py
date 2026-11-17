#!/usr/bin/env python3
"""Turn an image-model concept into a native Gen 3 sprite draft (design/STYLE.md §3).

The output is a *draft*, not finished art: it gets the silhouette, proportions,
palette and outline onto the real pixel grid so the hand-fix pass (§3.5) can
start from something close. Steps:

  1. key the background by flood fill from the border, so interior colors that
     match the backdrop (cream muzzles, eye whites) stay opaque;
  2. sample cell centres (median) at the pitch that fits the target height,
     instead of nearest-neighbour resizing the whole illustration;
  3. quantize the opaque pixels to at most 15 GBA colors (multiples of 8);
  4. clean up: strip blur halos, remove orphan pixels and specks;
  5. close a selective outline: ink on the shadow side (bottom/right),
     the darker shade of the local ramp on the lit side (top/left).

A true-grid concept (--pitch) that already uses 15 colors or fewer is clean
pixel art: steps 3-5 are skipped and its colors and outline are kept exactly.

Usage:
  python3 tools/ichor/art/concept_to_native.py CONCEPT.png OUT.png \
      [--size 64] [--fit 60] [--colors 15] [--bg R,G,B]

--size is the canvas (64 for battle fronts and trainer fronts); --fit is the
subject's largest dimension in native pixels (leave 2-4 px of air); --bg names
the concept's backdrop when its corners are not representative.
"""
import argparse
from collections import deque

import numpy as np
from PIL import Image

NEIGHBORS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def lum(c):
    c = np.asarray(c, float)
    return 0.3 * c[..., 0] + 0.59 * c[..., 1] + 0.11 * c[..., 2]


def border_color(a):
    edges = [a[:3], a[-3:], a[:, :3], a[:, -3:]]
    return np.median(np.concatenate([e.reshape(-1, 3) for e in edges]), axis=0)


def trim(a, bg, tol):
    mask = np.abs(a - bg).sum(-1) > tol
    ys, xs = np.where(mask)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def sample(a, pitch):
    """Median of each cell's central third: robust to soft model edges."""
    h, w = a.shape[:2]
    rows, cols = int(h / pitch + 0.5), int(w / pitch + 0.5)
    r = max(1, int(pitch * 0.3))
    out = np.zeros((rows, cols, 3), int)
    for j in range(rows):
        cy = min(h - 1, int((j + 0.5) * pitch))
        for i in range(cols):
            cx = min(w - 1, int((i + 0.5) * pitch))
            blk = a[max(0, cy - r):cy + r + 1, max(0, cx - r):cx + r + 1]
            out[j, i] = np.median(blk.reshape(-1, 3), axis=0)
    return out


def flood_alpha(nat, bg, tol):
    h, w = nat.shape[:2]
    near = np.abs(nat - bg).sum(-1) <= tol
    outside = np.zeros((h, w), bool)
    q = deque((y, x) for y in range(h) for x in range(w)
              if (y in (0, h - 1) or x in (0, w - 1)) and near[y, x])
    for y, x in q:
        outside[y, x] = True
    while q:
        y, x = q.popleft()
        for dy, dx in NEIGHBORS:
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and near[yy, xx] and not outside[yy, xx]:
                outside[yy, xx] = True
                q.append((yy, xx))
    return ~outside


def detail_palette(px, k):
    """k-means for the body colors, plus reserved slots for the extremes.

    Eye shines, teeth and pupils are a handful of pixels; plain k-means merges
    them into the nearest big cluster and the face goes dead. Reserve the
    lightest and darkest few pixels' colors first.
    """
    L = lum(px)
    keep = []
    for sel in (L >= np.percentile(L, 99.6), L <= np.percentile(L, 0.6)):
        if sel.sum() >= 2:
            keep.append(np.round(px[sel].mean(0) / 8) * 8)
    keep += accents(px, k - len(keep))
    body = kmeans(px, k - len(keep))
    pal = np.vstack([body] + [np.asarray(keep).clip(0, 248)] if keep else [body]).astype(int)
    return np.unique(pal, axis=0)


def magentaness(c):
    """How far a color leans magenta: min(R, B) - G. The backdrop is ~240."""
    c = np.asarray(c, float)
    return np.minimum(c[..., 0], c[..., 2]) - c[..., 1]


def chroma_key(nat, alpha, key=90, spill=25):
    """Key a magenta backdrop everywhere, not just from the border.

    Magenta never appears in a subject (STYLE.md §3.2), so enclosed gaps (a
    lyre's strings, the space between legs) are backdrop too. Edge pixels
    that JPEG or anti-aliasing blended with magenta take the median of their
    clean neighbors, so no purple fringe survives into the palette.
    """
    m = magentaness(nat)
    alpha = alpha & (m < key)
    nat = nat.copy()
    h, w = m.shape
    clean = alpha & (m < spill)
    for y, x in zip(*np.where(alpha & (m >= spill))):
        y0, y1, x0, x1 = max(0, y - 1), min(h, y + 2), max(0, x - 1), min(w, x + 2)
        nb = nat[y0:y1, x0:x1][clean[y0:y1, x0:x1]]
        if len(nb):
            nat[y, x] = np.median(nb, axis=0)
        else:
            g = nat[y, x, 1]
            nat[y, x] = (g, g, g)
    return alpha, nat


def accents(px, k, most=2):
    """Small, saturated color accents a body palette would swallow.

    Eyes, flames, sparks and lantern glow are a few pixels of a hue the big
    clusters don't have. Reserve up to `most` of them: a hue bin covering
    0.15-4% of the subject whose hue is 35+ degrees from every body color.
    """
    import colorsys
    hsv = np.array([colorsys.rgb_to_hsv(*(c / 255.0)) for c in px])
    sat = (hsv[:, 1] > 0.45) & (hsv[:, 2] > 0.35)
    if sat.sum() < 3:
        return []
    body = kmeans(px, k).astype(float)
    bins = (hsv[:, 0] * 12).astype(int) % 12
    found = []
    for b in range(12):
        sel = sat & (bins == b)
        share = sel.sum() / len(px)
        if not (0.0015 <= share <= 0.04):
            continue
        col = px[sel].mean(0)
        # only when the full palette would still miss it by a visible margin
        if np.sqrt(((body - col) ** 2).sum(-1)).min() < 70:
            continue
        found.append((share, np.round(col / 8) * 8))
    found.sort(key=lambda t: -t[0])
    return [c for _, c in found[:most]]


def kmeans(px, k, seed=3, iters=30):
    k = min(k, len(np.unique(px, axis=0)))
    rng = np.random.default_rng(seed)
    cent = px[rng.choice(len(px), k, replace=False)].astype(float)
    for _ in range(iters):
        lab = ((px[:, None] - cent[None]) ** 2).sum(-1).argmin(1)
        for c in range(k):
            m = px[lab == c]
            if len(m):
                cent[c] = m.mean(0)
    return (np.round(cent / 8) * 8).clip(0, 248).astype(int)


def cleanup(idx, alpha, pal):
    h, w = idx.shape
    L = lum(pal)

    def outside(y, x):
        return not (0 <= y < h and 0 <= x < w) or not alpha[y, x]

    for _ in range(2):  # blur halo: light pixels hanging on the silhouette
        keep = alpha.copy()
        for y in range(h):
            for x in range(w):
                if not alpha[y, x]:
                    continue
                nb = [(y + dy, x + dx) for dy, dx in NEIGHBORS]
                out = sum(outside(yy, xx) for yy, xx in nb)
                ins = [L[idx[yy, xx]] for yy, xx in nb if not outside(yy, xx)]
                if out >= 2 and ins and L[idx[y, x]] > np.mean(ins) + 40:
                    keep[y, x] = False
        alpha = keep
    for _ in range(2):  # orphans and specks
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if not alpha[y, x]:
                    continue
                if alpha[y - 1:y + 2, x - 1:x + 2].sum() - 1 <= 1:
                    alpha[y, x] = False
                    continue
                n = {idx[y - 1, x], idx[y + 1, x], idx[y, x - 1], idx[y, x + 1]}
                if alpha[y - 1:y + 2, x - 1:x + 2].all() and len(n) == 1 and idx[y, x] not in n:
                    idx[y, x] = n.pop()

    ink = int(np.argmin(L))

    def ramp_dark(i):
        c = pal[i] / max(1, pal[i].sum())
        cands = [(np.abs(pal[j] / max(1, pal[j].sum()) - c).sum(), j)
                 for j in range(len(pal)) if L[j] < L[i] - 50]
        return min(cands)[1] if cands else ink

    new = idx.copy()
    for y in range(h):
        for x in range(w):
            if not alpha[y, x]:
                continue
            if outside(y + 1, x) or outside(y, x + 1):
                new[y, x] = ink
            elif (outside(y - 1, x) or outside(y, x - 1)) and L[idx[y, x]] > 60:
                new[y, x] = ramp_dark(idx[y, x])
    return new, alpha


def detect_grid(a, bg, tol=60):
    """Find the concept's own pixel grid: (pitch, phase_x, phase_y, strength).

    Image-model "pixel art" is drawn on a grid of its own choosing (Kynder's at
    16 screen pixels per pixel, others at 10 or 5). Color steps line up on the
    grid lines, so a comb of candidate lines is scored against the summed
    gradient; the smallest pitch within 8% of the best wins (multiples of the
    true pitch score as well, halves score worse).
    """
    sub = np.abs(a - bg).sum(-1) > tol
    if magentaness(bg) > 120:
        sub &= magentaness(a) < 90
    ys, xs = np.where(sub)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    r = a[y0:y1, x0:x1].astype(float)
    gx = np.abs(np.diff(r, axis=1)).sum(-1).sum(0)
    gy = np.abs(np.diff(r, axis=0)).sum(-1).sum(1)
    gx = np.maximum.reduce([gx, np.r_[0, gx[:-1]], np.r_[gx[1:], 0]])  # tolerate 1 px of blur
    gy = np.maximum.reduce([gy, np.r_[0, gy[:-1]], np.r_[gy[1:], 0]])

    def comb(g, p):
        best, phase = 0.0, 0.0
        for ph in np.arange(0, p, 0.5):
            pos = np.round(np.arange(ph, len(g) - 1, p)).astype(int)
            if len(pos) < 4:
                return 0.0, 0.0
            sc = g[pos].mean() / (g.mean() + 1e-9)
            if sc > best:
                best, phase = sc, ph
        return best, phase

    # Image models draw an N x N grid and scale it to the canvas, so the grid
    # lines sit at round(k * W / N) from the image's own edge: test whole grid
    # counts first, exactly aligned.
    H, W = a.shape[:2]

    def at_edges(g, p, origin):
        pos = np.round(np.arange(0, origin + len(g) + p, p)).astype(int) - origin - 1
        pos = pos[(pos >= 0) & (pos < len(g))]
        return g[pos].mean() / (g.mean() + 1e-9) if len(pos) >= 4 else 0.0

    grids = []
    for n in range(48, 257):  # coarser "grids" are chunky strokes, not pixels
        p = W / n
        if p < 3:
            break
        grids.append(((at_edges(gx, p, x0) + at_edges(gy, H / n, y0)) / 2, p))
    top = max(sc for sc, _ in grids)
    sc, p = min((t for t in grids if t[0] >= top * 0.92), key=lambda t: t[1])
    if sc >= 1.4:
        return p, 0.0, 0.0, sc
    # otherwise a free search over pitch and phase
    scores = []
    for p in np.arange(3.0, 24.01, 0.05):
        sx, px = comb(gx, p)
        sy, py = comb(gy, p)
        scores.append(((sx + sy) / 2, p, px, py))
    top = max(sc for sc, *_ in scores)
    sc, p, px, py = min((t for t in scores if t[0] >= top * 0.92), key=lambda t: t[1])
    # phases are boundary positions relative to the crop; +1 for diff indexing
    return p, x0 + px + 1, y0 + py + 1, sc


def sample_grid(a, p, phx, phy):
    """Median of each grid cell's center: one value per concept pixel."""
    h, w = a.shape[:2]
    cx = np.arange(phx % p, w - p / 2, p)
    cy = np.arange(phy % p, h - p / 2, p)
    r = max(1, int(p * 0.25))
    out = np.zeros((len(cy), len(cx), 3), int)
    for j, y in enumerate(cy):
        yc = int(y + p / 2)
        for i, x in enumerate(cx):
            xc = int(x + p / 2)
            blk = a[max(0, yc - r):yc + r + 1, max(0, xc - r):xc + r + 1]
            out[j, i] = np.median(blk.reshape(-1, 3), axis=0)
    return out


def pixel_downscale(idx, alpha, pal, scale):
    """Reduce indexed pixel art by `scale` (< 1) keeping what reads at 1x.

    Per output pixel, over its source window: rare extreme colors (eye shine,
    pupils) win if present; the outline ink wins when it covers a third of
    the window, so 1 px lines survive; otherwise the most common color.
    """
    h, w = idx.shape
    oh, ow = max(1, round(h * scale)), max(1, round(w * scale))
    L = lum(pal)
    order = np.argsort(L)
    ink = int(order[0])
    freq = np.bincount(idx[alpha], minlength=len(pal)) / max(1, alpha.sum())
    extreme = set(order[:2].tolist()) | set(order[-2:].tolist())
    rare = {i for i in extreme if 0 < freq[i] < 0.015}
    out = np.zeros((oh, ow), int)
    oa = np.zeros((oh, ow), bool)
    for j in range(oh):
        y0, y1 = int(j * h / oh), max(int(j * h / oh) + 1, int(round((j + 1) * h / oh)))
        for i in range(ow):
            x0, x1 = int(i * w / ow), max(int(i * w / ow) + 1, int(round((i + 1) * w / ow)))
            win, am = idx[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
            if am.mean() < 0.5:
                continue
            vals = win[am]
            oa[j, i] = True
            hit = [v for v in vals if v in rare]
            if hit:
                out[j, i] = hit[0]
            elif (vals == ink).mean() >= 0.34:
                out[j, i] = ink
            else:
                out[j, i] = np.bincount(vals).argmax()
    return out, oa


def hybrid_downscale(nat, alpha, pal, scale, sharpen=40):
    """Reduce a concept that's bigger than the frame, keeping as much as fits.

    The interior comes from an area average (alpha-premultiplied, lightly
    sharpened) snapped to the palette, which keeps faces, eyes and texture
    that single-pixel picks drop. The line art and silhouette come from
    pixel_downscale's ink, so edges stay crisp.
    """
    from PIL import ImageFilter
    h, w = alpha.shape
    oh, ow = max(1, round(h * scale)), max(1, round(w * scale))
    rgba = np.dstack([nat * alpha[..., None], alpha * 255]).clip(0, 255).astype(np.uint8)
    r = np.asarray(Image.fromarray(rgba, "RGBA").resize((ow, oh), Image.BOX)).astype(float)
    oa = r[..., 3] > 127
    col = np.where(oa[..., None], r[..., :3] * 255 / np.maximum(r[..., 3:4], 1), 0).clip(0, 255)
    if sharpen:
        col = np.asarray(Image.fromarray(col.astype(np.uint8)).filter(
            ImageFilter.UnsharpMask(radius=1, percent=sharpen, threshold=2))).astype(float)
    out = ((col[..., None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    idx = ((nat[..., None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    lines, _ = pixel_downscale(idx, alpha, pal, scale)
    lines = lines[:oh, :ow]
    ink = int(np.argmin(lum(pal)))
    out[(lines == ink) & oa] = ink
    return out, oa


def despeckle(idx, alpha):
    """Remove lone pixels inside flat areas and stray specks off the silhouette."""
    h, w = idx.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if not alpha[y, x]:
                continue
            if alpha[y - 1:y + 2, x - 1:x + 2].sum() - 1 <= 1:
                alpha[y, x] = False
                continue
            n = {idx[y - 1, x], idx[y + 1, x], idx[y, x - 1], idx[y, x + 1]}
            if alpha[y - 1:y + 2, x - 1:x + 2].all() and len(n) == 1 and idx[y, x] not in n:
                idx[y, x] = n.pop()
    return idx, alpha


def convert(src, size=64, fit=60, colors=15, bg=None, tol=60, concept_pitch=None, grid="auto", sharpen=40,
            target=None):
    """target: the subject's largest dimension in the frame (the size ladder,
    STYLE.md §3.1). A concept bigger than that at its own scale is reduced to
    it once; a smaller one is never enlarged. Default: fill the frame."""
    lim = min(target, size - 1) if target else size - 1
    a = np.asarray(Image.open(src).convert("RGB")).astype(int)
    bg = np.asarray(bg, float) if bg is not None else border_color(a)
    found = None
    if concept_pitch or grid == "auto":
        p, phx, phy, strength = detect_grid(a, bg, tol)
        if concept_pitch:
            p = concept_pitch
        if concept_pitch or strength >= 1.4:
            found = (p, phx, phy)
    if found:
        # Read the concept on its own grid: one value per concept pixel.
        nat = sample_grid(a, *found)
    else:
        # No grid (a painted illustration): sample by size, as before.
        a = trim(a, bg, tol)
        a = np.pad(a, ((8, 8), (8, 8), (0, 0)))
        a[:8], a[-8:], a[:, :8], a[:, -8:] = bg, bg, bg, bg
        nat = sample(a, (max(a.shape[:2]) - 16) / min(fit, lim))
    alpha = flood_alpha(nat, bg, tol)
    if magentaness(bg) > 120:
        alpha, nat = chroma_key(nat, alpha)
    ys, xs = np.where(alpha)
    nat, alpha = nat[ys.min():ys.max() + 1, xs.min():xs.max() + 1], alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    exact = np.unique((np.round(nat[alpha] / 8) * 8).clip(0, 248).astype(int), axis=0)
    if found and len(exact) <= colors:
        pal = exact  # clean pixel art: keep the artist's colors exactly
    else:
        pal = detail_palette(nat[alpha].astype(float), colors)
    idx = ((nat[..., None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    h, w = idx.shape
    if found and max(h, w) > lim:
        # Bigger than its target at its own scale: reduce once, to the target,
        # keeping faces and line art (STYLE.md §3.3).
        idx, alpha = hybrid_downscale(nat, alpha, pal, lim / max(h, w), sharpen)
    if found:
        idx, alpha = despeckle(idx, alpha)  # keep the concept's own outline
    else:
        idx, alpha = cleanup(idx, alpha, pal)
    h, w = idx.shape
    if max(h, w) > lim:
        # still bigger than the target or the frame plus a row of floor (the
        # no-grid path samples by size): reduce once more, keeping line art
        idx, alpha = pixel_downscale(idx, alpha, pal, lim / max(h, w))
        h, w = idx.shape
    out = np.zeros((size, size), np.uint8)
    oy, ox = size - h - 1, (size - w) // 2  # feet on the floor, centred
    out[oy:oy + h, ox:ox + w] = np.where(alpha, idx + 1, 0)
    img = Image.fromarray(out, "P")
    flat = [248, 0, 248] + [int(v) for c in pal for v in c]
    img.putpalette(flat + [0] * (768 - len(flat)))
    img.info["concept_grid"] = found
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--size", type=int, default=64)
    ap.add_argument("--fit", type=int, default=60)
    ap.add_argument("--colors", type=int, default=15)
    ap.add_argument("--bg", help="backdrop color R,G,B")
    ap.add_argument("--pitch", type=float,
                    help="concept pixels per native pixel; overrides --fit and never shrinks")
    args = ap.parse_args()
    bg = [int(v) for v in args.bg.split(",")] if args.bg else None
    convert(args.src, args.size, args.fit, args.colors, bg,
            concept_pitch=args.pitch).save(args.dst, transparency=0)


if __name__ == "__main__":
    main()
