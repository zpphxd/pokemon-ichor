#!/usr/bin/env python3
"""Build Pokémon sprites from approved concepts (design/STYLE.md §3).

For each species with a concept in tools/ichor/art/concepts/mon/<name>.png:

  anim_front.png  frame 1 from concept_to_native, plus the hand-fix list;
                  frame 2 is a breathing bob (upper body down 1 px)
  normal.pal      the front's 15 colors
  shiny.pal       the old shiny scheme carried over by hue/saturation/value
                  shift, index for index
  back.png        from <name>_back.png when it exists; otherwise an interim
                  back from the mirrored front with the face painted out
  icon.png        the new front reduced to 32x32 in the species' shared icon
                  palette, two frames (bob up 1 px)

Writes design/dex/sprites/<name>/; run `python3 tools/dex/rom/gen.py` after it
to copy into graphics/pokemon/ and re-measure battle coordinates.

A concept PNG in that folder protects the species: tools/dex/sprites/build.py
will not overwrite it. The concept-sprites skill (.claude/skills) runs it all.

  python3 tools/ichor/art/mon_from_concept.py ingest FOLDER [--dry-run]
  python3 tools/ichor/art/mon_from_concept.py [NAME ...] [--preview DIR] [--sheet PNG]
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

SPECIES_FILE = CONCEPTS / "species.json"
PROMPTS = ROOT / "design/dex/concept_prompts.json"

# Per-species settings live in concepts/mon/species.json; a species without an
# entry gets defaults from its evolution stage (STYLE.md §3.1).
#   fit    the subject's largest dimension in native pixels, for concepts that
#          are not on a true grid (ignored when the pitch is detected)
#   pivot  the row, as a fraction of the subject's height from the top, above
#          which frame 2 lowers by one pixel
#   fixes  the hand-fix pass: [x, y, [r, g, b]] in frame-1 canvas coordinates,
#          each color snapped to the nearest palette entry; null color = clear
STAGE_FIT = {"basic": 56, "middle": 60, "final": 63, "single": 60}

# The size ladder (STYLE.md §3.1): each species' largest dimension in the
# battle frame, from its place in its line, its dex height and its build,
# benchmarked on Emerald (basics ~41 px, middles ~52, finals ~61; Taillow 43x30,
# Natu 25). Concepts are drawn filling their canvas, so without this every
# stage came out 63 px. "size" in species.json overrides it.
SPECIES_YAML = ROOT / "design/dex/species"
LADDER = {  # (position, line length): (low, high) px; height picks the spot
    ("basic", 3): (34, 46), ("middle", 3): (46, 56), ("final", 3): (58, 63),
    ("basic", 2): (36, 50), ("final", 2): (54, 63),
    ("single", 1): (44, 62),
}
LEGENDARY_BST = 600
H_SMALL, H_LARGE = 0.2, 2.0  # metres at the low and high ends of a band
FLYER_SHRINK = 4             # small birds read small


def _dex():
    import yaml
    out = {}
    for f in sorted(SPECIES_YAML.glob("*.yaml")):
        sp = yaml.safe_load(f.read_text())["species"]
        for i, s in enumerate(sp):
            out[s["name"].lower()] = (i, len(sp), s)
    return out


_DEX = None


def ladder_size(name):
    """The species' front size on the ladder, or 63 when it has no dex entry."""
    global _DEX
    _DEX = _DEX if _DEX is not None else _dex()
    if name not in _DEX:
        return 63
    pos, n, s = _DEX[name]
    if sum(s["base_stats"].values()) >= LEGENDARY_BST:
        return 63
    stage = "single" if n == 1 else "basic" if pos == 0 else "final" if pos == n - 1 else "middle"
    lo, hi = LADDER[(stage, 1 if n == 1 else min(n, 3))]
    t = (np.log(max(s.get("height_m", 1.0), 0.15)) - np.log(H_SMALL)) / (np.log(H_LARGE) - np.log(H_SMALL))
    v = lo + (hi - lo) * min(max(t, 0.0), 1.0)
    if "Flying" in s["types"] and stage in ("basic", "middle"):
        v -= FLYER_SHRINK
    return int(round(min(max(v, 28), 63)))


