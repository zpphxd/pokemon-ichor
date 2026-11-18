#!/usr/bin/env python3
"""Every town's travel herm: the great herm and its plaque at the main entrance.

design/SYSTEMS.md §4 and design/MAP_DESIGN.md §7: every town, hamlet and major
rest stop has a great herm a step or two from where the player arrives, with a
small plaque beside it that names it a travel herm. Touching the herm (or using
the town's Asclepeion or healer) registers it; any herm then carries the player
to any registered one.

This file is the source of truth for where each town's herm stands. It writes
two object events into each town's map.json (no metatiles change, so it works
on every tileset):

  the herm    OBJ_EVENT_GFX_ICHOR_GREAT_HERM, script EventScript_IchorTownHerm
  the plaque  OBJ_EVENT_GFX_ICHOR_HERM_PLAQUE, script EventScript_IchorTownHermSign

The engine's row for each town (map, landing tile, name) is in
src/data/ichor_town_herms.h; the landing tile here must match it, and
tools/ichor/herm_audit.py checks both (smoke_test.sh runs it).

Usage:
  /usr/bin/python3 tools/ichor/maps/town_herms.py              apply to every map.json
  /usr/bin/python3 tools/ichor/maps/town_herms.py --preview DIR
        render each town's entrance with the herm and plaque drawn in, gridded

Run it again after re-running a town's own generator, if that generator
rewrites map.json's object events. It is idempotent: it replaces its own two
objects and leaves every other event alone.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

HERM_GFX = "OBJ_EVENT_GFX_ICHOR_GREAT_HERM"
PLAQUE_GFX = "OBJ_EVENT_GFX_ICHOR_HERM_PLAQUE"
HERM_SCRIPT = "EventScript_IchorTownHerm"
PLAQUE_SCRIPT = "EventScript_IchorTownHermSign"

# map, herm (x, y), plaque (x, y), landing (x, y): where Hermes sets the
# traveler down, beside the herm on the main path. "arrives" names the
# entrance the herm greets. Keep the order and the landing tiles in step with
# src/data/ichor_town_herms.h.
TOWNS = [
    # map                 herm       plaque     landing    arrives
    ("ElaiaVillage",      (15, 2),   (14, 2),   (15, 3),   "the north gate, from Route 1"),
    ("AktiTown",          (14, 26),  (15, 26),  (13, 26),  "the south road, from Route 1"),
    ("AeginaTown",        (9, 11),   (8, 11),   (9, 12),   "the quay, from the Euploia"),
    ("EmporionCity",      (19, 42),  (18, 42),  (19, 41),  "the south gate, from the harbor"),
    ("EleusaVillage",     (5, 23),   (4, 23),   (5, 24),   "the west road, from Route 5"),
    ("ThyrsaCity",        (25, 41),  (24, 41),  (26, 41),  "the south gate, from Route 7"),
    ("Lebadeia",          (33, 16),  (32, 16),  (33, 17),  "the east road, from Route 8"),
    ("Kirrha",            (13, 2),   (12, 2),   (14, 2),   "the Sacred Way, from Route 9"),
    ("Aigion",            (17, 29),  (18, 29),  (16, 29),  "the south road, from Route 11"),
    ("StyxFalls",         (15, 12),  (16, 12),  (15, 13),  "the north pass, from Route 11"),
    ("Arkadia",           (21, 3),   (20, 3),   (22, 3),   "the north road, from Route 12"),
    ("Nemea",             (2, 16),   (1, 16),   (2, 17),   "the west road, from Route 13"),
    ("Daphni",            (4, 15),   (5, 15),   (4, 16),   "the west road, from Route 15"),
    ("Astyra",            (4, 32),   (5, 32),   (4, 33),   "the west gate, from Route 16"),
    ("Kaldera",           (17, 33),  (16, 33),  (17, 34),  "the landing, from the ferry"),
    ("KytheraSkandeia",   (29, 11),  (28, 12),  (28, 11),  "the harbor, from the ferry"),
    ("KytheraPaphia",     (40, 21),  (41, 21),  (40, 22),  "the east gate, from the Foam Road"),
    ("KnossaAmnisos",     (13, 7),   (12, 8),   (14, 7),   "the quay, from the crossing"),
    ("Ascent_3F",         (16, 4),   (15, 4),   (16, 5),   "the Propylaia's steps, the League"),
    ("Gytheion",          (23, 13),  (22, 13),  (23, 14),  "the Euploia's berth, from the crossing"),
    ("Lakonia",           (37, 35),  (38, 35),  (37, 36),  "the bridge, from Route 25"),
    ("Route28_SacredOlives", (42, 2), (42, 3),  (43, 2),   "the gorge path, above Hieron's clearing"),
    ("Delphoi",           (37, 41),  (37, 40),  (38, 41),  "the falls road, from the Kastalian Gorge"),
    ("Ascent_2F",         (3, 41),   (3, 42),   (4, 41),   "the cloud ledges' landing, up from the slopes"),
    ("LakeStymphalia",    (19, 32),  (18, 32),  (20, 32),  "the causeway's foot, from Route 26"),
]


def map_path(name):
    return ROOT / "data/maps" / name / "map.json"


def elevation(name, x, y):
    sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
    from mapedit import Layout
    lay = json.loads(map_path(name).read_text())["layout"]
    return Layout(name, lay).elev(x, y)


def herm_objects(name, herm, plaque):
    def obj(gfx, xy, script):
        return {
            "graphics_id": gfx,
            "x": xy[0],
            "y": xy[1],
            "elevation": elevation(name, *xy),
            "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
            "movement_range_x": 0,
            "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": script,
            "flag": "0",
        }
    return [obj(HERM_GFX, herm, HERM_SCRIPT), obj(PLAQUE_GFX, plaque, PLAQUE_SCRIPT)]


def apply(row):
    name, herm, plaque, _landing, _ = row
    path = map_path(name)
    text = path.read_text()
    data = json.loads(text)
    objs = [o for o in data.get("object_events") or []
            if o.get("graphics_id") not in (HERM_GFX, PLAQUE_GFX)]
    # Appended last, so no existing object's local id shifts.
    data["object_events"] = objs + herm_objects(name, herm, plaque)
    out = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if out != text:
        path.write_text(out)
        print(f"town_herms: {name}: herm {herm}, plaque {plaque}")


def preview(row, out_dir):
    """The entrance, 20x14 cells around the herm, at 3x with a cell grid."""
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import numpy as np
    from PIL import Image, ImageDraw
    import render_map as rm
    name, herm, plaque, landing, arrives = row
    rm.read_fieldmap_constants()
    symbols = rm.scan_tileset_symbols()
    lays = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    lay_id = json.loads(map_path(name).read_text())["layout"]
    lay = next(l for l in lays if l.get("id") == lay_id)
    r = rm.Renderer(rm.Tileset(rm.resolve_tileset(lay["primary_tileset"], symbols)),
                    rm.Tileset(rm.resolve_tileset(lay["secondary_tileset"], symbols)))
    img = rm.render_blocks(r, np.fromfile(ROOT / lay["blockdata_filepath"], "<u2"), lay["width"]).convert("RGBA")
    pics = ROOT / "graphics/object_events/pics/misc/ichor"
    data = json.loads(map_path(name).read_text())
    for o in data.get("object_events") or []:
        if o.get("graphics_id") not in (HERM_GFX, PLAQUE_GFX):
            ImageDraw.Draw(img).rectangle([o["x"] * 16 + 3, o["y"] * 16 + 3, o["x"] * 16 + 12, o["y"] * 16 + 12],
                                          outline=(255, 0, 255, 255))
    img.alpha_composite(Image.open(pics / "great_herm.png").convert("RGBA"), (herm[0] * 16, herm[1] * 16 - 16))
    img.alpha_composite(Image.open(pics / "herm_plaque.png").convert("RGBA"), (plaque[0] * 16, plaque[1] * 16))
    d = ImageDraw.Draw(img)
    lx, ly = landing
    d.rectangle([lx * 16 + 1, ly * 16 + 1, lx * 16 + 14, ly * 16 + 14], outline=(0, 160, 255, 255))
    for w in data.get("warp_events") or []:
        d.rectangle([w["x"] * 16 + 5, w["y"] * 16 + 5, w["x"] * 16 + 10, w["y"] * 16 + 10], fill=(255, 255, 0, 255))
    cx, cy = herm
    x0, y0 = max(0, cx - 10), max(0, cy - 7)
    x1, y1 = min(lay["width"], x0 + 20), min(lay["height"], y0 + 14)
    crop = img.crop((x0 * 16, y0 * 16, x1 * 16, y1 * 16))
    k = 3
    big = crop.resize((crop.width * k, crop.height * k), Image.NEAREST)
    d = ImageDraw.Draw(big)
    for i in range(x1 - x0 + 1):
        d.line([(i * 16 * k, 0), (i * 16 * k, big.height)], fill=(0, 0, 0, 70))
    for j in range(y1 - y0 + 1):
        d.line([(0, j * 16 * k), (big.width, j * 16 * k)], fill=(0, 0, 0, 70))
    for i in range(x1 - x0):
        d.text((i * 16 * k + 2, 1), str(x0 + i), fill=(255, 255, 255, 255))
    for j in range(y1 - y0):
        d.text((1, j * 16 * k + 2), str(y0 + j), fill=(255, 255, 255, 255))
    out = Path(out_dir) / f"{name}.png"
    big.save(out)
    print(out, arrives)


def main():
    args = sys.argv[1:]
    rows = [t for t in TOWNS if t[1] != (0, 0)]
    only = [a for a in args if not a.startswith("--") and a not in args[args.index("--preview") + 1:args.index("--preview") + 2]] \
        if "--preview" in args else [a for a in args if not a.startswith("--")]
    if only:
        rows = [t for t in rows if t[0] in only]
    if "--preview" in args:
        out_dir = Path(args[args.index("--preview") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        for row in rows:
            preview(row, out_dir)
        return
    for row in rows:
        apply(row)


if __name__ == "__main__":
    main()
