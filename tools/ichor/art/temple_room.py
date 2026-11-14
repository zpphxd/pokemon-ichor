#!/usr/bin/env python3
"""Build, check and show the Temple of Hestia tileset in its room.

1. Draws the tileset (temple_hestia.py) and compiles it with Porytiles.
2. Checks the compiled metatiles: every tile is the temple's own (or the
   transparent tile 0 in an upper layer) and every palette is 6-12.
3. Renders the Hearth Trial room, as designed in tools/ichor/maps/temple.py,
   cold and after the trial, with tools/ichor/render_map.py on the building
   primary and on aethos. The two renders must match pixel for pixel, which
   shows the temple works on any primary.

Writes, in design/phase1/img/:
  temple_room.png      the room at 3x, braziers cold, the dais closed
  temple_room_lit.png  the same room after the trial
  temple_identity.png  building and aethos renders side by side, and the diff
  temple_sheet.png     every metatile with its id, from the compiled tileset

Usage: /usr/bin/python3 tools/ichor/art/temple_room.py [--skip-compile]
  --skip-compile renders what is already compiled.
The map's own layout files are written by tools/ichor/maps/temple.py.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import temple_hestia  # noqa: E402

BIN = ROOT / "data/tilesets/secondary/temple_hestia/porytiles_bin"
IMG = ROOT / "design/phase1/img"
BUILD = ROOT / "build/render"
PY = sys.executable

# The room itself lives with the map (tools/ichor/maps/temple.py).
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
import temple  # noqa: E402


def blockdata(grid, ids):
    return np.array([ids[name] for row in grid for name in row], "<u2")


# --- Compile and check --------------------------------------------------------------

def compile_tileset():
    subprocess.run([PY, str(HERE / "temple_hestia.py")], check=True)
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.local/bin:/opt/homebrew/bin:" + env.get("PATH", "")
    # aethos's Porytiles cache is stale (its sources were repainted after its
    # last compile), so checksum verification has to be off to pair with it.
    r = subprocess.run(["porytiles", "compile-tileset", "--no-verify-checksums",
                        "gTileset_TempleHestia"], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        sys.exit("porytiles failed:\n" + r.stdout + r.stderr)


def check_compiled():
    mt = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    idx, pal = mt & 0x3FF, mt >> 12
    errors = []
    for n in range(len(mt)):
        for k in range(8):
            if idx[n, k] >= 512:
                if not 6 <= pal[n, k] <= 12:
                    errors.append(f"metatile {0x200 + n:#x} entry {k} uses palette {pal[n, k]}")
            elif idx[n, k] != 0:
                errors.append(f"metatile {0x200 + n:#x} entry {k} uses primary tile {idx[n, k]}")
            elif k < 4:
                errors.append(f"metatile {0x200 + n:#x} has a transparent first layer")
    tiles = Image.open(BIN / "tiles.png").size
    count = tiles[0] // 8 * tiles[1] // 8
    if errors:
        sys.exit("temple_room: compiled tileset is not self-contained:\n  " + "\n  ".join(errors[:20]))
    return len(mt), count


# --- Render ---------------------------------------------------------------------------

def render(blocks_path, width, primary, out):
    subprocess.run([PY, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(blocks_path),
                    "--width", str(width), "--primary", primary, "--secondary", "temple_hestia",
                    "-o", str(out)], check=True, capture_output=True)
    return np.array(Image.open(out).convert("RGB"))


def scaled(a, s):
    return Image.fromarray(a).resize((a.shape[1] * s, a.shape[0] * s), Image.NEAREST)


def identity_image(a, b):
    diff = np.any(a != b, axis=2)
    pad, s = 12, 2
    font = ImageFont.load_default(size=14)
    h, w = a.shape[0] * s, a.shape[1] * s
    img = Image.new("RGB", (3 * w + 4 * pad, h + 3 * pad + 18), (40, 40, 48))
    d = ImageDraw.Draw(img)
    vis = np.zeros_like(a)
    vis[diff] = (255, 0, 0)
    vis[~diff] = (a[~diff] // 3)
    for i, (label, arr) in enumerate((("--primary building", a), ("--primary aethos", b),
                                      (f"differing pixels: {int(diff.sum())}", vis))):
        x = pad + i * (w + pad)
        d.text((x, pad), label, fill=(230, 230, 200), font=font)
        img.paste(scaled(arr, s), (x, 2 * pad + 18))
    return img, int(diff.sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skip-compile", action="store_true")
    args = ap.parse_args()

    if not args.skip_compile:
        compile_tileset()
    n_meta, n_tiles = check_compiled()
    ids = temple_hestia.catalog()
    grid = temple.names_grid()
    width, height = len(grid[0]), len(grid)

    BUILD.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    cold, lit = BUILD / "temple_room.bin", BUILD / "temple_room_lit.bin"
    blockdata(grid, ids).tofile(cold)
    blockdata(temple.staged(grid, solved=True), ids).tofile(lit)

    a = render(cold, width, "building", BUILD / "temple_room_building.png")
    b = render(cold, width, "aethos", BUILD / "temple_room_aethos.png")
    la = render(lit, width, "building", BUILD / "temple_room_lit_building.png")
    lb = render(lit, width, "aethos", BUILD / "temple_room_lit_aethos.png")
    scaled(a, 3).save(IMG / "temple_room.png")
    scaled(la, 3).save(IMG / "temple_room_lit.png")
    ident, ndiff = identity_image(a, b)
    ident.save(IMG / "temple_identity.png")
    ndiff_lit = int(np.any(la != lb, axis=2).sum())

    subprocess.run([PY, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "temple_hestia",
                    "--primary", "building", "--scale", "3", "-o", str(IMG / "temple_sheet.png")],
                   check=True, capture_output=True)

    print(f"temple_room: {n_meta} metatiles, {n_tiles}/512 tiles; room {width}x{height}")
    print(f"identity: cold room {ndiff} px differ, lit room {ndiff_lit} px differ "
          f"(building vs aethos)")
    if ndiff or ndiff_lit:
        sys.exit("temple_room: the renders differ between primaries")


if __name__ == "__main__":
    main()
