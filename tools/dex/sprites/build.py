"""Builds the Aethos dex sprites from tools/dex/sprites/lines/*.py.

Usage:
    python3 tools/dex/sprites/build.py [NAME ...] [--preview DIR] [--sheet PNG]
                                       [--complete] [--no-write]

Each lines module exports MONS, a list of mon_lib.Mon. For every species the
build writes design/dex/sprites/<name>/ in the expansion's own layout, so a
folder can later be copied into graphics/pokemon/<name>/ as it is:

    anim_front.png   64x128, two 64x64 frames (phase 0 and 1)
    back.png         64x64
    normal.pal       JASC, 16 colors, color 0 transparent
    shiny.pal
    icon.png         32x64, two frames, in one of the six shared icon
                     palettes (graphics/pokemon/icon_palettes/pal0-5.pal);
                     index.json records which
    footprint.png    16x16, 1 bit
    overworld.png    192x32: down x2, up x2, side (facing left) x2
    overworld_normal.pal, overworld_shiny.pal

--preview DIR writes one review card per species (and grid crops for
placing details), --sheet writes a contact sheet of every front. The build
also checks each species and exits non-zero on an error.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import sys

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mon_lib import ROOT, FOOTPRINTS, MonFig, Pen, Mon  # noqa: E402
from sprites_lib import save_indexed, to_rgba, Palette  # noqa: E402

OUT = os.path.join(ROOT, "design", "dex", "sprites")
ART = os.path.join(HERE, "art")
SPECIES_DIR = os.path.join(ROOT, "design", "dex", "species")
ICON_PALS = os.path.join(ROOT, "graphics", "pokemon", "icon_palettes")

FOLLOW_SCALE = 0.55  # follower size relative to the battle front
FOLLOW_MAX = 30      # px, inside a 32x32 frame
ICON_W, ICON_H = 30, 27


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_mons():
    mons = {}
    for path in sorted(glob.glob(os.path.join(HERE, "lines", "*.py"))):
        mod_name = "dexline_" + os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(mod_name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for m in getattr(mod, "MONS", []):
            if m.name in mons:
                raise SystemExit(f"duplicate species {m.name} in {path}")
            m.source = os.path.relpath(path, ROOT)
            mons[m.name] = m
    return mons


def dex_numbers():
    out = {}
    for path in glob.glob(os.path.join(SPECIES_DIR, "*.yaml")):
        with open(path) as fh:
            data = yaml.safe_load(fh)
        for sp in data.get("species", []):
            out[sp["name"]] = (sp["dex"], data.get("line"))
    return out


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def art_path(mon, view, phase):
    return os.path.join(ART, f"{mon.name.lower()}_{view}{phase}.txt")


def load_art(path, pal):
    """Reads a hand-finished battle sprite: the --dump format (two column
    header lines, then rows of 'yy' + hex palette indices, '.' for clear)."""
    arr = np.zeros((64, 64), np.int32)
    hexd = "0123456789abcdef"
    head = []
    with open(path) as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if len(head) < 2:
                head.append(line)
                continue
            y = int(line[:3])
            x0 = int(head[0][4]) * 10 + int(head[1][4])
            for i, ch in enumerate(line[4:]):
                if ch == ".":
                    continue
                v = hexd.find(ch)
                if v <= 0 or pal.names[v].startswith("_pad"):
                    raise SystemExit(f"{path}:{n}: {ch!r} is not a palette index")
                arr[y, x0 + i] = v
    return arr


def render(mon: Mon, view, phase=0, W=64, H=64, s=1.0, ox=0.0, oy=0.0, shiny=False, art=True):
    if art and view in ("front", "back") and (W, H, s, ox, oy) == (64, 64, 1.0, 0.0, 0.0):
        path = art_path(mon, view, phase)
        if os.path.exists(path):
            return load_art(path, mon.palette(shiny))
    fig = MonFig(mon.palette(shiny), W, H)
    pen = Pen(fig, s, ox, oy, view, phase)
    mon.draw(pen, view, phase)
    if len(fig.parts) <= 1 and not fig.post:
        return None
    return fig.render()


def bbox(arr):
    ys, xs = np.nonzero(arr)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def render_view(mon, view, phase, fallback):
    """Design-size render of a view, falling back to another view when the
    species doesn't draw it. Returns (array, view actually drawn)."""
    arr = render(mon, view, phase)
    if arr is None or not arr.any():
        arr = render(mon, fallback, phase)
        return arr, fallback
    return arr, view


