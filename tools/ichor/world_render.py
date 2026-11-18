#!/usr/bin/env python3
"""Render the whole overworld: every map joined to others by connections,
stitched at its real offsets, one island (connected group) per block.

  /usr/bin/python3 tools/ichor/world_render.py [-o build/render/world.png] [--labels]

Writes the full-size image (16 px per tile) and a half-size copy beside it.
"""
import argparse
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map as rm  # noqa: E402

Image.MAX_IMAGE_PIXELS = None


def load_maps():
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
    layouts = {l["id"]: l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"] if "id" in l}
    maps = {}
    for g in groups["group_order"]:
        for name in groups[g]:
            p = ROOT / "data/maps" / name / "map.json"
            if not p.exists():
                continue
            d = json.loads(p.read_text())
            lay = layouts.get(d.get("layout"))
            if not lay or "blockdata_filepath" not in lay:
                continue
            maps[d["id"]] = {"name": name, "json": d, "layout": lay}
    return maps


def islands(maps):
    """Connected groups of maps, each with tile positions from the connections."""
    seen, out = set(), []
    for start in maps:
        conns = maps[start]["json"].get("connections") or []
        if start in seen or not conns:
            continue
        pos = {start: (0, 0)}
        q = deque([start])
        seen.add(start)
        while q:
            m = q.popleft()
            x, y = pos[m]
            w, h = maps[m]["layout"]["width"], maps[m]["layout"]["height"]
            for c in maps[m]["json"].get("connections") or []:
                n, off, d = c["map"], c["offset"], c["direction"]
                if n not in maps or n in pos:
                    continue
                nw, nh = maps[n]["layout"]["width"], maps[n]["layout"]["height"]
                if d == "up":
                    pos[n] = (x + off, y - nh)
                elif d == "down":
                    pos[n] = (x + off, y + h)
                elif d == "left":
                    pos[n] = (x - nw, y + off)
                elif d == "right":
                    pos[n] = (x + w, y + off)
                else:
                    continue
                seen.add(n)
                q.append(n)
        out.append(pos)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-o", "--out", default=str(ROOT / "build/render/world.png"))
    ap.add_argument("--labels", action="store_true", help="write each map's name on it")
    args = ap.parse_args()

    rm.read_fieldmap_constants()
    symbols = rm.scan_tileset_symbols()
    maps = load_maps()
    groups = sorted(islands(maps), key=len, reverse=True)

    cache = {}

    def render(mid):
        lay = maps[mid]["layout"]
        key = (lay["primary_tileset"], lay["secondary_tileset"])
        if key not in cache:
            cache[key] = rm.Renderer(rm.Tileset(rm.resolve_tileset(key[0], symbols)),
                                     rm.Tileset(rm.resolve_tileset(key[1], symbols)))
        blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2")
        return rm.render_blocks(cache[key], blocks, lay["width"]).convert("RGB")

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
    except OSError:
        font = ImageFont.load_default()

    blocks = []
    for pos in groups:
        minx = min(x for x, _ in pos.values())
        miny = min(y for _, y in pos.values())
        maxx = max(x + maps[m]["layout"]["width"] for m, (x, _) in pos.items())
        maxy = max(y + maps[m]["layout"]["height"] for m, (_, y) in pos.items())
        img = Image.new("RGB", ((maxx - minx) * 16, (maxy - miny) * 16), (18, 32, 48))
        draw = ImageDraw.Draw(img)
        for m, (x, y) in pos.items():
            img.paste(render(m), ((x - minx) * 16, (y - miny) * 16))
        if args.labels:
            for m, (x, y) in pos.items():
                draw.text(((x - minx) * 16 + 12, (y - miny) * 16 + 8), maps[m]["name"],
                          fill=(255, 255, 255), font=font, stroke_width=4, stroke_fill=(0, 0, 0))
        blocks.append((img, len(pos)))
        print(f"island of {len(pos)} maps: {img.width // 16}x{img.height // 16} tiles")

    # Lay the islands out left to right, wrapping at a sensible width.
    pad, maxw = 64, max(b.width for b, _ in blocks) * 2
    rows, row, w = [], [], 0
    for b, n in blocks:
        if row and w + b.width > maxw:
            rows.append(row)
            row, w = [], 0
        row.append(b)
        w += b.width + pad
    rows.append(row)
    W = max(sum(b.width for b in r) + pad * (len(r) + 1) for r in rows)
    H = sum(max(b.height for b in r) for r in rows) + pad * (len(rows) + 1)
    world = Image.new("RGB", (W, H), (18, 32, 48))
    y = pad
    for r in rows:
        x = pad
        for b in r:
            world.paste(b, (x, y))
            x += b.width + pad
        y += max(b.height for b in r) + pad
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    world.save(out)
    half = world.resize((world.width // 2, world.height // 2), Image.LANCZOS)
    half.save(out.with_name(out.stem + "_half.png"))
    print(f"{out} {world.width}x{world.height}")


if __name__ == "__main__":
    main()
