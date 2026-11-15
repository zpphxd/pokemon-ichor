#!/usr/bin/env python3
"""Draw, compile, register and catalog Act III's Lakonia secondaries.

Lakonia's six maps (and Route 24's strait) need far more distinct pieces than
one secondary's 504 tiles hold, so the art is split by map, as the Kythera
family is:

  gytheion    Gytheion and Route 24: the purple quay, the dye-works, Kranai,
              the theater, Cape Malea, the drowned town
  eurotas     Route 25: the river, reeds, Amyklai, the Vapheio door, the
              roofless farmhouse, the herm-shrines
  lakonia     Lakonia: the houses, the agoge's yard and ring, the stoa, the
              palaestra, Orthia, the Eurotas and the Taygetos wall
  stymphalia  Route 26, Lake Stymphalia and Route 27: the Platanistas, the
              marsh, its causeway and boardwalks, the hills to Arkadia

All pair with the aethos primary and share painters (lakonia_town, _water,
_mount, _route, _harbor), so a piece two of them carry is drawn once. The
pipeline is kythera_build.py's (its packing, Porytiles scratch project,
borrowed ground, verification and registration), with Lakonia's palette plan
(lakonia_lib.GROUPS, seven per tileset), its own catalog
(tools/ichor/maps/lakonia_tiles.py, design/phase4/TILES_<name>.md) and its
animations (the Eurotas, the black water, fire, glints, the Malea current).

Usage: /usr/bin/python3 tools/ichor/art/lakonia_build.py [gytheion|eurotas|lakonia|stymphalia|all]
           [--no-compile]
Then lakonia_scene.py renders the mock scenes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_build as KB  # noqa: E402
import kythera_lib as K  # noqa: E402
import lakonia_lib as L  # noqa: E402

ROOT = K.ROOT
TILES_PY = ROOT / "tools/ichor/maps/lakonia_tiles.py"
NAMES = ["gytheion", "eurotas", "lakonia", "stymphalia"]

# animation frame orders (Porytiles queues one step every 16 frames)
KB.ANIM_ORDER.update({
    "eurotas": ["0", "1", "2", "1"],
    "marsh": ["0", "0", "1", "1", "2", "2", "1", "1"],
    "glint": ["0", "0", "0", "1", "2", "0", "0", "0", "0", "0", "1", "0"],
    "flame": ["0", "1", "2", "1"],
    "current": ["0", "1", "2", "3"],
    "steam": ["0", "1", "2", "1"],
})


# --------------------------------------------------------------------------
# What each tileset holds
# --------------------------------------------------------------------------

def _all():
    import lakonia_mount as Mo
    import lakonia_town as T
    import lakonia_water as Wa
    by = {}
    for s in T.build() + Wa.build() + Mo.build():
        by[s.key] = s
    import kythera_land as KL
    by["_trees_kythera"] = KL.trees()
    for mod in ("lakonia_route", "lakonia_harbor"):
        try:
            m = __import__(mod)
        except ImportError:
            continue
        for s in m.build():
            by[s.key] = s
    return by


def plane(by):
    return K.pick(by["_trees_kythera"], ["plane_00", "plane_10", "plane_20", "plane_01",
                                         "plane_11", "plane_21", "plane_02", "plane_12",
                                         "plane_22"], w=3, key="plane",
                  notes="The oriental plane (3 x 3), Lakonia's tree: a broad crown of maple-like "
                        "leaves over a mottled pale trunk, on borrowed grass. Its top row is "
                        "drawn over the player (`T`); the rest is impassable. (Kythera's "
                        "painter: `kythera_land.trees`.)")


TAYGETOS_TOWN = ["mass_00", "mass_10", "mass_01", "mass_11", "mass_pine", "lip", "lip_b",
                 "face", "face_b", "foot", "foot_b", "pine_face", "side_E", "side_E_foot",
                 "in_E", "boulder", "scree"]

HOUSE_TOWN = ["RB_L", "RB_M", "RB_R", "R_L", "R_M", "R_R", "R_brush", "R_vent",
              "RF_L", "RF_M", "RF_R", "RF_jar", "T_L", "T_M", "T_R", "U_window",
              "U_L", "U_M", "U_R", "U_shield", "U_worn", "U_cloak", "U_list", "G_jar",
              "G_L", "G_M", "G_R", "door", "G_open", "G_bench", "G_spears", "G_wood",
              "P_L", "P_col", "door_porch", "P_R"]


def house_pick(by, names):
    h = by["house"]
    return K.pick(h, names, w=8, key="house", notes=h.notes)


def taygetos_pick(by, names, notes=None):
    t = by["taygetos"]
    return K.pick(t, names, w=8, key="taygetos", notes=notes or t.notes)


def spec(name):
    by = _all()
    if name == "lakonia":
        br = by["bridge"]
        return {
            "symbol": "gTileset_Lakonia", "dir": "lakonia", "label": "Lakonia",
            "doc": "TILES_lakonia.md", "title": "Lakonia, the town with no walls",
            "maps": "Lakonia",
            "groups": L.groups(["red", "stone", "veg", "river", "mount", "wood", "yard"]),
            "images": [("lakonia_agoge.png", "A 240 x 160 screen of the agoge's yard: the ring, the barracks, the Taygetos wall behind (3x; `lakonia_agoge_1x.png` is 1x)"),
                       ("lakonia_town.png", "The agora and the river: the Persian Stoa, the chained Enyalios, the Lesche, houses round their yards, the bridge, Orthia")],
            "sections": [
                ("town", [house_pick(by, HOUSE_TOWN), by["stoa"], by["colonnade"], by["orthia"],
                          by["enyalios"], by["burial"], by["rope"]]),
                ("yard", [by["yard"], by["ring"], by["sands"], by["sown"]]),
                ("land", [taygetos_pick(by, TAYGETOS_TOWN), plane(by), by["willow"],
                          by["oleander"]]),
                ("water", [by["river"],
                           K.pick(br, ["deck_W", "deck", "deck_E", "face_W", "arch", "face_E"],
                                  w=3, key="bridge",
                                  notes="Lakonia's plain stone bridge over the Eurotas, "
                                        "east-west: `deck_W` `deck` `deck_E` (repeat `deck`) "
                                        "over its south face `face_W` `arch` `face_E` in the "
                                        "water. Deck walkable, face impassable.")]),
            ],
            "rows": None,
            "fronts": ["house", "house_wide", "lampito", "low_house", "syssition", "barracks",
                       "lesche"],
            "labels": [("sown", [("C_teeth", "SownField_Teeth"), ("C", "SownField")])],
        }
    raise SystemExit(f"lakonia_build: unknown tileset {name}")


# --------------------------------------------------------------------------
# Kythera's pipeline, with Lakonia's text where it writes some
# --------------------------------------------------------------------------

def auto_rows(sp, spare=1):
    """Each section's start row when the sections are packed one after another
    (kythera_build.pack's first fit), with `spare` empty rows after each."""
    import numpy as np
    used = np.zeros((64, KB.COLS), bool)
    rows, start = {}, 0
    for name, structs in sp["sections"]:
        rows[name] = start
        end = start
        for s in structs:
            for c0 in range(0, s.w, KB.COLS):
                cw = min(KB.COLS, s.w - c0)
                spot = None
                for row in range(start, 64 - s.h + 1):
                    for col in range(0, KB.COLS - cw + 1):
                        if not used[row:row + s.h, col:col + cw].any():
                            spot = (row, col)
                            break
                    if spot:
                        break
                assert spot, f"no room for {s.key}"
                used[spot[0]:spot[0] + s.h, spot[1]:spot[1] + cw] = True
                end = max(end, spot[0] + s.h)
        start = end + spare
    print("  section rows:", rows)
    return rows


def write_sources(sp, structs, rows, used, filler="sn2"):
    """kythera_build.write_sources, with a filler color from Lakonia's palettes
    (an unused sheet cell must be opaque, and Kythera's filler is in none of
    them)."""
    import numpy as np
    from PIL import Image
    import shutil
    src = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_src"
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
    W, H = KB.COLS * 16, rows * 16
    sheets = {ln: np.zeros((H, W, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    beh = {}
    for s in structs:
        for cy in range(s.h):
            for cx in range(s.w):
                i = s.ids[cy][cx] - 0x200
                r, c = divmod(i, KB.COLS)
                for ln in sheets:
                    sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                        s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        for (x, y), mb in s.behaviors.items():
            beh[s.ids[y][x] - 0x200] = mb
    for r in range(rows):
        for c in range(KB.COLS):
            if not used[r, c]:
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, :3] = K.C[filler]
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, 3] = 255
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (src / "attributes.csv").write_text("\n".join(lines) + "\n")
    KB.write_anims(src, structs)
    return src


def register(sp, animated):
    KB.register(sp, animated)
    hdr = ROOT / "src/data/tilesets/headers.h"
    t = hdr.read_text()
    t = t.replace(f"// Ichor: {sp['dir']}, {sp['title']} (Act III). Porytiles-managed, built by\n"
                  "// tools/ichor/art/kythera_build.py",
                  f"// Ichor: {sp['dir']}, {sp['title']} (Act III). Porytiles-managed, built by\n"
                  "// tools/ichor/art/lakonia_build.py")
    hdr.write_text(t)
    gfx = ROOT / "src/data/tilesets/graphics.h"
    t = gfx.read_text()
    t = t.replace(f"// Ichor: {sp['dir']} ({sp['title']}), written by tools/ichor/art/kythera_build.py",
                  f"// Ichor: {sp['dir']} ({sp['title']}), written by tools/ichor/art/lakonia_build.py")
    gfx.write_text(t)


def write_config(sp, groups):
    cfg = ROOT / "porytiles/tilesets" / sp["symbol"] / "config.yaml"
    cfg.write_text(
        f"# Per-tileset Porytiles config for {sp['symbol']} ({sp['title']}).\n"
        "# Written by tools/ichor/art/lakonia_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, path, sand,\n"
        "# sea and shallows. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + KB.palette_hints(groups))


LABELS = ROOT / "include/constants/metatile_labels.h"


def write_labels(sp, structs):
    want = dict(sp.get("labels", []))
    if not want:
        return
    start = f"// {sp['symbol']} (Ichor: {sp['title']}), written by tools/ichor/art/lakonia_build.py"
    end = f"// end {sp['symbol']}"
    lines = [start]
    by = {s.key: s for s in structs}
    for key, items in want.items():
        s = by[key]
        for name, label in items:
            cx, cy = s.names[name]
            lines.append(f"#define METATILE_{sp['label']}_{label:<24} 0x{s.ids[cy][cx]:03X}")
    lines.append(end)
    block = "\n".join(lines) + "\n"
    text = LABELS.read_text()
    if start in text:
        a = text.index(start)
        b = text.index(end, a) + len(end) + 1
        text = text[:a] + block + text[b:]
    else:
        e = text.rindex("#endif")
        text = text[:e] + block + "\n" + text[e:]
    LABELS.write_text(text)


def catalog(sp, structs):
    import lakonia_town as T
    data = []
    for sec_name, ss in sp["sections"]:
        for s in ss:
            data.append({
                "key": s.key, "title": s.title, "section": sec_name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                "ground": {f"{x},{y}": g for (x, y), g in s.ground.items()},
                "anims": sorted(set(K.anim_tiles(s).values())),
            })
    by = {d["key"]: d for d in data}
    fronts = {}
    for k in sp.get("fronts", []):
        f = T.FRONTS[k]
        house = by["house"]
        ids = []
        for row in f["rows"]:
            r = []
            for ref in row:
                cx, cy = house["names"][ref]
                r.append(house["ids"][cy][cx])
            ids.append(r)
        fronts[k] = {**f, "ids": ids}
    out = ROOT / f"build/{sp['dir']}"
    out.mkdir(parents=True, exist_ok=True)
    cat = {"tileset": sp["symbol"], "structures": data, "fronts": fronts}
    (out / "catalog.json").write_text(json.dumps(cat, indent=1))
    return cat


def write_tiles_py(name, cat):
    """tools/ichor/maps/lakonia_tiles.py: every Lakonia-family catalog as a
    Python dict, so map builders place pieces by key and name."""
    cur = {}
    if TILES_PY.exists():
        ns = {}
        exec(compile(TILES_PY.read_text(), str(TILES_PY), "exec"), ns)
        cur = ns.get("TILESETS", {})
    slim = {"symbol": cat["tileset"], "structures": {}, "fronts": {}}
    for d in cat["structures"]:
        slim["structures"][d["key"]] = {
            "w": d["w"], "h": d["h"], "ids": d["ids"], "walk": d["walk"],
            "names": {k: tuple(v) for k, v in d["names"].items()},
            "ground": d["ground"], "section": d["section"],
        }
    for k, f in cat["fronts"].items():
        slim["fronts"][k] = {"rows": f["rows"], "ids": f["ids"]}
    cur[name] = slim
    body = json.dumps(cur, indent=1, sort_keys=True)
    body = body.replace("true", "True").replace("false", "False").replace("null", "None")
    TILES_PY.parent.mkdir(parents=True, exist_ok=True)
    TILES_PY.write_text(
        '"""Metatile ids of Act III\'s Lakonia-family secondaries, for map builders.\n\n'
        "Generated by tools/ichor/art/lakonia_build.py; do not edit. One entry per\n"
        "tileset (gytheion, eurotas, lakonia, stymphalia), each {'symbol', 'structures':\n"
        "{key: {'w', 'h', 'ids' (rows of metatile ids), 'walk' (rows of walk codes),\n"
        "'names' {piece: (x, y)}, 'ground' {'x,y': aethos ground}, 'section'}},\n"
        "'fronts': {key: {'rows', 'ids'}}}. The catalogs, with what every piece is\n"
        "for, are design/phase4/TILES_*.md. Soft-edged pieces (yards, rivers, reeds,\n"
        "the marsh) are named by blob shape key: blob_key() below gives a cell's key\n"
        "from a mask, as kythera_lib.blob_key does.\n\n"
        "    from lakonia_tiles import mid, blob_key\n"
        "    door = mid('lakonia', 'house', 'door')\n"
        "    water = mid('lakonia', 'river', blob_key(mask, x, y))\n"
        '"""\n\n'
        f"TILESETS = {body}\n\n\n"
        "def mid(tileset, key, name=None, x=0, y=0):\n"
        '    """The metatile id of a named piece (or of cell (x, y) of a structure)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['ids'][y][x]\n\n\n"
        "def walk(tileset, key, name=None, x=0, y=0):\n"
        '    """The walk code of a named piece: X . T G J D W P (see the catalogs)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['walk'][y][x]\n\n\n"
        "def front(tileset, key):\n"
        '    """A house front\'s rows of metatile ids (None where nothing is drawn)."""\n'
        "    return TILESETS[tileset]['fronts'][key]['ids']\n\n\n"
        "NEIGHBORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]\n\n\n"
        "def blob_key(region, x, y):\n"
        '    """The shape key of cell (x, y) in a boolean region grid [y][x]: \'1|\' then\n'
        "    N NE E SE S SW W NW, a diagonal counting only when both of its sides are in\n"
        '    the region. Cells off the grid count as in the region."""\n'
        "    hh, ww = len(region), len(region[0])\n\n"
        "    def at(i, j):\n"
        "        if not (0 <= i < ww and 0 <= j < hh):\n"
        "            return 1\n"
        "        return 1 if region[j][i] else 0\n"
        "    b = [at(x + dx, y + dy) for dx, dy in NEIGHBORS]\n"
        "    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):\n"
        "        if not (b[a] and b[c]):\n"
        "            b[d] = 0\n"
        "    return '1|' + ''.join(str(v) for v in b)\n")


# --------------------------------------------------------------------------

def build_one(name, compile_=True):
    sp = spec(name)
    groups = sp["groups"]
    group_rgb = L.group_rgb(groups)
    structs = [s for _, ss in sp["sections"] for s in ss]
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), f"duplicate structure keys in {name}"
    probs = K.validate(structs, group_rgb)
    if not probs:
        before = len(K.tiles_of(structs))
        merges = K.merge_near_duplicates(structs, KB.NEAR_DUPLICATE_PX, group_rgb)
        print(f"{name}: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(K.tiles_of(structs))} tiles")
        probs = K.validate(structs, group_rgb)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    KB.fix_keys(structs)
    KB.check_anim_keys(structs)
    if not sp.get("rows"):
        sp["rows"] = auto_rows(sp)
    rows, used = KB.pack(sp)
    write_sources(sp, structs, rows, used)
    cat = catalog(sp, structs)
    write_tiles_py(name, cat)
    write_labels(sp, structs)
    print(f"{name}: {sum(s.w * s.h for s in structs)} metatiles in {rows} rows")
    if not compile_:
        return
    # until the tileset is registered, Porytiles can't reopen it from a manifest
    hdr = (ROOT / "src/data/tilesets/headers.h").read_text()
    cfg = ROOT / "porytiles/tilesets" / sp["symbol"]
    if f"const struct Tileset {sp['symbol']} =" not in hdr:
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            (cfg / f).unlink(missing_ok=True)
    animated = KB.compile_tileset(sp, groups)
    write_config(sp, groups)
    patched = KB.borrow_ground(sp, structs)
    register(sp, animated)
    n_tiles, n_meta = KB.verify(sp, rows, patched)
    KB.images(sp, structs)
    import lakonia_catalog
    lakonia_catalog.main(name, sp, n_tiles, n_meta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="lakonia")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    names = NAMES if args.tileset == "all" else [args.tileset]
    for n in names:
        build_one(n, not args.no_compile)


if __name__ == "__main__":
    main()
