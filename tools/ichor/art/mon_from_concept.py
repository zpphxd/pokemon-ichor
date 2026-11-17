#!/usr/bin/env python3
"""Build Pokémon sprites from approved concepts (design/STYLE.md §3).

For each species in SPECIES, from tools/ichor/art/concepts/mon/<name>.png:

  anim_front.png  frame 1 from concept_to_native, plus the hand-fix list;
                  frame 2 is a breathing bob (upper body down 1 px)
  normal.pal      the front's 15 colors
  shiny.pal       the old shiny scheme carried over by hue/saturation/value
                  shift, index for index
  back.png        the existing back pic re-indexed into the new palette, until
                  a back concept exists (its colors then match the front)
  icon.png        the new front reduced to 32x32 in the species' shared icon
                  palette, two frames (bob up 1 px)

Writes design/dex/sprites/<name>/; run `python3 tools/dex/rom/gen.py` after it
to copy into graphics/pokemon/ and re-measure battle coordinates.

These species are protected: tools/dex/sprites/build.py will not overwrite them
(CONCEPT_SOURCED below is read from manifest.json).

  python3 tools/ichor/art/mon_from_concept.py [NAME ...] [--preview DIR]
"""
import argparse
import colorsys
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concept_to_native as c2n  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CONCEPTS = ROOT / "tools/ichor/art/concepts/mon"
OUT = ROOT / "design/dex/sprites"
ICON_PALS = ROOT / "graphics/pokemon/icon_palettes"

# fit: the subject's largest dimension in native pixels (STYLE.md §3.1).
# pivot: the row (fraction of the subject's height from the top) above which
# frame 2 lowers by one pixel.
# fixes: hand-fix pass, (x, y, (r, g, b)) in frame-1 canvas coordinates; each
# color snaps to the nearest palette entry. None makes the pixel transparent.
SPECIES = {
    "kynder":    {"fit": 56, "pivot": 0.55, "fixes": []},
    "dikyon":    {"fit": 60, "pivot": 0.50, "fixes": []},
    "pylakyon":  {"fit": 63, "pivot": 0.50, "fixes": []},
    "nebrel":    {"fit": 56, "pivot": 0.45, "fixes": []},
    "kladoe":    {"fit": 60, "pivot": 0.45, "fixes": []},
    # Her face survived the reduction as a pale blank; give her the concept's
    # amber eyes (2x2, shine upper-left) and a mouth.
    "daphnyad":  {"fit": 63, "pivot": 0.40, "fixes": [
        (26, 16, (240, 232, 200)), (27, 16, (16, 16, 16)), (26, 17, (16, 16, 16)), (27, 17, (224, 176, 64)),
        (31, 16, (240, 232, 200)), (32, 16, (16, 16, 16)), (31, 17, (16, 16, 16)), (32, 17, (224, 176, 64)),
        (29, 19, (208, 184, 160)),
    ]},
    "hipling":   {"fit": 56, "pivot": 0.50, "fixes": []},
    "thalamare": {"fit": 60, "pivot": 0.50, "fixes": []},
    "seismare":  {"fit": 63, "pivot": 0.45, "fixes": []},
}


def read_jasc(path):
    lines = Path(path).read_text().split()
    n = int(lines[2])
    v = list(map(int, lines[3:3 + 3 * n]))
    return np.array(v, int).reshape(n, 3)


def write_jasc(pal, path):
    rows = ["JASC-PAL", "0100", str(len(pal))] + [f"{r} {g} {b}" for r, g, b in pal]
    Path(path).write_text("\r\n".join(rows) + "\r\n")


def save_indexed(a, pal, path):
    im = Image.fromarray(a.astype(np.uint8), "P")
    flat = [int(v) for c in pal for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path, bits=4, transparency=0)


def nearest(pal, rgb, skip0=True):
    d = ((pal - np.asarray(rgb)) ** 2).sum(-1).astype(float)
    if skip0:
        d[0] = 1e18
    return int(d.argmin())