def back_size(front):
    """Gen 3 backs sit a little bigger than small fronts (Mudkip 41 -> 53)."""
    return int(round(min(63, front + (63 - front) * 0.35)))


def stage_of(name):
    if PROMPTS.exists():
        for r in json.loads(PROMPTS.read_text()):
            if r["name"].lower() == name:
                return r.get("stage", "single")
    return "single"


def config(name):
    table = json.loads(SPECIES_FILE.read_text()) if SPECIES_FILE.exists() else {}
    c = {"fit": STAGE_FIT[stage_of(name)], "pivot": 0.5, "fixes": [], "size": ladder_size(name)}
    c.update(table.get(name, {}))
    return c


def concept_names():
    return sorted(p.stem for p in CONCEPTS.glob("*.png") if not p.stem.endswith("_back"))


def grid_pitch(path):
    """Pixels per native pixel for a true-grid concept from the prompt page.

    The prompts ask for a 64x64 grid rendered at 512x512; any square image
    whose side is a multiple of 64 (256 or more) is read at that exact pitch,
    so nothing is resized. Anything else returns None (fit-based sampling).
    """
    w, h = Image.open(path).size
    if w == h and w >= 256 and w % 64 == 0:
        return w / 64
    return None


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
    src = CONCEPTS / f"{name}.png"
    img = c2n.convert(src, fit=cfg["fit"], sharpen=cfg.get("sharpen", 40), target=cfg["size"])
    f0 = np.array(img)
    pal = np.array(img.getpalette()[:48], int).reshape(16, 3)
    for x, y, rgb in cfg.get("fixes", []):
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


def shiny_global(pal, old_normal, old_shiny):
    """One smooth shift for every colored entry, taken from the old design's
    most saturated body color, so neighboring shades stay neighbors."""
    on = old_normal[1:] / 255.0
    os_ = old_shiny[1:] / 255.0
    hn = np.array([colorsys.rgb_to_hsv(*c) for c in on])
    hs = np.array([colorsys.rgb_to_hsv(*c) for c in os_])
    j = int(np.argmax(hn[:, 1] * (hn[:, 2] > 0.25)))
    dh = hs[j, 0] - hn[j, 0]
    rs = hs[j, 1] / max(hn[j, 1], 0.05)
    rv = hs[j, 2] / max(hn[j, 2], 0.05)
    out = pal.copy()
    for i in range(1, len(pal)):
        h, s, v = colorsys.rgb_to_hsv(*(pal[i] / 255.0))
        if s < 0.15:
            continue  # neutrals, outlines and highlights stay
        r, g, b = colorsys.hsv_to_rgb((h + dh) % 1.0, min(1.0, s * rs), min(1.0, v * rv))
        out[i] = (np.round(np.array([r, g, b]) * 255 / 8) * 8).clip(0, 248)
    return out


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


def recolor(pal, spec):
    """Move a color family onto a planned ramp, by brightness rank.

    spec: {"hue": [lo, hi] degrees, "min_sat": 0.25, "ink_below": 0.25,
           "ink": [r, g, b], "ramp": [[r, g, b], ...] dark -> light}
    Palette entries in the hue range take the ramp's color at their own
    relative brightness (interpolated between steps), keeping their order;
    near-black entries in the range become the ramp's outline ink.
    """
    if not spec:
        return pal
    out = pal.copy()
    lo, hi = spec.get("hue", [0, 360])
    ramp = np.array(spec["ramp"], float)
    fam, ink = [], []
    for i in range(1, len(pal)):
        h, s, v = colorsys.rgb_to_hsv(*(pal[i] / 255.0))
        if spec.get("neutral"):
            # grays and near-grays (stone, ash), not the outline or the whites
            if s >= spec.get("max_sat", 0.18) or not (0.15 <= v <= 0.92):
                continue
        elif not (lo <= h * 360 <= hi) or s < spec.get("min_sat", 0.25):
            continue
        (ink if v < spec.get("ink_below", 0.25) else fam).append(i)
    # several near-blacks: keep them as distinct steps from the outline ink
    # toward the ramp's darkest color, so no palette slot is wasted
    ink.sort(key=lambda i: c2n.lum(pal[i]))
    for k, i in enumerate(ink):
        t = k / max(1, len(ink)) * 0.6
        col = np.array(spec.get("ink", pal[i]), float) * (1 - t) + ramp[0] * t
        out[i] = (np.round(col / 8) * 8).clip(0, 248)
    fam.sort(key=lambda i: c2n.lum(pal[i]))
    lums = [c2n.lum(pal[i]) for i in fam]
    lo_l, hi_l = (min(lums), max(lums)) if lums else (0, 1)
    for r, i in enumerate(fam):
        # place each color by its own brightness, so a mostly mid-dark body
        # stays mid-toned instead of being spread evenly toward the light end
        t = (c2n.lum(pal[i]) - lo_l) / max(1e-6, hi_l - lo_l) * (len(ramp) - 1)
        a, b = int(np.floor(t)), min(len(ramp) - 1, int(np.floor(t)) + 1)
        col = ramp[a] + (ramp[b] - ramp[a]) * (t - a)
        out[i] = (np.round(col / 8) * 8).clip(0, 248)
    return out


