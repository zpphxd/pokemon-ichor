#!/usr/bin/env python3
"""Trophonios's cave: two field objects in the Ichor cast palette.

  cobweb         16 x 16  a web stretched across a passage, for
                          EventScript_IchorCobweb (ENGINE_API section 2:
                          "any sprite; a web sprite is coming")
  great_boulder  32 x 32  a great boulder jammed in a niche's mouth, for
                          EventScript_IchorGreatBoulder (Hephaestus's Hammer).
                          A 32-wide object is centred on its tile, so it
                          overlaps half a tile either side: it reads as a rock
                          wedged between the niche's jambs.

Both load under OBJ_EVENT_PAL_TAG_ICHOR_CAST, so they cost no extra palette
on a map that shows the cast. --write writes the PNGs and registers them
(appended entries before each "End of Ichor object events" marker), as
design/phase1/SPRITES_npc.md describes.

Usage: /usr/bin/python3 tools/ichor/art/trophonios_objects.py [--write] [--preview PNG]
"""
from __future__ import annotations

import math
import os
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale  # noqa: E402
from sprites_npc import CAST_PAL  # noqa: E402

OUT_DIR = Path(ROOT) / "graphics/object_events/pics/misc/ichor"


def cobweb():
    """Threads from the passage's four corners to a small hub, two sparse rings."""
    a = np.zeros((16, 16), np.int32)
    L, D, S = CAST_PAL["linen_l"], CAST_PAL["linen_d"], CAST_PAL["slate"]
    cx, cy = 7.5, 6.5

    def line(x0, y0, x1, y1, c, every=1):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for i in range(n + 1):
            x = int(round(x0 + (x1 - x0) * i / n))
            y = int(round(y0 + (y1 - y0) * i / n))
            if 0 <= x < 16 and 0 <= y < 16 and i % every == 0:
                a[y, x] = c
    for (x, y) in ((0, 0), (15, 0), (0, 13), (15, 13), (7.5, 0), (0, 6), (15, 6.5), (6, 14)):
        line(cx, cy, x, y, L)
    for rr, c in ((2.2, L), (4.6, D)):
        pts = []
        for k in range(9):
            t = 2 * math.pi * k / 8 + 0.2
            pts.append((cx + math.cos(t) * rr * 1.15, cy + math.sin(t) * rr))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            line(x0, y0, x1, y1, c)
    # its shadow on the floor
    for x in range(3, 13):
        if a[15, x] == 0 and x % 2:
            a[15, x] = S
    return a


def great_boulder():
    """A faceted round boulder, lit from the top left, wedged in a niche."""
    a = np.zeros((32, 32), np.int32)
    ink, br, um, ld, ll, sl = (CAST_PAL[n] for n in ("ink", "brown", "umber", "linen_d", "linen_l", "slate"))
    yy, xx = np.mgrid[0:32, 0:32]
    cx, cy = 15.5, 18.0
    ang = np.arctan2(yy - cy, xx - cx)
    rad = 13.5 + 1.2 * np.sin(ang * 3 + 0.5) + 0.8 * np.sin(ang * 5 + 1.3)
    d = np.hypot((xx - cx), (yy - cy) * 1.08)
    m = d <= rad
    m[31, :] = False
    # facets: nearest of a few seeds; each facet has its own tilt
    seeds = [(10, 10, -1.0), (19, 9, -0.55), (25, 15, 0.1), (8, 19, -0.35), (16, 17, -0.1),
             (23, 24, 0.7), (12, 26, 0.45), (5, 12, -0.8)]
    best = np.full((32, 32), 1e9)
    tilt = np.zeros((32, 32))
    for sx, sy, tv in seeds:
        dd = (xx - sx) ** 2 + (yy - sy) ** 2
        sel = dd < best
        best[sel] = dd[sel]
        tilt[sel] = tv
    shade = tilt + ((xx - cx) * 0.25 + (yy - cy) * 0.6) / 14.0
    for y, x in np.argwhere(m):
        s = shade[y, x]
        dither = ((x + y) % 2) * 0.12
        s += dither
        c = ll if s < -0.85 else (ld if s < -0.3 else (um if s < 0.35 else (br if s < 0.85 else sl)))
        a[y, x] = c
    # facet edges: a darker line where two facets meet
    for y in range(1, 31):
        for x in range(1, 31):
            if m[y, x] and m[y, x + 1] and tilt[y, x] != tilt[y, x + 1] and (x + y) % 3:
                a[y, x] = br if a[y, x] in (ll, ld) else a[y, x]
            if m[y, x] and m[y + 1, x] and tilt[y, x] != tilt[y + 1, x] and (x * 2 + y) % 3:
                a[y, x] = br if a[y, x] in (ll, ld, um) else a[y, x]
    p = np.pad(m, 1)
    edge = m & ~(p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])
    a[edge] = ink
    return a