def fit(mon, view, phase, W, H, s, cx, bottom, shiny=False):
    """Renders `view` at scale s, centered on cx with its lowest pixel on
    row `bottom`, measured from the design-size render."""
    arr = render(mon, view, phase)
    b = bbox(arr)
    x0, y0, x1, y1 = b
    ox = cx - s * (x0 + x1 + 1) / 2
    oy = bottom + 1 - s * (y1 + 1)
    return render(mon, view, phase, W, H, s, ox, oy, shiny=shiny)


class Built:
    pass


def build_mon(mon: Mon, errors, warnings):
    b = Built()
    b.mon = mon
    b.pal = mon.palette()
    b.pal_shiny = mon.palette(True)

    # battle
    b.front = [render(mon, "front", ph) for ph in (0, 1)]
    if b.front[0] is None:
        errors.append(f"{mon.name}: no front view")
        return None
    if b.front[1] is None:
        b.front[1] = b.front[0]
    b.back = render(mon, "back", 0)
    if b.back is None:
        errors.append(f"{mon.name}: no back view")
        return None
    fb = bbox(b.front[0])
    b.front_bbox = fb
    for name, arr in (("front", b.front[0]), ("front frame 2", b.front[1]), ("back", b.back)):
        x0, y0, x1, y1 = bbox(arr)
        if x0 == 0 or y0 == 0 or x1 == 63:
            warnings.append(f"{mon.name}: {name} touches the frame edge (x {x0}-{x1}, y {y0}-{y1})")

    # follower: down, up (else back), side (else front)
    fw, fh = fb[2] - fb[0] + 1, fb[3] - fb[1] + 1
    s_f = min(FOLLOW_SCALE, FOLLOW_MAX / max(fw, fh))
    if mon.follow:
        s_f = mon.follow / fh
    frames = []
    for view, fallback in (("down", "front"), ("up", "back"), ("side", "front")):
        for ph in (0, 1):
            _, v = render_view(mon, view, ph, fallback)
            if v != view and view == "down" and ph == 0:
                warnings.append(f"{mon.name}: no down view, follower uses the front")
            vb = bbox(render(mon, v, ph))
            vw, vh = vb[2] - vb[0] + 1, vb[3] - vb[1] + 1
            s = min(s_f, FOLLOW_MAX / vw, FOLLOW_MAX / vh)
            frames.append((v, ph, s))
    b.follow = [fit(mon, v, ph, 32, 32, s, 16, 30) for v, ph, s in frames]
    b.follow_shiny = [fit(mon, v, ph, 32, 32, s, 16, 30, shiny=True) for v, ph, s in frames]
    b.follow_views = [v for v, _, _ in frames]
    for i, arr in enumerate(b.follow):
        x0, y0, x1, y1 = bbox(arr)
        if x0 == 0 or y0 == 0 or x1 == 31:
            warnings.append(f"{mon.name}: follower frame {i} touches the frame edge")

    # icon
    _, iv = render_view(mon, "icon", 0, "front")
    ib = bbox(render(mon, iv, 0))
    iw, ih = ib[2] - ib[0] + 1, ib[3] - ib[1] + 1
    s_i = min(1.0, ICON_W / iw, ICON_H / ih)
    b.icon_rgb = [fit(mon, iv, 0, 32, 32, s_i, 16, 30), fit(mon, iv, 1, 32, 32, s_i, 16, 29)]
    b.icon_pal, b.icon = quantize_icon(b.icon_rgb, b.pal)

    # footprint
    rows = FOOTPRINTS[mon.foot] if isinstance(mon.foot, str) else mon.foot
    if len(rows) != 16 or any(len(r) != 16 for r in rows):
        errors.append(f"{mon.name}: footprint must be 16 rows of 16")
        return None
    b.foot = np.array([[1 if c == "#" else 0 for c in r] for r in rows], np.uint8)

    # palette use
    used = set()
    for arr in b.front + [b.back] + b.follow:
        used |= set(np.unique(arr).tolist())
    unused = [b.pal.names[i] for i in range(1, 16)
              if i not in used and not b.pal.names[i].startswith("_pad")]
    if unused:
        warnings.append(f"{mon.name}: palette colors never drawn: {unused}")
    b.colors = len([n for n in b.pal.names[1:] if not n.startswith("_pad")])
    return b


