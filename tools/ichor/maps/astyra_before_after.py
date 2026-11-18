#!/usr/bin/env python3
"""Before-and-after sheets for the awe pass's Astyra maps.

The "before" renders are the maps as they were at zach-main ee551c1d07, read
from git and drawn with render_map.py; the "after" are the current layouts.
Writes design/awe/img/<map>_before_after.png (whole maps side by side at 1x)
and <map>_screens.png (15 x 10 GBA screens, before above after, at 2x).

    /usr/bin/python3 tools/ichor/maps/astyra_before_after.py
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "design/awe/img"
BEFORE = "ee551c1d07"
MAPS = {
    "Astyra": ("kalliste", [(7, 33), (14, 21), (24, 14), (25, 5), (38, 15), (25, 40)]),
    "Astyra_Akropolis": ("kalliste", [(22, 50), (19, 37), (19, 26), (14, 18), (32, 10), (18, 8)]),
    "Astyra_Harbor": ("kalliste", [(24, 6), (12, 12), (24, 14)]),
}


def git_show(rev, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"], capture_output=True,
                          check=True).stdout


def render(bin_path, w, secondary, out, scale=1):
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(bin_path),
                    "--width", str(w), "--primary", "data/tilesets/primary/aethos", "--secondary",
                    f"data/tilesets/secondary/{secondary}", "--scale", str(scale), "-o", str(out)],
                   check=True, stdout=subprocess.DEVNULL)


def screens(im, views, c):
    crops = []
    for (px, py) in views:
        x0, y0 = max(0, (px - 7) * c), max(0, (py - 4) * c)
        crops.append(im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)))
    return crops


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "build/awe_before"
    tmp.mkdir(parents=True, exist_ok=True)
    lay_old = json.loads(git_show(BEFORE, "data/layouts/layouts.json"))
    lay_new = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    for name, (old_sec, views) in MAPS.items():
        lo = next(e for e in lay_old["layouts"] if e.get("blockdata_filepath") == f"data/layouts/{name}/map.bin")
        ln = next(e for e in lay_new["layouts"] if e.get("blockdata_filepath") == f"data/layouts/{name}/map.bin")
        ob = tmp / f"{name}_before.bin"
        ob.write_bytes(git_show(BEFORE, f"data/layouts/{name}/map.bin"))
        nb = ROOT / f"data/layouts/{name}/map.bin"
        sec_new = ln["secondary_tileset"].replace("gTileset_", "").lower()
        for scale in (1, 2):
            render(ob, lo["width"], old_sec, tmp / f"{name}_before_{scale}x.png", scale)
            render(nb, ln["width"], sec_new, tmp / f"{name}_after_{scale}x.png", scale)
        b1 = Image.open(tmp / f"{name}_before_1x.png").convert("RGB")
        a1 = Image.open(tmp / f"{name}_after_1x.png").convert("RGB")
        b1.save(OUT / f"{name.lower()}_before_1x.png")
        sheet = Image.new("RGB", (b1.width + a1.width + 30, max(b1.height, a1.height) + 24), (24, 24, 32))
        d = ImageDraw.Draw(sheet)
        d.text((10, 4), "before (ee551c1d07)", fill=(230, 230, 200))
        d.text((b1.width + 20, 4), "after (the awe pass)", fill=(230, 230, 200))
        sheet.paste(b1, (10, 20))
        sheet.paste(a1, (b1.width + 20, 20))
        sheet.save(OUT / f"{name.lower()}_before_after.png")
        b2 = Image.open(tmp / f"{name}_before_2x.png").convert("RGB")
        a2 = Image.open(tmp / f"{name}_after_2x.png").convert("RGB")
        cb, ca = screens(b2, views, 32), screens(a2, views, 32)
        W = len(views) * (15 * 32 + 8)
        sh = Image.new("RGB", (W, 2 * 10 * 32 + 30), (24, 24, 32))
        for i, (x, y) in enumerate(zip(cb, ca)):
            sh.paste(x, (i * (15 * 32 + 8), 0))
            sh.paste(y, (i * (15 * 32 + 8), 10 * 32 + 30))
        ImageDraw.Draw(sh).text((4, 10 * 32 + 8), "above: before; below: after (15 x 10 screens, 2x)",
                                fill=(230, 230, 200))
        sh.save(OUT / f"{name.lower()}_screens.png")
        print(OUT / f"{name.lower()}_before_after.png", OUT / f"{name.lower()}_screens.png")


if __name__ == "__main__":
    main()