def rim_light(a, pal):
    """A 1 px rim of light inside the lit (top/left) silhouette edge.

    Body pixels just inside the outline on the top or left take the next
    lighter color of their own hue, the classic Gen 3 way of rounding a form.
    """
    L = c2n.lum(pal)
    out = a.copy()
    h, w = a.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            v = a[y, x]
            if not v or L[v] < 60 or L[v] > 200:
                continue
            # only where the body is thick enough to round: a rim on a 1-2 px
            # leg or fin edge reads as noise, not light
            if not (a[y + 1, x] and a[y, x + 1] and (y + 2 >= h or a[y + 2, x]) and (x + 2 >= w or a[y, x + 2])):
                continue
            for dy, dx in ((-1, 0), (0, -1)):
                n1, n2 = a[y + dy, x + dx], a[y + 2 * dy, x + 2 * dx] if 0 <= y + 2 * dy and 0 <= x + 2 * dx else 0
                if n1 and L[n1] < 40 and not n2:  # outline pixel with air beyond it
                    hv = colorsys.rgb_to_hsv(*(pal[v] / 255.0))[0]
                    cands = [j for j in range(1, len(pal)) if L[j] > L[v] + 15 and
                             abs(colorsys.rgb_to_hsv(*(pal[j] / 255.0))[0] - hv) < 0.06]
                    if cands:
                        out[y, x] = min(cands, key=lambda j: L[j])
                    break
    return out


def build(name, cfg):
    d = OUT / name
    old_normal = read_jasc(d / "normal.pal")
    old_shiny = read_jasc(d / "shiny.pal")
    f0, f1, pal0 = front_frames(name, cfg)
    # Indices are assigned against the concept's own palette (pal0); a
    # recolor then changes colors only, so every shading step is kept.
    pal = recolor(pal0, cfg.get("recolor"))
    if cfg.get("shiny_recolor"):
        # a shiny designed from its dex line: ramps applied to the normal palette
        shiny = pal
        for spec in cfg["shiny_recolor"]:
            shiny = recolor(shiny, spec)
    elif cfg.get("shiny") == "global":
        shiny = shiny_global(pal, old_normal, old_shiny)
    else:
        shiny = shiny_from_old(pal, old_normal, old_shiny)
    back_src = CONCEPTS / f"{name}_back.png"
    if back_src.exists():
        bimg = c2n.convert(back_src, fit=64, sharpen=cfg.get("sharpen", 40), target=back_size(cfg["size"]))
        bpal = np.array(bimg.getpalette()[:48], int).reshape(16, 3)
        back = remap(np.array(bimg), bpal, pal0)
    else:
        bf, _, bp = front_frames(name, dict(cfg, size=back_size(cfg["size"])))
        back = back_from_front(remap(bf, bp, pal0), pal0)
    if cfg.get("rim_light"):
        f0, f1, back = (rim_light(x, pal) for x in (f0, f1, back))
    ipal = read_jasc(ICON_PALS / f"pal{icon_pal_index(name)}.pal")
    # icons are reduced from the full-frame conversion, so a small battle
    # sprite still gets a detailed party icon
    full = f0 if cfg["size"] >= 63 else front_frames(name, dict(cfg, size=63))
    if full is not f0:
        full = remap(full[0], full[2], pal0)
        if cfg.get("rim_light"):
            full = rim_light(full, pal)
    i0, i1 = icon_frames(full, pal, ipal)
    # the follower shares the battle palette (check_elaia); move it across,
    # unless this builder already wrote it in this palette's index layout
    follow = np.array(Image.open(d / "overworld.png"))
    old_ow = read_jasc(d / "overworld_normal.pal")
    if not np.array_equal(old_ow, pal):
        follow = remap(follow, old_ow, pal0)
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


