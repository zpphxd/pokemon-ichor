#!/usr/bin/env python3
"""Review renders for aethos: maps, metatile sheets and a Hoenn-town preview.

Hoenn secondaries (Petalburg and the rest) reach into the primary by raw tile
number, written against General's tile order. Porytiles packs aethos in its
own order, so those references land on unrelated tiles: a raw render of
Littleroot on aethos + petalburg shows garbage around doors and walls. That is
expected and never seen in Aethos maps, whose secondaries are compiled against
aethos.

To preview aethos in a Hoenn town anyway, --remap rewrites the secondary's
primary references in memory: each General tile is matched to the aethos tile
painted at the same metatile, layer and quadrant (with flips and palette).
This is what recompiling that secondary against aethos would give.

Usage:
  aethos_review.py LAYOUT_ROUTE101 [-o out.png] [--scale 2]
  aethos_review.py LAYOUT_LITTLEROOT_TOWN --secondary petalburg --remap
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map as rm  # noqa: E402


def primary_tile_map():
    """General tile -> (aethos tile, hflip, vflip, palette)."""
    g = np.fromfile(ROOT / "data/tilesets/primary/general/metatiles.bin", "<u2").reshape(-1, 8)
    a = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin", "<u2").reshape(-1, 8)
    out = {0: (0, 0, 0, 0)}
    for m in range(min(len(g), len(a))):
        for k in range(8):
            eg, ea = int(g[m, k]), int(a[m, k])
            tg = eg & 0x3FF
            if tg == 0 or tg in out:
                continue
            ta = ea & 0x3FF
            if ta == 0:
                continue
            hf = ((ea >> 10) ^ (eg >> 10)) & 1
            vf = ((ea >> 11) ^ (eg >> 11)) & 1
            out[tg] = (ta, hf, vf, ea >> 12)
    return out


def remap_secondary(sec):
    tmap = primary_tile_map()
    mt = sec.metatiles.copy()
    missing = set()
    for idx in np.ndindex(mt.shape):
        e = int(mt[idx])
        t = e & 0x3FF
        if t == 0 or t >= rm.NUM_TILES_IN_PRIMARY:
            continue
        if t not in tmap:
            missing.add(t)
            continue
        ta, hf, vf, pal = tmap[t]
        hf ^= (e >> 10) & 1
        vf ^= (e >> 11) & 1
        mt[idx] = ta | hf << 10 | vf << 11 | pal << 12
    sec.metatiles = mt
    return missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("layout")
    ap.add_argument("--secondary")
    ap.add_argument("--remap", action="store_true")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    rm.read_fieldmap_constants()
    symbols = rm.scan_tileset_symbols()
    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    lay = next(l for l in layouts if l.get("id") == args.layout)
    prim = rm.Tileset(rm.resolve_tileset("aethos", symbols))
    sec = rm.Tileset(rm.resolve_tileset(args.secondary or lay["secondary_tileset"], symbols))
    if args.remap:
        missing = remap_secondary(sec)
        if missing:
            print(f"note: {len(missing)} General tiles have no aethos match; left as is")
    r = rm.Renderer(prim, sec)
    blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2")
    img = rm.render_blocks(r, blocks, lay["width"])
    if args.scale > 1:
        img = img.resize((img.width * args.scale, img.height * args.scale), Image.NEAREST)
    out = Path(args.out) if args.out else ROOT / "build/render" / f"aethos_{args.layout.lower()}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