OBJECTS = {
    "cobweb": {"arr": cobweb, "w": 16, "h": 16, "const": "OBJ_EVENT_GFX_ICHOR_COBWEB",
               "sym": "IchorCobweb"},
    "great_boulder": {"arr": great_boulder, "w": 32, "h": 32, "const": "OBJ_EVENT_GFX_ICHOR_GREAT_BOULDER",
                      "sym": "IchorGreatBoulder"},
}

MARK = "// End of Ichor object events"


def insert_before(path, marker, text, key):
    p = Path(ROOT) / path
    t = p.read_text()
    if key in t:
        return
    i = t.index(marker)
    # keep the marker's indentation
    line_start = t.rfind("\n", 0, i) + 1
    t = t[:line_start] + text + t[line_start:]
    p.write_text(t)


def register():
    for name, o in OBJECTS.items():
        sym, const, w, h = o["sym"], o["const"], o["w"], o["h"]
        insert_before("include/constants/event_objects.h", MARK,
                      f"    {const},  // Trophonios's cave (tools/ichor/art/trophonios_objects.py)\n", const + ",")
        insert_before("src/data/object_events/object_event_graphics.h", MARK,
                      f'const u32 gObjectEventPic_{sym}[] = INCGFX_U32("graphics/object_events/pics/misc/ichor/{name}.png", ".4bpp");\n',
                      f"gObjectEventPic_{sym}[]")
        insert_before("src/data/object_events/object_event_pic_tables.h", MARK,
                      f"static const struct SpriteFrameImage sPicTable_{sym}[] = {{\n"
                      f"    obj_frame_tiles(gObjectEventPic_{sym}),\n}};\n",
                      f"sPicTable_{sym}[]")
        size = w * h // 2
        insert_before("src/data/object_events/object_event_graphics_info.h", MARK,
                      f"// Trophonios's cave: a {w}x{h} field object (tools/ichor/art/trophonios_objects.py).\n"
                      f"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{sym} = {{\n"
                      "    .tileTag = TAG_NONE,\n"
                      "    .paletteTag = OBJ_EVENT_PAL_TAG_ICHOR_CAST,\n"
                      "    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n"
                      f"    .size = {size},\n"
                      f"    .width = {w},\n"
                      f"    .height = {h},\n"
                      "    .paletteSlot = PALSLOT_NPC_SPECIAL,\n"
                      f"    .shadowSize = {'SHADOW_SIZE_S' if w == 16 else 'SHADOW_SIZE_M'},\n"
                      "    .inanimate = TRUE,\n"
                      "    .compressed = FALSE,\n"
                      "    .tracks = TRACKS_NONE,\n"
                      f"    .oam = &gObjectEventBaseOam_{w}x{h},\n"
                      f"    .subspriteTables = sOamTables_{w}x{h},\n"
                      "    .anims = sAnimTable_Inanimate,\n"
                      f"    .images = sPicTable_{sym},\n"
                      "};\n",
                      f"gObjectEventGraphicsInfo_{sym} =")
        ptr = "src/data/object_events/object_event_graphics_info_pointers.h"
        t = (Path(ROOT) / ptr).read_text()
        first = t.index(MARK)
        if f"extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{sym};" not in t:
            line_start = t.rfind("\n", 0, first) + 1
            t = t[:line_start] + f"extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{sym};\n" + t[line_start:]
        if f"[{const}]" not in t:
            second = t.index(MARK, t.index(MARK) + len(MARK))
            line_start = t.rfind("\n", 0, second) + 1
            t = t[:line_start] + f"    [{const}] = &gObjectEventGraphicsInfo_{sym},\n" + t[line_start:]
        (Path(ROOT) / ptr).write_text(t)


def main():
    args = sys.argv[1:]
    arrs = {n: o["arr"]() for n, o in OBJECTS.items()}
    if "--write" in args:
        for n, arr in arrs.items():
            save_indexed(arr, CAST_PAL, str(OUT_DIR / f"{n}.png"))
        register()
    if "--preview" in args:
        from PIL import Image
        out = Image.new("RGBA", (80, 32), (88, 72, 64, 255))
        x = 0
        for n, arr in arrs.items():
            out.alpha_composite(to_rgba(arr, CAST_PAL), (x, 32 - arr.shape[0]))
            x += arr.shape[1] + 8
        upscale(out, 6).save(args[args.index("--preview") + 1])


if __name__ == "__main__":
    main()
