#!/usr/bin/env python3
"""The whole climb of Mount Olympus on one sheet, in the order you walk it, each map
rendered with its people (design/maps/img/mount_olympus_full.png, and a copy in
playtest/ for the user).

Usage: /usr/bin/python3 tools/ichor/maps/olympus_composite.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
import render_map as R  # noqa: E402
import league_lib as L  # noqa: E402

CLIMB = [
    ("Ascent_1F", "1. The slopes"), ("Ascent_2F", "2. The cloud ledges (camp + herm)"),
    ("Ascent_Snowfield", "3. The Leuke snowfield (outdoors)"), ("Ascent_Icefall", "4. The Icefall"),
    ("Ascent_IcefallDeep", "5. The Icefall Deep"), ("Ascent_CrystalVault", "6. The Crystal Vault"),
    ("Ascent_Glacier", "7. The Glacier (outdoors)"), ("Ascent_WindRidge", "8. Boreas's ridge (outdoors)"),
    ("Ascent_3F", "9. Above the clouds: the Propylaia"), ("Olympus_Propylaia", "10. The Propylaia (lobby)"),
    ("Olympus_SeatOfAres", "11. Seat of Ares"), ("Olympus_SeatOfPoseidon", "12. Seat of Poseidon"),
    ("Olympus_SeatOfAthena", "13. Seat of Athena"), ("Olympus_SeatOfHera", "14. Seat of Hera"),
    ("Olympus_Summit", "15. The Summit (the Archon)"), ("Olympus_HallOfHeroes", "16. Hall of Heroes"),
]


def render(name):
    m = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    data = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    lay = next(l for l in data["layouts"] if l.get("id") == m["layout"])
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    r = R.Renderer(R.Tileset(R.resolve_tileset(lay["primary_tileset"], syms)),
                   R.Tileset(R.resolve_tileset(lay["secondary_tileset"], syms)))
    blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2")
    img = R.render_blocks(r, blocks, lay["width"]).convert("RGBA")
    for o in m.get("object_events", []):
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE_" in o["movement_type"] else "DOWN"
        try:
            spr, fw, fh = L._sprite(o["graphics_id"], facing)
        except (FileNotFoundError, OSError):
            continue
        img.alpha_composite(spr, (o["x"] * 16 + 8 - fw // 2, o["y"] * 16 + 16 - fh))
    return img.convert("RGB")


def main():
    ims = [(label, render(name)) for name, label in CLIMB]
    cols = 4
    cw = max(i.width for _, i in ims)
    rows = (len(ims) + cols - 1) // cols
    rh = [max(i.height for _, i in ims[r * cols:(r + 1) * cols]) + 28 for r in range(rows)]
    sheet = Image.new("RGB", (cols * (cw + 16) + 16, sum(rh) + 16), (22, 26, 36))
    d = ImageDraw.Draw(sheet)
    y = 8
    for r in range(rows):
        for c, (label, im) in enumerate(ims[r * cols:(r + 1) * cols]):
            x = 16 + c * (cw + 16)
            d.text((x, y), label, fill=(236, 226, 190))
            sheet.paste(im, (x, y + 18))
        y += rh[r]
    out = ROOT / "design/maps/img/mount_olympus_full.png"
    sheet.save(out)
    (ROOT / "playtest").mkdir(exist_ok=True)
    shutil.copy2(out, ROOT / "playtest/mount_olympus_full.png")
    print(out, sheet.size)


if __name__ == "__main__":
    main()
