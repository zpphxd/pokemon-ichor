#!/usr/bin/env python3
"""Turn a 3x3 walker concept sheet into an engine walker sheet (STYLE.md §3.6).

The concept (from design/art/WALKER_PROMPTS.md) has rows facing down, up and
left, and columns standing, step A and step B, each frame 16x32 on a true pixel
grid. This reads it on its own grid (concept_to_native.detect_grid), keys the
magenta backdrop, maps every color into the family palette, closes a
continuous ink outline, puts the feet on the bottom row (one shift per facing,
so the walk cycle doesn't jitter) and writes the 144x32 sheet in the engine's
order: down, up, left standing; down A, down B; up A, up B; left A, left B.

  python3 tools/ichor/art/walker_from_concept.py CONCEPT.png NAME [--palette folk]
          [--out graphics/object_events/pics/people/ichor/NAME.png] [--preview PNG]

--palette defaults to the family recorded in design/art/walker_prompts.json.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concept_to_native as c2n  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
PALS = ROOT / "graphics/object_events/palettes"
SHEETS = ROOT / "graphics/object_events/pics/people/ichor"
ORDER = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)]  # (row, col)


def read_pal(family):
    v = list(map(int, (PALS / f"ichor_{family}.pal").read_text().split()[3:]))
    return np.array(v, int).reshape(-1, 3)[:16]


def to_lab(rgb):
    """Rough perceptual space: weight green, as the eye does."""
    rgb = np.asarray(rgb, float)
    return rgb * np.array([0.30, 0.59, 0.11]) ** 0.5


def read_grid(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    bg = c2n.border_color(a)
    h, w = a.shape[:2]
    # the prompt asks for a 48x96 grid (3x3 frames of 16x32); trust it when the image fits
    if abs(w / 48 - h / 96) < 0.02 * (w / 48):
        p, phx, phy = w / 48, 0.0, 0.0
    else:
        p, phx, phy, _ = c2n.detect_grid(a, bg)
    nat = c2n.sample_grid(a, p, phx, phy)
    alpha = c2n.flood_alpha(nat, bg, 60)
    if c2n.magentaness(bg) > 120:
        alpha, nat = c2n.chroma_key(nat, alpha)
    return nat, alpha


def to_palette(nat, alpha, pal):
    lab_pal = to_lab(pal[1:])
    d = ((to_lab(nat)[..., None, :] - lab_pal[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1) + 1
    return np.where(alpha, idx, 0)


def close_outline(frame, pal):
    """Every silhouette-edge pixel becomes the family's ink (its darkest color)."""
    ink = 1 + int(c2n.lum(pal[1:]).argmin())
    m = frame != 0
    pad = np.pad(m, 1)
    inner = pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:]
    edge = m & ~inner
    out = frame.copy()
    out[edge & (c2n.lum(pal[frame]) > 70)] = ink
    return out


def convert(path, family):
    pal = read_pal(family)
    nat, alpha = read_grid(path)
    rows, cols = nat.shape[0] // 32, nat.shape[1] // 16
    if rows < 3 or cols < 3:
        raise SystemExit(f"{path}: expected a 3x3 sheet of 16x32 frames, read {cols}x{rows}")
    idx = to_palette(nat, alpha, pal)
    frames = {}
    for r in range(3):
        cells = [idx[r * 32:(r + 1) * 32, c * 16:(c + 1) * 16].copy() for c in range(3)]
        cells = [c2n.despeckle(f, f != 0)[0] * (f != 0) for f in cells]
        # one shift per facing: feet of the standing frame on the bottom row,
        # centered on its standing pose
        ys, xs = np.where(cells[0] != 0)
        if not len(ys):
            raise SystemExit(f"{path}: row {r + 1} has an empty standing frame")
        dy = 31 - ys.max()
        dx = int(round(7.5 - (xs.min() + xs.max()) / 2))
        for c, f in enumerate(cells):
            g = np.zeros_like(f)
            ys, xs = np.where(f != 0)
            ok = (ys + dy >= 0) & (ys + dy < 32) & (xs + dx >= 0) & (xs + dx < 16)
            g[ys[ok] + dy, xs[ok] + dx] = f[ys[ok], xs[ok]]
            frames[(r, c)] = close_outline(g, pal)
    sheet = np.hstack([frames[k] for k in ORDER]).astype(np.uint8)
    return sheet, pal


def save(sheet, pal, out):
    im = Image.fromarray(sheet, "P")
    flat = [int(v) for c in pal for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(out, bits=4, transparency=0)


def preview(sheet, pal, name, out, Z=4):
    """New sheet at 4x on grass, beside Theo and an Emerald townsperson for scale."""
    def rgba(path, n=3):
        im = Image.open(path).convert("RGBA")
        return im.crop((0, 0, 16 * n, 32))
    new = np.zeros(sheet.shape + (4,), np.uint8)
    m = sheet != 0
    new[m, :3] = pal[sheet[m]]
    new[m, 3] = 255
    parts = [Image.fromarray(new),
             rgba(ROOT / "graphics/object_events/pics/people/brendan/walking.png"),
             rgba(ROOT / "graphics/object_events/pics/people/boy_1.png")]
    old = SHEETS / f"{name}.png"
    if old.exists():
        parts.insert(0, rgba(old, 9))
    W = sum(p.width for p in parts) + 6 * len(parts)
    card = Image.new("RGBA", (W, 32), (168, 200, 120, 255))
    x = 0
    for p in parts:
        card.alpha_composite(p, (x, 0))
        x += p.width + 6
    card.convert("RGB").resize((W * Z, 32 * Z), Image.NEAREST).save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("concept")
    ap.add_argument("name")
    ap.add_argument("--palette")
    ap.add_argument("--out")
    ap.add_argument("--preview")
    a = ap.parse_args()
    fam = a.palette
    if not fam:
        rows = json.loads((ROOT / "design/art/walker_prompts.json").read_text())
        fam = next((r["palette"] for r in rows if r["name"] == a.name), "folk")
    sheet, pal = convert(a.concept, fam)
    if a.preview:
        preview(sheet, pal, a.name, a.preview)
    if a.out:
        save(sheet, pal, a.out)
    print(f"{a.name}: {sheet.shape[1] // 16} frames, palette {fam}")


if __name__ == "__main__":
    main()
