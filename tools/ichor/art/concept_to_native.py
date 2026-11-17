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
    body = kmeans(px, k - len(keep))
    pal = np.vstack([body] + [np.asarray(keep).clip(0, 248)] if keep else [body]).astype(int)
    return np.unique(pal, axis=0)


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


def convert(src, size=64, fit=60, colors=15, bg=None, tol=60, concept_pitch=None):
    a = np.asarray(Image.open(src).convert("RGB")).astype(int)
    bg = np.asarray(bg, float) if bg is not None else border_color(a)
    a = trim(a, bg, tol)
    a = np.pad(a, ((8, 8), (8, 8), (0, 0)))
    a[:8], a[-8:], a[:, :8], a[:, -8:] = bg, bg, bg, bg
    # Sample at the concept's own pixel pitch when given; shrinking a concept
    # below its drawn scale is what destroys detail (STYLE.md §3.2).
    pitch = concept_pitch or (max(a.shape[:2]) - 16) / fit
    nat = sample(a, pitch)
    alpha = flood_alpha(nat, bg, tol)
    ys, xs = np.where(alpha)
    nat, alpha = nat[ys.min():ys.max() + 1, xs.min():xs.max() + 1], alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    pal = detail_palette(nat[alpha].astype(float), colors)
    idx = ((nat[..., None, :] - pal[None, None]) ** 2).sum(-1).argmin(-1)
    idx, alpha = cleanup(idx, alpha, pal)
    h, w = idx.shape
    if h > size or w > size:
        raise SystemExit(f"subject {w}x{h} exceeds the {size}px canvas: regenerate the "
                         f"concept at native scale rather than shrinking it (STYLE.md §3.2)")
    out = np.zeros((size, size), np.uint8)
    oy, ox = size - h - 1, (size - w) // 2  # feet on the floor, centred
    out[oy:oy + h, ox:ox + w] = np.where(alpha, idx + 1, 0)
    img = Image.fromarray(out, "P")
    flat = [248, 0, 248] + [int(v) for c in pal for v in c]
    img.putpalette(flat + [0] * (768 - len(flat)))
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