# --------------------------------------------------------------------------
# Icons: the six shared icon palettes
# --------------------------------------------------------------------------

def read_jasc(path):
    with open(path) as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    return [tuple(int(v) for v in ln.split()[:3]) for ln in lines[3:19]]


def _lab(c):
    def lin(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(v)) for v in c)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def _dist(a, b):
    """Lab distance, with chroma weighted up so a brown stays a brown
    rather than turning gray in the few-color icon palettes."""
    la, lb = _lab(a), _lab(b)
    dl = la[0] - lb[0]
    ca, cb = (la[1] ** 2 + la[2] ** 2) ** 0.5, (lb[1] ** 2 + lb[2] ** 2) ** 0.5
    dc = ca - cb
    dh2 = max(0.0, (la[1] - lb[1]) ** 2 + (la[2] - lb[2]) ** 2 - dc * dc)
    return dl * dl + 1.6 * dc * dc + 1.6 * dh2


def quantize_icon(frames, pal: Palette):
    pals = [read_jasc(os.path.join(ICON_PALS, f"pal{i}.pal")) for i in range(6)]
    counts = np.zeros(16)
    for f in frames:
        for i, n in zip(*np.unique(f, return_counts=True)):
            counts[i] += n
    best = None
    for pi, ip in enumerate(pals):
        maps, err = [0], 0.0
        for ci in range(1, 16):
            c = pal.colors[ci]
            # keep dark outline colors dark: never map ink to a light gray
            j = min(range(1, 16), key=lambda k: _dist(c, ip[k]))
            maps.append(j)
            err += counts[ci] * _dist(c, ip[j])
        if best is None or err < best[0]:
            best = (err, pi, maps)
    _, pi, maps = best
    lut = np.array(maps, np.int32)
    return pi, [lut[f] for f in frames]


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

def write_mon(b: Built):
    d = os.path.join(OUT, b.mon.name.lower())
    os.makedirs(d, exist_ok=True)
    save_indexed(np.vstack(b.front), b.pal, os.path.join(d, "anim_front.png"))
    save_indexed(b.back, b.pal, os.path.join(d, "back.png"))
    b.pal.write_jasc(os.path.join(d, "normal.pal"))
    b.pal_shiny.write_jasc(os.path.join(d, "shiny.pal"))
    b.pal.write_jasc(os.path.join(d, "overworld_normal.pal"))
    b.pal_shiny.write_jasc(os.path.join(d, "overworld_shiny.pal"))
    save_indexed(np.hstack(b.follow), b.pal, os.path.join(d, "overworld.png"))
    # the shared icon palettes aren't multiples of 8, so write them raw
    icon = np.vstack(b.icon).astype(np.uint8)
    im = Image.fromarray(icon, "P")
    flat = []
    for c in read_jasc(os.path.join(ICON_PALS, f"pal{b.icon_pal}.pal")):
        flat.extend(c)
    im.putpalette(flat)
    im.save(os.path.join(d, "icon.png"), bits=4, transparency=0)
    fp = Image.fromarray(b.foot, "P")
    fp.putpalette([255, 255, 255, 98, 98, 98])
    fp.save(os.path.join(d, "footprint.png"), bits=1)
    return d


