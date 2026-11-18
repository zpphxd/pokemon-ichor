#!/usr/bin/env python3
"""Pan's Crook's climbable faces for the tilesets that have no painter of their
own (ported ones, such as gTileset_Arkadia).

Skiron and the cave draw their faces in their own build scripts
(skiron_rock.crook, cave_dark_kit); this file is for a secondary whose
porytiles_src is the source of truth. For each face in FACES it takes an
existing cliff metatile, paints crook_marks's handholds, ivy and hoof votive
over it, and stores the result as a new metatile at the end of the tileset
with MB_ROCK_CLIMB:

  1. Each 8x8 quarter the marks touch is flattened (every layer of the base,
     then the marks) and stored as one new tile, in whichever of the 13
     palettes holds its colors best (the base's own, nearly always). Quarters
     the marks miss keep the base's tile entries, so a face cell costs two or
     three new tiles.
  2. porytiles_bin gets the tiles, metatiles and attributes; porytiles_src gets
     the same metatile drawn into bottom.png and a line in attributes.csv, so
     the sources still describe the tileset.
  3. It is idempotent: a face already built (same id, same art) is left alone,
     and the run prints the metatile ids for the map builders.

The tile budget is checked against 496 (Arkadia's doors: CLAUDE.md).

Usage: /usr/bin/python3 tools/ichor/art/crook_faces.py [--check] [--preview out.png]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crook_marks as CM  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
MB_ROCK_CLIMB = None      # read from include/constants/metatile_behaviors.h

# Role colors, matched to the nearest color the chosen palette holds.
ROLE_RGB = {"H": (32, 24, 24), "h": (72, 72, 80), "L": (232, 232, 224), "W": (176, 176, 176),
            "I": (40, 72, 40), "i": (72, 112, 48), "v": (120, 152, 64),
            "V": (56, 56, 64), "S": (216, 216, 208)}

# tileset -> [(name, base metatile, kind, lip row or foot base)], in id order.
# Arkadia's grey limestone crag (0x224-0x236), right-hand edge pieces: the
# face sits on the crag's east edge, beside the cypress stand over Pan's grotto.
FACES = {
    "arkadia": {
        "primary": "aethos",
        "tile_limit": 496,
        "faces": [
            ("crook_top", 0x226, "top", 3),
            ("crook_face", 0x22E, "face", None),
            ("crook_foot", 0x236, "foot", 13),
        ],
    },
}


def behaviors():
    names, n = {}, 0
    text = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    body = text[text.index("{") + 1:text.index("}")]
    for line in body.splitlines():
        line = line.split("//")[0].strip().rstrip(",")
        if not line:
            continue
        if "=" in line:
            k, v = (p.strip() for p in line.split("="))
            n = int(v, 0)
            names[k] = n
        else:
            names[line] = n
        n += 1
    return names


def read_pal(p):
    lines = Path(p).read_text().split()
    vals = [int(v) for v in lines[3:3 + 48]]
    return [tuple(vals[i:i + 3]) for i in range(0, 48, 3)]


class Tileset:
    def __init__(self, name, primary):
        self.name = name
        self.d = ROOT / "data/tilesets/secondary" / name
        self.bin = self.d / "porytiles_bin"
        self.src = self.d / "porytiles_src"
        pbin = ROOT / "data/tilesets/primary" / primary / "porytiles_bin"
        self.pal = [read_pal(pbin / f"palettes/{i:02d}.pal") for i in range(6)] + \
                   [read_pal(self.bin / f"palettes/{i:02d}.pal") for i in range(6, 13)]
        self.ptiles = np.array(Image.open(pbin / "tiles.png"))
        self.im = Image.open(self.bin / "tiles.png")
        self.tiles = np.array(self.im)
        self.meta = np.fromfile(self.bin / "metatiles.bin", "<u2").reshape(-1, 8).copy()
        self.attrs = np.fromfile(self.bin / "metatile_attributes.bin", "<u2").copy()

    # tiles are stored as pal * 16 + color in the preview PNG; only the low nibble matters
    def tile(self, idx):
        src, i = (self.ptiles, idx) if idx < 512 else (self.tiles, idx - 512)
        w = src.shape[1] // 8
        y, x = divmod(i, w)
        if y * 8 >= src.shape[0]:
            return np.zeros((8, 8), np.uint8)
        return src[y * 8:y * 8 + 8, x * 8:x * 8 + 8] & 0x0F

    def used_tiles(self):
        idx = self.meta & 0x3FF
        refs = idx[idx >= 512] - 512
        a = self.tiles & 0x0F
        w = a.shape[1] // 8
        drawn = [i for i in range((a.shape[0] // 8) * w)
                 if a[(i // w) * 8:(i // w) * 8 + 8, (i % w) * 8:(i % w) * 8 + 8].any()]
        return max([int(refs.max()) if len(refs) else -1] + drawn) + 1

    def quarter_rgba(self, mid, q):
        """The quarter q (0 TL, 1 TR, 2 BL, 3 BR) of metatile mid, layers flattened."""
        out = np.zeros((8, 8, 4), np.uint8)
        ent = self.meta[mid - 0x200]
        for layer in range(2):
            v = int(ent[layer * 4 + q])
            t = self.tile(v & 0x3FF)
            if v >> 10 & 1:
                t = t[:, ::-1]
            if v >> 11 & 1:
                t = t[::-1]
            pal = self.pal[v >> 12] if (v >> 12) < 13 else self.pal[0]
            m = t > 0
            for y, x in zip(*np.nonzero(m)):
                out[y, x, :3] = pal[t[y, x]]
                out[y, x, 3] = 255
        return out


def render(ts, ent):
    """A metatile entry list drawn to 16x16 RGBA."""
    out = np.zeros((16, 16, 4), np.uint8)
    for layer in range(2):
        for q in range(4):
            v = int(ent[layer * 4 + q])
            t = ts.tile(v & 0x3FF) if (v & 0x3FF) < 512 else None
            if t is None:
                i = (v & 0x3FF) - 512
                w = ts.tiles.shape[1] // 8
                y, x = divmod(i, w)
                t = ts.tiles[y * 8:y * 8 + 8, x * 8:x * 8 + 8] & 0x0F
            if v >> 10 & 1:
                t = t[:, ::-1]
            if v >> 11 & 1:
                t = t[::-1]
            pal = ts.pal[(v >> 12) % 13]
            qx, qy = (q % 2) * 8, (q // 2) * 8
            for y, x in zip(*np.nonzero(t)):
                out[qy + y, qx + x, :3] = pal[t[y, x]]
                out[qy + y, qx + x, 3] = 255
    return out


def nearest(pal, rgb):
    best, bi = None, 0
    for i, c in enumerate(pal[1:], 1):
        d = sum((a - b) ** 2 for a, b in zip(c, rgb))
        if best is None or d < best:
            best, bi = d, i
    return bi, best


def fit(ts, rgba, marks_q):
    """Pick a palette for an 8x8 RGBA (+ role marks) and index it."""
    best = None
    for p in range(13):
        pal = ts.pal[p]
        err, idx = 0, np.zeros((8, 8), np.uint8)
        for y in range(8):
            for x in range(8):
                role = marks_q.get((x, y))
                if role:
                    i, e = nearest(pal, ROLE_RGB[role])
                    err += e // 4          # a role only needs to be close
                elif rgba[y, x, 3]:
                    i, e = nearest(pal, tuple(int(v) for v in rgba[y, x, :3]))
                    err += e
                else:
                    i = 0
                idx[y, x] = i
        if best is None or err < best[0]:
            best = (err, p, idx)
    return best[1], best[2], best[0]


def build(name, cfg, check=False):
    mb = behaviors()["MB_ROCK_CLIMB"]
    ts = Tileset(name, cfg["primary"])
    first = len(ts.meta)
    csv = ts.src / "attributes.csv"
    lines = csv.read_text().splitlines()
    tag = "# crook_faces.py"
    done = any(tag in l for l in lines)
    if done:
        # already built: the faces are the last metatiles
        first -= len(cfg["faces"])
        ids = {key: 0x200 + first + j for j, (key, *_) in enumerate(cfg["faces"])}
        print(f"crook_faces: {name}: already built, {ts.used_tiles()} of {cfg['tile_limit']} tiles used")
        for key, mid in ids.items():
            print(f"  {key}: {mid:#x}")
        return ids
    n_tiles = ts.used_tiles()
    new_tiles, ids, out = [], {}, []
    for (key, base, kind, row) in cfg["faces"]:
        if kind == "top":
            m = CM.marks("top", lip=row)
        elif kind == "foot":
            m = CM.marks("foot", foot_base=row)
        else:
            m = CM.marks("face")
        ent = [int(e) for e in ts.meta[base - 0x200]]
        new = list(ent)
        for q in range(4):
            qx, qy = (q % 2) * 8, (q // 2) * 8
            mq = {(x - qx, y - qy): r for (x, y), r in m.items() if qx <= x < qx + 8 and qy <= y < qy + 8}
            if not mq:
                continue
            rgba = ts.quarter_rgba(base, q)
            p, idx, err = fit(ts, rgba, mq)
            ti = n_tiles + len(new_tiles)
            new_tiles.append(p * 16 + idx)
            new[q] = (512 + ti) | (p << 12)
            new[4 + q] = 0
        mid = 0x200 + first + len(out)
        ids[key] = mid
        out.append((key, mid, new, (int(ts.attrs[base - 0x200]) & ~0xFF) | mb))
    total = n_tiles + len(new_tiles)
    print(f"crook_faces: {name}: {len(out)} faces at {out[0][1]:#x}-{out[-1][1]:#x}, "
          f"{len(new_tiles)} new tiles, {total} of {cfg['tile_limit']} used")
    if total > cfg["tile_limit"]:
        sys.exit(f"crook_faces: {name} is over its tile budget")
    for key, mid, _, _ in out:
        print(f"  {key}: {mid:#x}")
    if check:
        return ids
    # porytiles_bin: tiles, metatiles, attributes
    ts.tiles_new = new_tiles
    a = ts.tiles.copy()
    w = a.shape[1] // 8
    need_rows = (total + w - 1) // w
    if need_rows * 8 > a.shape[0]:
        a = np.vstack([a, np.zeros((need_rows * 8 - a.shape[0], a.shape[1]), a.dtype)])
    for k, t in enumerate(new_tiles):
        i = n_tiles + k
        y, x = divmod(i, w)
        a[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = t
    im = Image.fromarray(a.astype(np.uint8), "P")
    im.putpalette(ts.im.getpalette())
    im.save(ts.bin / "tiles.png")
    meta = np.vstack([ts.meta] + [np.array(e, "<u2").reshape(1, 8) for _, _, e, _ in out])
    attrs = np.concatenate([ts.attrs, np.array([at for _, _, _, at in out], "<u2")])
    meta.astype("<u2").tofile(ts.bin / "metatiles.bin")
    attrs.astype("<u2").tofile(ts.bin / "metatile_attributes.bin")
    # porytiles_src: the composite into bottom.png, empty middle and top, the behavior
    imgs = {ln: Image.open(ts.src / f"{ln}.png").convert("RGBA") for ln in ("bottom", "middle", "top")}
    rows = (first + len(out) + 7) // 8
    for ln, img in imgs.items():
        if img.height < rows * 16:
            grown = Image.new("RGBA", (128, rows * 16), (0, 0, 0, 0))
            grown.paste(img, (0, 0))
            imgs[ln] = grown
    for key, mid, e, _ in out:
        i = mid - 0x200
        box = ((i % 8) * 16, (i // 8) * 16)
        imgs["bottom"].paste(Image.fromarray(render(ts, e)), box)
        for ln in ("middle", "top"):
            imgs[ln].paste(Image.new("RGBA", (16, 16), (0, 0, 0, 0)), box)
    for ln, img in imgs.items():
        img.save(ts.src / f"{ln}.png")
    keep = [l for l in lines if tag not in l]
    keep += [f"{mid - 0x200},MB_ROCK_CLIMB" + (f"  {tag} {out[0][1]:#x} tiles {n_tiles}" if j == 0 else f"  {tag}")
             for j, (_, mid, _, _) in enumerate(out)]
    csv.write_text("\n".join(keep) + "\n")
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="print the ids and budgets, write nothing")
    args = ap.parse_args()
    for name, cfg in FACES.items():
        build(name, cfg, check=args.check)


if __name__ == "__main__":
    main()