def front_frames(name, cfg):
    img = c2n.convert(CONCEPTS / f"{name}.png", fit=cfg["fit"])
    f0 = np.array(img)
    pal = np.array(img.getpalette()[:48], int).reshape(16, 3)
    for x, y, rgb in cfg["fixes"]:
        f0[y, x] = 0 if rgb is None else nearest(pal, rgb)
    ys = np.where(f0.any(1))[0]
    top, bot = ys.min(), ys.max()
    pivot = int(top + (bot - top) * cfg["pivot"])
    f1 = f0.copy()
    f1[top + 1:pivot + 1] = f0[top:pivot]  # upper body sinks one pixel
    f1[top] = 0
    return f0, f1, pal


def shiny_from_old(pal, old_normal, old_shiny):
    """Carry the designed shiny scheme to the new palette, by nearest hue."""
    out = pal.copy()
    on = old_normal[1:] / 255.0
    os_ = old_shiny[1:] / 255.0
    on_hsv = np.array([colorsys.rgb_to_hsv(*c) for c in on])
    os_hsv = np.array([colorsys.rgb_to_hsv(*c) for c in os_])
    for i in range(1, len(pal)):
        h, s, v = colorsys.rgb_to_hsv(*(pal[i] / 255.0))
        # nearest old color, weighting hue for saturated colors
        dh = np.minimum(abs(on_hsv[:, 0] - h), 1 - abs(on_hsv[:, 0] - h))
        d = dh * 4 * min(s, on_hsv[:, 1].max() + 1e-6) + abs(on_hsv[:, 1] - s) + abs(on_hsv[:, 2] - v)
        j = int(d.argmin())
        a, b = on_hsv[j], os_hsv[j]
        nh = (h + (b[0] - a[0])) % 1.0
        ns = min(1.0, s * (b[1] / a[1])) if a[1] > 0.05 else b[1]
        nv = min(1.0, v * (b[2] / a[2])) if a[2] > 0.05 else b[2]
        r, g, bl = colorsys.hsv_to_rgb(nh, ns, nv)
        out[i] = (np.round(np.array([r, g, bl]) * 255 / 8) * 8).clip(0, 248)
    return out


def back_from_front(f0, pal):
    """Interim back pic until a back concept exists (STYLE.md §3.1).

    Gen 3 backs show the player's own Pokémon turned away, set low and cropped
    by the bottom edge. Mirror the front so it faces up-right, drop it 6 px so
    the base is cropped, and paint out the face: interior eye ink and shine in
    the head become the surrounding fur, so the head reads from behind.
    """
    a = f0[:, ::-1].copy()
    L = c2n.lum(pal)
    ys, xs = np.where(a != 0)
    top, bot, left, right = ys.min(), ys.max(), xs.min(), xs.max()
    head_y = top + int((bot - top) * 0.5)
    head_x = right - int((right - left) * 0.45)  # facing right after the mirror
    ink = set(np.argsort(L)[:2].tolist()) - {0}
    shine = set(np.argsort(L)[-2:].tolist()) - {0}
    out = a.copy()
    for y in range(top, head_y):
        for x in range(head_x, right + 1):
            v = a[y, x]
            if v == 0 or (v not in ink and v not in shine):
                continue
            nb = a[max(0, y - 2):y + 3, max(0, x - 2):x + 3].ravel()
            if (nb == 0).any():
                continue  # silhouette outline stays
            fur = [int(n) for n in nb if n and n not in ink and n not in shine]
            if fur:
                out[y, x] = max(set(fur), key=fur.count)
    drop = 6
    back = np.zeros_like(out)
    back[drop:] = out[:-drop]
    return back


def remap(a, old_pal, new_pal):
    lut = np.zeros(16, int)
    for i in range(1, len(old_pal)):
        lut[i] = nearest(new_pal, old_pal[i])
    return lut[a]