def icon_rgba(b, k):
    flat = read_jasc(os.path.join(ICON_PALS, f"pal{b.icon_pal}.pal"))
    a = b.icon[k]
    rgba = np.zeros(a.shape + (4,), np.uint8)
    for i, c in enumerate(flat):
        m = a == i
        rgba[m, :3] = c
        rgba[m, 3] = 0 if i == 0 else 255
    return Image.fromarray(rgba, "RGBA")


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

BG = (240, 232, 216, 255)
PANEL = (224, 212, 188, 255)
INKC = (32, 24, 24, 255)


def _font(size):
    for path in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def card(b: Built, dexno=None):
    """One review card: battle front (both frames), back, shiny front and
    back at 2x; icons, follower frames and footprint at 2x."""
    k = 2
    W = 5 * (64 * k + 8) + 8
    H = 24 + 64 * k + 16 + 32 * k + 26
    im = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(im)
    title = f"#{dexno:03d} {b.mon.name}" if dexno else b.mon.name
    d.text((8, 4), title, fill=INKC, font=_font(14))
    x = 8
    shiny_front = to_rgba(b.front[0], b.pal_shiny)
    shiny_back = to_rgba(b.back, b.pal_shiny)
    for spr in (to_rgba(b.front[0], b.pal), to_rgba(b.front[1], b.pal), to_rgba(b.back, b.pal), shiny_front, shiny_back):
        d.rectangle([x, 24, x + 64 * k - 1, 24 + 64 * k - 1], fill=PANEL)
        im.alpha_composite(_up(spr, k), (x, 24))
        x += 64 * k + 8
    y = 24 + 64 * k + 8
    x = 8
    for i in range(2):
        d.rectangle([x, y, x + 32 * k - 1, y + 32 * k - 1], fill=PANEL)
        im.alpha_composite(_up(icon_rgba(b, i), k), (x, y))
        x += 32 * k + 4
    x += 8
    for i, arr in enumerate(b.follow):
        d.rectangle([x, y, x + 32 * k - 1, y + 32 * k - 1], fill=PANEL)
        im.alpha_composite(_up(to_rgba(arr, b.pal), k), (x, y))
        x += 32 * k + 4
    x += 8
    fp = np.zeros((16, 16, 4), np.uint8)
    fp[b.foot == 1] = (98, 98, 98, 255)
    fp[b.foot == 0] = (255, 255, 255, 255)
    im.alpha_composite(_up(Image.fromarray(fp, "RGBA"), k), (x, y + 16))
    d.text((8, H - 16), f"{b.colors} colors · icon pal {b.icon_pal} · follower {', '.join(b.follow_views[::2])}",
           fill=INKC, font=_font(11))
    return im


def grid(arr, pal, k=10):
    """Upscaled crop with a pixel grid, for placing details by hand."""
    from sprites_lib import grid_preview
    return grid_preview(to_rgba(arr, pal), k)


