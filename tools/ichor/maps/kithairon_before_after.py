#!/usr/bin/env python3
"""The polish pass's before/after sheet for the Kithairon crossing:
design/phase3/img/kithairon_polish_before_after.png.

Each map's batch 1 render (from git, the commit the polish pass started on) beside
its render now (design/phase3/img/<Map>.png), at 1x, labelled; Route 7 at the top,
as the maps run north to south.

  /usr/bin/python3 tools/ichor/maps/kithairon_before_after.py [--base <commit>]
"""
from __future__ import annotations

import argparse
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
IMG = ROOT / "design/phase3/img"
BASE = "07dddca1556ef23b300e172fa3d17682acf83ecc"   # batch 1's crossing, before the polish pass
MAPS = [("Route7_KroniaGrounds", "Route 7, the Kronia grounds"),
        ("MtKithairon", "Mt. Kithairon"),
        ("Eleutherai", "Eleutherai"),
        ("Route6_EleutheraiRoad", "Route 6, the Eleutherai Road"),
        ("Route6_AntiopesCave", "Antiope's cave")]
BG, FG, PAD, HEAD = (24, 24, 32), (232, 232, 216), 12, 26


def old(base, folder):
    data = subprocess.run(["git", "show", f"{base}:design/phase3/img/{folder}.png"], cwd=ROOT,
                          capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data)).convert("RGB")


def half(im):
    return im.resize((im.width // 2, im.height // 2), Image.NEAREST)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=BASE)
    args = ap.parse_args()
    font = ImageFont.load_default(size=16)
    rows = []
    for folder, title in MAPS:
        a, b = half(old(args.base, folder)), half(Image.open(IMG / f"{folder}.png").convert("RGB"))
        rows.append((title, a, b))
    colw = max(max(a.width, b.width) for _, a, b in rows)
    w = PAD * 3 + colw * 2
    h = PAD + HEAD + sum(HEAD + max(a.height, b.height) + PAD for _, a, b in rows)
    sheet = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(sheet)
    d.text((PAD, PAD), "Before: batch 1", fill=FG, font=font)
    d.text((PAD * 2 + colw, PAD), "After: the polish pass", fill=FG, font=font)
    y = PAD + HEAD
    for title, a, b in rows:
        d.text((PAD, y), title, fill=FG, font=font)
        y += HEAD
        sheet.paste(a, (PAD, y))
        sheet.paste(b, (PAD * 2 + colw, y))
        y += max(a.height, b.height) + PAD
    out = IMG / "kithairon_polish_before_after.png"
    sheet.save(out)
    print(out.relative_to(ROOT), sheet.size)


if __name__ == "__main__":
    main()