NAME_RE = re.compile(r"^(?:(\d{1,3})_)?([a-z]+?)(?:_(front|back))?$")


def ingest(folder, dry_run=False):
    """Check a folder of returned concepts and file them under concepts/mon/.

    Accepts the prompt page's names (004_kynder_front.png, 004_kynder_back.png)
    or bare <name>.png. Every file is checked before anything is copied: the
    species exists, the number matches it, the backdrop is flat, and the
    subject fits the 64x64 frame. Returns the species names ingested.
    """
    dex = {r["name"].lower(): r for r in json.loads(PROMPTS.read_text())}
    plan, problems = [], []
    for f in sorted(Path(folder).iterdir()):
        if f.suffix.lower() not in (".png", ".webp", ".jpg", ".jpeg"):
            continue
        m = NAME_RE.match(f.stem.lower())
        if not m or m.group(2) not in dex:
            problems.append(f"{f.name}: not a dex species name (expected e.g. 004_kynder_front.png)")
            continue
        num, name, view = m.group(1), m.group(2), m.group(3) or "front"
        if num and int(num) != dex[name]["dex"]:
            problems.append(f"{f.name}: {name} is #{dex[name]['dex']:03d}, not #{int(num):03d}")
            continue
        try:
            im = Image.open(f).convert("RGB")
        except Exception as e:  # unreadable or not an image
            problems.append(f"{f.name}: can't read it ({e})")
            continue
        a = np.asarray(im).astype(int)
        # Compare the four corners' averages, not single pixels: JPEG noise and
        # a gentle gradient are fine (the flood fill handles them); a scene isn't.
        corners = np.array([c.reshape(-1, 3).mean(0) for c in
                            (a[:8, :8], a[:8, -8:], a[-8:, :8], a[-8:, -8:])])
        # agree with the median corner; one corner may be covered by the
        # subject itself (smoke, a wing tip) and is only a warning
        off = np.abs(corners - np.median(corners, axis=0)).sum(-1) > 90
        if off.sum() > 1:
            problems.append(f"{f.name}: the background isn't flat; regenerate on solid magenta")
            continue
        warn = " (the subject touches a corner: it is cropped at the frame)" if off.any() else ""
        if not (im.width == im.height and im.width % 64 == 0 and im.width >= 256):
            warn += f" (not on a 64-grid, {im.width}x{im.height}: sampled by size, check detail)"
        dst = CONCEPTS / (f"{name}_back.png" if view == "back" else f"{name}.png")
        tmp = CONCEPTS / f".check_{name}_{view}.png"
        im.save(tmp)
        try:
            c2n.convert(tmp, fit=64 if view == "back" else config(name)["fit"])
        except SystemExit as e:
            problems.append(f"{f.name}: {e}")
            continue
        finally:
            tmp.unlink(missing_ok=True)
        plan.append((tmp, dst, im, name, view, warn))
    for _, dst, im, name, view, warn in plan:
        print(f"{'would file' if dry_run else 'filed'} {name} {view} -> {dst.relative_to(ROOT)}{warn}")
        if not dry_run:
            im.save(dst)
    for p_ in problems:
        print("SKIPPED", p_)
    return sorted({n for _, _, _, n, _, _ in plan})


