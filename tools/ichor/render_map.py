#!/usr/bin/env python3
"""Render a map layout, or a numbered metatile sheet, to PNG.

Reads the same files the game does: the layout's map.bin from
data/layouts/layouts.json, and each tileset's tiles.png, palettes/*.pal and
metatiles.bin (found through src/data/tilesets/*.h, or by directory name).
Both metatile layers are drawn with their flips and palettes, and color 0 shows
the backdrop (primary palette 0, color 0) exactly as on hardware.

Usage:
  tools/ichor/render_map.py LAYOUT_LITTLEROOT_TOWN
  tools/ichor/render_map.py LAYOUT_ROUTE101 --primary aethos --secondary kalliste --scale 3
  tools/ichor/render_map.py --sheet kalliste --primary aethos --scale 2
  tools/ichor/render_map.py --blockdata scene.bin --width 24 --primary aethos --secondary kalliste

Tilesets can be named by symbol (gTileset_General), directory name (general)
or path (data/tilesets/primary/general). Needs Pillow and numpy; macOS's
/usr/bin/python3 has both.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
TILES_PER_METATILE = 8
SHEET_COLS = 8


def read_fieldmap_constants():
    global NUM_TILES_IN_PRIMARY, NUM_METATILES_IN_PRIMARY, NUM_PALS_IN_PRIMARY, TILES_PER_METATILE
    text = (ROOT / "include/fieldmap.h").read_text()
    def const(name, default):
        m = re.search(rf"#define {name} (\d+)\b", text)
        return int(m.group(1)) if m else default
    NUM_TILES_IN_PRIMARY = const("NUM_TILES_IN_PRIMARY", 512)
    NUM_METATILES_IN_PRIMARY = const("NUM_METATILES_IN_PRIMARY", 512)
    NUM_PALS_IN_PRIMARY = const("NUM_PALS_IN_PRIMARY", 6)
    TILES_PER_METATILE = const("NUM_TILES_PER_METATILE", 8)


# --- tileset lookup -------------------------------------------------------

def scan_tileset_symbols():
    """Map gTileset_* symbols to their tiles, palette and metatile files."""
    src = ROOT / "src"
    headers = (src / "data/tilesets/headers.h").read_text()
    gfx = (src / "data/tilesets/graphics.h").read_text() + (src / "graphics.c").read_text()
    metas = (src / "data/tilesets/metatiles.h").read_text()

    # Vanilla tilesets use INCGFX on the source PNG/PAL; Porytiles-managed ones
    # INCBIN the built .4bpp.lz/.gbapal, which sit next to the source files.
    def source(path):
        return re.sub(r"\.4bpp(\.lz)?$", ".png", re.sub(r"\.gbapal$", ".pal", path))
    tiles = {n: source(p) for n, p in re.findall(r'(gTilesetTiles_\w+)\[\]\s*=\s*INC(?:GFX|BIN)_U32\("([^"]+)"', gfx)}
    pals = {}
    for name, body in re.findall(r'(gTilesetPalettes_\w+)\[\]\[16\]\s*=\s*\{(.*?)\};', gfx, re.S):
        pals[name] = [source(p) for p in re.findall(r'INC(?:GFX|BIN)_U16\("([^"]+)"', body)]
    metatiles = dict(re.findall(r'(gMetatiles_\w+)\[\]\s*=\s*INCBIN_U16\("([^"]+)"', metas))

    out = {}
    for name, body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\};', headers, re.S):
        fields = dict(re.findall(r'\.(\w+)\s*=\s*(\w+)', body))
        try:
            out[name] = {
                "secondary": fields.get("isSecondary") == "TRUE",
                "tiles": ROOT / tiles[fields["tiles"]],
                "palettes": [ROOT / p for p in pals[fields["palettes"]]],
                "metatiles": ROOT / metatiles[fields["metatiles"]],
            }
        except KeyError:
            continue
    return out


def tileset_name(info):
    """Directory name of a tileset, e.g. 'general' or 'aethos'."""
    d = info["tiles"].parent
    return d.parent.name if d.name == "porytiles_bin" else d.name


def tileset_from_dir(d):
    d = Path(d)
    if (d / "porytiles_bin").is_dir():
        d = d / "porytiles_bin"
        return {
            "secondary": d.parent.parent.name == "secondary",
            "tiles": d / "tiles.png",
            "palettes": [d / "palettes" / f"{i:02d}.pal" for i in range(16)],
            "metatiles": d / "metatiles.bin",
        }
    return {
        "secondary": d.parent.name == "secondary",
        "tiles": d / "tiles.png",
        "palettes": [d / "palettes" / f"{i:02d}.pal" for i in range(16)],
        "metatiles": d / "metatiles.bin",
    }


def resolve_tileset(name, symbols):
    if name in symbols:
        return symbols[name]
    p = Path(name)
    if not p.is_absolute():
        p = ROOT / p
    if (p / "metatiles.bin").exists() or (p / "porytiles_bin" / "metatiles.bin").exists():
        return tileset_from_dir(p)
    # A bare directory name: prefer the registered symbol that points at it.
    for info in symbols.values():
        if tileset_name(info) == name:
            return info
    for kind in ("primary", "secondary"):
        d = ROOT / "data/tilesets" / kind / name
        if (d / "metatiles.bin").exists():
            return tileset_from_dir(d)
    sys.exit(f"render_map: unknown tileset '{name}'")


# --- loading --------------------------------------------------------------

def load_pal(path):
    colors = np.zeros((16, 3), np.uint8)
    if not path.exists():
        return colors
    lines = path.read_text().split()
    vals = [int(v) for v in lines[3:3 + 48]]
    for i in range(min(16, len(vals) // 3)):
        # Hardware keeps 5 bits per channel.
        colors[i] = [v & 0xF8 for v in vals[i * 3:i * 3 + 3]]
    return colors


def load_tiles(path):
    im = Image.open(path)
    if im.mode == "P":
        a = np.array(im, np.uint8) % 16
    elif im.mode == "L":
        a = (np.array(im, np.uint16) * 15 // 255).astype(np.uint8)
    else:
        sys.exit(f"render_map: {path} is not an indexed PNG")
    h, w = a.shape
    a = a[: h - h % 8, : w - w % 8]
    tiles = a.reshape(h // 8, 8, w // 8, 8).swapaxes(1, 2).reshape(-1, 8, 8)
    return tiles


class Tileset:
    def __init__(self, info):
        self.info = info
        self.tiles = load_tiles(info["tiles"])
        self.pals = [load_pal(p) for p in info["palettes"]]
        raw = np.fromfile(info["metatiles"], "<u2")
        self.metatiles = raw.reshape(-1, TILES_PER_METATILE)


class Renderer:
    def __init__(self, primary, secondary):
        self.p, self.s = primary, secondary
        pals = [self.p.pals[i] if i < NUM_PALS_IN_PRIMARY else self.s.pals[i] for i in range(16)]
        self.pals = np.stack(pals)
        self.backdrop = self.pals[0][0]
        self.cache = {}

    def tile(self, entry):
        """8x8 RGBA for one metatile entry (tile index, flips, palette)."""
        if entry in self.cache:
            return self.cache[entry]
        idx, hflip, vflip, pal = entry & 0x3FF, entry >> 10 & 1, entry >> 11 & 1, entry >> 12
        if idx < NUM_TILES_IN_PRIMARY:
            src = self.p.tiles[idx] if idx < len(self.p.tiles) else None
        else:
            j = idx - NUM_TILES_IN_PRIMARY
            src = self.s.tiles[j] if j < len(self.s.tiles) else None
        if src is None:
            src = np.zeros((8, 8), np.uint8)
        if hflip:
            src = src[:, ::-1]
        if vflip:
            src = src[::-1, :]
        rgba = np.zeros((8, 8, 4), np.uint8)
        rgba[..., :3] = self.pals[pal][src]
        rgba[..., 3] = np.where(src == 0, 0, 255)
        self.cache[entry] = rgba
        return rgba

    def metatile(self, mid):
        """16x16 RGB for a metatile id, both layers over the backdrop."""
        if mid < NUM_METATILES_IN_PRIMARY:
            table, j = self.p.metatiles, mid
        else:
            table, j = self.s.metatiles, mid - NUM_METATILES_IN_PRIMARY
        out = np.empty((16, 16, 3), np.uint8)
        out[:] = self.backdrop
        if j >= len(table):
            return out, False
        entries = table[j]
        for layer in range(TILES_PER_METATILE // 4):
            for k in range(4):
                t = self.tile(int(entries[layer * 4 + k]))
                y, x = (k // 2) * 8, (k % 2) * 8
                region = out[y:y + 8, x:x + 8]
                m = t[..., 3:] > 0
                region[:] = np.where(m, t[..., :3], region)
        return out, True


def render_blocks(r, blocks, width):
    height = len(blocks) // width
    img = np.zeros((height * 16, width * 16, 3), np.uint8)
    for i, b in enumerate(blocks[: width * height]):
        y, x = divmod(i, width)
        img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = r.metatile(int(b) & 0x3FF)[0]
    return Image.fromarray(img)


def render_sheet(r, first, count, scale):
    rows = (count + SHEET_COLS - 1) // SHEET_COLS
    cell = 16 * scale
    label_h = 10
    pad = 2
    W = SHEET_COLS * (cell + pad) + pad
    H = rows * (cell + label_h + pad) + pad
    sheet = Image.new("RGB", (W, H), (40, 40, 48))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=9)
    for n in range(count):
        mid = first + n
        tile, ok = r.metatile(mid)
        row, col = divmod(n, SHEET_COLS)
        x = pad + col * (cell + pad)
        y = pad + row * (cell + label_h + pad)
        sheet.paste(Image.fromarray(tile).resize((cell, cell), Image.NEAREST), (x, y + label_h))
        draw.text((x + 1, y), f"{mid:03X}", fill=(230, 230, 200) if ok else (110, 110, 110), font=font)
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("layout", nargs="?", help="layout id, e.g. LAYOUT_LITTLEROOT_TOWN")
    ap.add_argument("--primary", help="override the primary tileset")
    ap.add_argument("--secondary", help="override the secondary tileset")
    ap.add_argument("--scale", type=int, default=1)
    ap.add_argument("--sheet", metavar="TILESET", help="render a numbered metatile sheet instead")
    ap.add_argument("--range", help="sheet metatile range, e.g. 0x200-0x27F")
    ap.add_argument("--blockdata", help="render a raw map.bin instead of a layout (needs --width)")
    ap.add_argument("--width", type=int, help="blocks per row for --blockdata")
    ap.add_argument("-o", "--out", help="output PNG (default build/render/<name>.png)")
    args = ap.parse_args()

    read_fieldmap_constants()
    symbols = scan_tileset_symbols()

    if args.sheet:
        info = resolve_tileset(args.sheet, symbols)
        if info["secondary"]:
            prim = resolve_tileset(args.primary or "gTileset_General", symbols)
            sec = info
            base = NUM_METATILES_IN_PRIMARY
        else:
            prim = info
            sec = resolve_tileset(args.secondary or "gTileset_Petalburg", symbols)
            base = 0
        r = Renderer(Tileset(prim), Tileset(sec))
        count = len((r.s if info["secondary"] else r.p).metatiles)
        first, last = base, base + count - 1
        if args.range:
            a, b = args.range.split("-")
            first, last = max(first, int(a, 0)), min(last, int(b, 0))
        img = render_sheet(r, first, last - first + 1, max(1, args.scale))
        name = f"sheet_{tileset_name(info)}"
    else:
        if args.blockdata:
            if not args.width:
                sys.exit("render_map: --blockdata needs --width")
            prim = resolve_tileset(args.primary or "gTileset_General", symbols)
            sec = resolve_tileset(args.secondary or "gTileset_Petalburg", symbols)
            blocks, width = np.fromfile(args.blockdata, "<u2"), args.width
            name = Path(args.blockdata).stem
        else:
            if not args.layout:
                ap.error("give a layout id, --sheet or --blockdata")
            layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
            lay = next((l for l in layouts if l.get("id") == args.layout or l.get("name") == args.layout), None)
            if not lay:
                sys.exit(f"render_map: no layout {args.layout}")
            prim = resolve_tileset(args.primary or lay["primary_tileset"], symbols)
            sec = resolve_tileset(args.secondary or lay["secondary_tileset"], symbols)
            blocks, width = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2"), lay["width"]
            name = args.layout.lower().removeprefix("layout_")
        r = Renderer(Tileset(prim), Tileset(sec))
        img = render_blocks(r, blocks, width)
        if args.scale > 1:
            img = img.resize((img.width * args.scale, img.height * args.scale), Image.NEAREST)

    out = Path(args.out) if args.out else ROOT / "build/render" / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