def sheet(builts, numbers, cols=10):
    k = 1
    cw, ch = 64 * k + 8, 64 * k + 20
    rows = (len(builts) + cols - 1) // cols
    im = Image.new("RGBA", (cols * cw + 8, rows * ch + 8), BG)
    d = ImageDraw.Draw(im)
    f = _font(10)
    for i, b in enumerate(builts):
        x, y = 8 + (i % cols) * cw, 8 + (i // cols) * ch
        d.rectangle([x, y, x + 64 * k - 1, y + 64 * k - 1], fill=PANEL)
        im.alpha_composite(_up(to_rgba(b.front[0], b.pal), k), (x, y))
        n = numbers.get(b.mon.name, (0, ""))[0]
        d.text((x, y + 64 * k + 2), f"{n:03d} {b.mon.name}", fill=INKC, font=f)
    return im


def dump(mon, view, phase, out=None, draft=False):
    arr = render(mon, view, phase, art=not draft)
    if out:
        with open(out, "w") as fh:
            old = sys.stdout
            sys.stdout = fh
            try:
                _dump(mon, view, phase, arr)
            finally:
                sys.stdout = old
        print("wrote", os.path.relpath(out, ROOT))
        return
    _dump(mon, view, phase, arr)


def _dump(mon, view, phase, arr):
    pal = mon.palette()
    hexd = "0123456789abcdef"
    print(f"# {mon.name} {view} phase {phase}. Legend: " +
          ", ".join(f"{hexd[i]}={pal.names[i]}" for i in range(1, 16) if not pal.names[i].startswith("_pad")))
    b = bbox(arr)
    x0, x1 = 0, 63
    print("    " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1)))
    print("    " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(64):
        print("%3d " % y + "".join("." if v == 0 else hexd[v] for v in arr[y, x0:x1 + 1]))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--preview")
    ap.add_argument("--sheet")
    ap.add_argument("--grid", action="store_true", help="with --preview, also write pixel grids")
    ap.add_argument("--complete", action="store_true", help="error if a dex species has no sprite")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--dump", nargs="+", metavar=("VIEW", "PHASE"),
                    help="print NAME's VIEW (front, back, down...) as a hex-index grid for hand polish")
    ap.add_argument("--draft", action="store_true", help="with --dump, dump the code-drawn draft, not the art file")
    ap.add_argument("--start-art", action="store_true",
                    help="with --dump, write the draft to tools/dex/sprites/art/ as the start of a hand-finished file")
    a = ap.parse_args()

    mons = load_mons()
    numbers = dex_numbers()
    for n in a.names:
        if n not in mons:
            raise SystemExit(f"no sprite source for {n}")
    if a.dump:
        view = a.dump[0]
        phase = int(a.dump[1]) if len(a.dump) > 1 else 0
        for n in a.names:
            out = None
            if a.start_art:
                os.makedirs(ART, exist_ok=True)
                out = art_path(mons[n], view, phase)
                if os.path.exists(out):
                    raise SystemExit(f"{out} exists; edit it instead")
            dump(mons[n], view, phase, out, draft=a.draft or a.start_art)
        return
    names = a.names or list(mons)
    names.sort(key=lambda n: numbers.get(n, (999,))[0])

    errors, warnings, builts = [], [], []
    for n in names:
        if n not in numbers:
            errors.append(f"{n}: not a species in design/dex/species")
        b = build_mon(mons[n], errors, warnings)
        if b is None:
            continue
        builts.append(b)
        if not a.no_write:
            write_mon(b)
        if a.preview:
            os.makedirs(a.preview, exist_ok=True)
            card(b, numbers.get(n, (None,))[0]).save(os.path.join(a.preview, f"{n.lower()}.png"))
            if a.grid:
                grid(b.front[0], b.pal).save(os.path.join(a.preview, f"{n.lower()}_grid_front.png"))
                grid(b.back, b.pal).save(os.path.join(a.preview, f"{n.lower()}_grid_back.png"))
    if a.complete:
        missing = sorted(set(numbers) - set(mons), key=lambda n: numbers[n][0])
        for n in missing:
            errors.append(f"{n}: no sprite yet")
    if a.sheet and builts:
        sheet(builts, numbers).save(a.sheet)

    if not a.no_write and not a.names:
        index = {}
        for b in builts:
            index[b.mon.name] = {
                "dex": numbers.get(b.mon.name, (None,))[0],
                "dir": b.mon.name.lower(),
                "icon_pal": b.icon_pal,
                "colors": b.colors,
                "front_bbox": b.front_bbox,
                "source": b.mon.source,
            }
        with open(os.path.join(OUT, "index.json"), "w") as fh:
            json.dump(index, fh, indent=1, sort_keys=True)

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(builts)} species built, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