def sheet(rows, path):
    """Before/after review sheet: old front and back beside the new set, 3x."""
    Z, pad, green = 3, 8, (168, 200, 120)

    def tile(a, pal, size=64, bg=green):
        rgb = np.zeros((size, size, 3), np.uint8) + np.array(bg, np.uint8)
        m = a != 0
        rgb[m] = np.asarray(pal)[a[m]]
        return Image.fromarray(rgb).resize((size * Z, size * Z), Image.NEAREST)

    cards = []
    for name, before, b in rows:
        tiles = [tile(before["front"], before["pal"]), tile(before["back"], before["pal"]),
                 tile(b["front"][:64], b["pal"]), tile(b["front"][64:], b["pal"]),
                 tile(b["front"][:64], b["shiny"]), tile(b["back"], b["pal"]),
                 tile(b["icon"][:32], b["icon_pal"], 32, (232, 226, 212))]
        w = sum(t.width for t in tiles) + pad * (len(tiles) + 2)
        card = Image.new("RGB", (w, 64 * Z + 2 * pad + 14), (232, 226, 212))
        x = pad
        for k, t in enumerate(tiles):
            card.paste(t, (x, pad + 14))
            x += t.width + pad + (pad if k == 1 else 0)
        from PIL import ImageDraw
        ImageDraw.Draw(card).text((pad, 2), f"{name}:  BEFORE front, back  |  AFTER front, frame 2, shiny, back, icon", fill=0)
        cards.append(card)
    out = Image.new("RGB", (max(c.width for c in cards), sum(c.height for c in cards)), (232, 226, 212))
    y = 0
    for c in cards:
        out.paste(c, (0, y))
        y += c.height
    out.save(path)


def grid(name, b, out, Z=10):
    """Frame 1 at 10x with every 5th column/row numbered, for writing fixes."""
    from PIL import ImageDraw
    a, pal = b["front"][:64], b["pal"]
    im = Image.new("RGB", (64 * Z, 64 * Z), (168, 200, 120))
    d = ImageDraw.Draw(im)
    for y in range(64):
        for x in range(64):
            if a[y, x]:
                d.rectangle([x * Z, y * Z, x * Z + Z - 1, y * Z + Z - 1], fill=tuple(int(v) for v in pal[a[y, x]]))
    for k in range(0, 64, 5):
        d.line([k * Z, 0, k * Z, 64 * Z], fill=(40, 40, 220) if k % 10 == 0 else (150, 150, 240))
        d.line([0, k * Z, 64 * Z, k * Z], fill=(40, 40, 220) if k % 10 == 0 else (150, 150, 240))
        d.text((k * Z + 1, 1), str(k), fill=(20, 20, 160))
        d.text((1, k * Z + 1), str(k), fill=(20, 20, 160))
    im.save(Path(out) / f"{name}_grid.png")
    pal_txt = ", ".join(f"{i}:{tuple(int(v) for v in c)}" for i, c in enumerate(pal) if i)
    print(f"{name} palette {pal_txt}")


def current(name):
    d = OUT / name
    pal = read_jasc(d / "normal.pal")
    return {"front": np.array(Image.open(d / "anim_front.png"))[:64],
            "back": np.array(Image.open(d / "back.png")), "pal": pal}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        ap = argparse.ArgumentParser(prog="mon_from_concept.py ingest")
        ap.add_argument("folder")
        ap.add_argument("--dry-run", action="store_true")
        a = ap.parse_args(sys.argv[2:])
        names = ingest(a.folder, a.dry_run)
        print("species:", " ".join(names) if names else "(none)")
        return
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--preview", help="write review cards here instead of writing sprites")
    ap.add_argument("--sheet", help="also write a before/after review sheet (PNG)")
    ap.add_argument("--grid", help="with --preview: also write numbered 10x grids of frame 1 here")
    a = ap.parse_args()
    rows = []
    for n in [x.lower() for x in a.names] or concept_names():
        if not (CONCEPTS / f"{n}.png").exists():
            raise SystemExit(f"no concept for {n}: expected {(CONCEPTS / (n + '.png')).relative_to(ROOT)}")
        before = current(n)
        b = build(n, config(n))
        rows.append((n, before, b))
        if a.preview:
            Path(a.preview).mkdir(parents=True, exist_ok=True)
            preview(n, b, a.preview)
            if a.grid:
                Path(a.grid).mkdir(parents=True, exist_ok=True)
                grid(n, b, a.grid)
        else:
            write(n, b)
        print(n, "front colors", len(np.unique(b["front"])) - 1)
    if a.sheet and rows:
        sheet(rows, a.sheet)
        print("review sheet:", a.sheet)


if __name__ == "__main__":
    main()