def icon_frames(f0, pal, icon_pal):
    """32x32 icon from the front: median-sample the subject, map to the shared palette."""
    ys, xs = np.where(f0 != 0)
    sub = f0[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    rgb = pal[sub]
    alpha = sub != 0
    h, w = sub.shape
    k = 28 / max(h, w)
    nh, nw = max(1, round(h * k)), max(1, round(w * k))
    out = np.zeros((32, 32), int)
    oy, ox = 31 - nh, (32 - nw) // 2
    for j in range(nh):
        for i in range(nw):
            y0, y1 = int(j / k), max(int(j / k) + 1, int((j + 1) / k))
            x0, x1 = int(i / k), max(int(i / k) + 1, int((i + 1) / k))
            m = alpha[y0:y1, x0:x1]
            if m.mean() < 0.4:
                continue
            col = np.median(rgb[y0:y1, x0:x1][m], axis=0)
            out[oy + j, ox + i] = nearest(icon_pal, col)
    # close the silhouette with the icon palette's darkest color
    dark = 1 + int(c2n.lum(icon_pal[1:]).argmin())
    a = out != 0
    edge = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
    out[edge] = dark
    up = np.zeros_like(out)
    up[:-1] = out[1:]
    return out, up


def icon_pal_index(name):
    src = (ROOT / "src/data/pokemon/species_info/aethos_families.h").read_text()
    m = re.search(rf"\[SPECIES_{name.upper()}\] =.*?\.iconPalIndex = (\d+)", src, re.S)
    return int(m.group(1))


def build(name, cfg):
    d = OUT / name
    old_normal = read_jasc(d / "normal.pal")
    old_shiny = read_jasc(d / "shiny.pal")
    f0, f1, pal = front_frames(name, cfg)
    shiny = shiny_from_old(pal, old_normal, old_shiny)
    back_src = CONCEPTS / f"{name}_back.png"
    if back_src.exists():
        bimg = c2n.convert(back_src, fit=64)
        bpal = np.array(bimg.getpalette()[:48], int).reshape(16, 3)
        back = remap(np.array(bimg), bpal, pal)
    else:
        back = back_from_front(f0, pal)
    ipal = read_jasc(ICON_PALS / f"pal{icon_pal_index(name)}.pal")
    i0, i1 = icon_frames(f0, pal, ipal)
    # the follower shares the battle palette (check_elaia); move it across
    follow = remap(np.array(Image.open(d / "overworld.png")),
                   read_jasc(d / "overworld_normal.pal"), pal)
    return {"front": np.vstack([f0, f1]), "pal": pal, "shiny": shiny, "follow": follow,
            "back": back, "icon": np.vstack([i0, i1]), "icon_pal": ipal}


def write(name, b):
    d = OUT / name
    save_indexed(b["front"], b["pal"], d / "anim_front.png")
    save_indexed(b["back"], b["pal"], d / "back.png")
    write_jasc(b["pal"], d / "normal.pal")
    write_jasc(b["shiny"], d / "shiny.pal")
    save_indexed(b["follow"], b["pal"], d / "overworld.png")
    write_jasc(b["pal"], d / "overworld_normal.pal")
    write_jasc(b["shiny"], d / "overworld_shiny.pal")
    save_indexed(b["icon"], b["icon_pal"], d / "icon.png")


def preview(name, b, out):
    Z = 4
    tiles = []
    for a, p in ((b["front"][:64], b["pal"]), (b["front"][64:], b["pal"]),
                 (b["front"][:64], b["shiny"]), (b["back"], b["pal"])):
        rgb = np.zeros((64, 64, 3), np.uint8) + np.array([168, 200, 120], np.uint8)
        m = a != 0
        rgb[m] = p[a[m]]
        tiles.append(Image.fromarray(rgb).resize((64 * Z, 64 * Z), Image.NEAREST))
    ic = np.zeros((32, 32, 3), np.uint8) + np.array([232, 226, 212], np.uint8)
    m = b["icon"][:32] != 0
    ic[m] = b["icon_pal"][b["icon"][:32][m]]
    tiles.append(Image.fromarray(ic).resize((32 * Z, 32 * Z), Image.NEAREST))
    W = sum(t.width for t in tiles) + 8 * (len(tiles) + 1)
    card = Image.new("RGB", (W, 64 * Z + 16), (232, 226, 212))
    x = 8
    for t in tiles:
        card.paste(t, (x, 8))
        x += t.width + 8
    card.save(Path(out) / f"{name}.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--preview", help="write review cards here instead of writing sprites")
    a = ap.parse_args()
    for n in a.names or SPECIES:
        b = build(n, SPECIES[n])
        if a.preview:
            Path(a.preview).mkdir(parents=True, exist_ok=True)
            preview(n, b, a.preview)
        else:
            write(n, b)
        print(n, "front colors", len(np.unique(b["front"])) - 1)


if __name__ == "__main__":
    main()
