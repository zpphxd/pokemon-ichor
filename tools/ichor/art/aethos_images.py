#!/usr/bin/env python3
"""Regenerate aethos's review images in design/phase1/img/.

  aethos_route101.png    LAYOUT_ROUTE101 on aethos, 2x
  aethos_littleroot.png  LAYOUT_LITTLEROOT_TOWN on aethos + petalburg, 2x
                         (raw: Petalburg's tile references are pinned)
  aethos_village.png     a mock village block built only from aethos
                         metatiles (throwaway block data, not a map), 2x
  aethos_coast.png       part of LAYOUT_ROUTE109 on aethos, 2x (Slateport's
                         own primary references remapped, see aethos_review)
  aethos_sheet.png       the numbered metatile sheet, 2x
  aethos_anims.png       every animation, key frame first, 3x

Usage: /usr/bin/python3 tools/ichor/art/aethos_images.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
IMG = ROOT / "design/phase1/img"
PY = sys.executable
RENDER = ROOT / "tools/ichor/render_map.py"
REVIEW = ROOT / "tools/ichor/art/aethos_review.py"

VILLAGE = """
1CE 1CF 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 001 1CE 1CF
1D4 1D5 00E 001 001 001 001 048 049 04A 04B 001 001 028 029 029 02B 001 001 00E 01E 01F 1D4 1D5
1DC 1DD 016 001 001 001 001 050 051 052 053 001 001 030 031 032 033 001 001 016 026 027 1DC 1DD
1D4 1D5 004 004 001 001 001 058 059 05A 05B 001 001 038 039 03A 03B 001 001 001 001 001 1D4 1D5
1E4 1E5 004 001 001 003 001 060 061 062 063 001 001 060 041 042 043 001 01B 001 001 001 1DC 1DD
001 001 001 001 1D0 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D1 1D2 001 001 1D4 1D5
1CE 1CF 001 001 1D8 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1D9 1DA 001 0E0 1E4 1E5
1D4 1D5 001 001 1E0 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E1 1E2 001 001 001 001
1E4 1E5 148 149 149 149 14A 001 001 008 009 00A 001 00D 00D 00D 00D 00D 001 001 004 001 001 001
001 001 001 004 001 001 001 001 001 010 011 012 001 00D 00D 00D 00D 00D 00D 001 001 001 001 001
001 001 001 001 001 001 001 001 001 018 019 01A 001 00D 00D 00D 00D 00D 00D 001 001 001 001 001
001 0D5 087 087 087 087 0D6 001 001 020 021 022 001 001 00D 00D 00D 001 001 001 001 001 001 001
124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124 124
12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C 12C
170 170 170 18C 170 170 170 170 170 170 170 170 170 170 170 170 170 18C 170 170 170 170 170 170
170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170 170
"""


def run(*args):
    r = subprocess.run([PY, *map(str, args)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout + r.stderr)


def anims(out, scale=3):
    base = ROOT / "data/tilesets/primary/aethos/porytiles_src/anim"
    rows = []
    for name in ("water", "sand_water_edge", "waterfall", "flower", "land_water_edge"):
        d = base / name
        names = ["key"] + sorted([p.stem for p in d.glob("*.png") if p.stem != "key"], key=int)
        rows.append((name, [Image.open(d / f"{n}.png").convert("RGBA") for n in names]))
    pad, lab = 6, 14
    W = max(sum(i.width * scale + pad for i in fr) for _, fr in rows) + pad
    H = sum(max(i.height for i in fr) * scale + lab + pad for _, fr in rows) + pad
    sheet = Image.new("RGB", (W, H), (40, 40, 48))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=11)
    y = pad
    for name, fr in rows:
        d.text((pad, y), f"{name}: key, then frames", fill=(230, 230, 200), font=font)
        x = pad
        for im in fr:
            bg = Image.new("RGBA", im.size, (24, 40, 80, 255))
            px = np.array(im)
            px[(px[..., :3] == (255, 0, 255)).all(-1)] = 0
            bg.alpha_composite(Image.fromarray(px))
            sheet.paste(bg.convert("RGB").resize((im.width * scale, im.height * scale), Image.NEAREST),
                        (x, y + lab))
            x += im.width * scale + pad
        y += max(i.height for i in fr) * scale + lab + pad
    sheet.save(out)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    run(RENDER, "LAYOUT_ROUTE101", "--primary", "aethos", "--scale", 2, "-o", IMG / "aethos_route101.png")
    run(RENDER, "LAYOUT_LITTLEROOT_TOWN", "--primary", "aethos", "--secondary", "petalburg",
        "--scale", 2, "-o", IMG / "aethos_littleroot.png")
    with tempfile.TemporaryDirectory() as tmp:
        rows = [r.split() for r in VILLAGE.strip().split("\n")]
        blocks = np.array([[int(v, 16) for v in r] for r in rows], np.uint16)
        bin_path = Path(tmp) / "aethos_village.bin"
        blocks.tofile(bin_path)
        run(RENDER, "--blockdata", bin_path, "--width", blocks.shape[1], "--primary", "aethos",
            "--secondary", "petalburg", "--scale", 2, "-o", IMG / "aethos_village.png")
        full = Path(tmp) / "r109.png"
        run(REVIEW, "LAYOUT_ROUTE109", "--remap", "--scale", 1, "-o", full)
        im = Image.open(full).crop((0, 400, 480, 720))
        im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(IMG / "aethos_coast.png")
    run(RENDER, "--sheet", "aethos", "--scale", 2, "-o", IMG / "aethos_sheet.png")
    anims(IMG / "aethos_anims.png")
    print("wrote", ", ".join(sorted(p.name for p in IMG.glob("aethos_*.png"))))


if __name__ == "__main__":
    main()
