#!/usr/bin/env python3
"""Build gTileset_Ergasteria and the rooms laid out from it.

Works like oikia_build.py (design/phase1/TILES_oikia.md), whose generic pieces
it reuses:

1. Compose every cell of every room (tools/ichor/maps/aegina_homes.py and
   tools/ichor/maps/emporion_rooms.py) and of the catalog layouts from the
   pieces in ergasteria_art.py: floor or wall on the bottom layer, furniture on
   the middle layer, overhangs on the top layer.
2. Deduplicate the cells into metatiles and write Porytiles' sources to
   data/tilesets/secondary/ergasteria/porytiles_src/.
3. Compile with Porytiles, paired with gTileset_Aethos, and copy back any solid
   tile Porytiles borrowed from it, so ergasteria uses only its own tiles and
   palettes 6-12 and works on any primary.
4. Check that, render every room through tools/ichor/render_map.py on oikos,
   aethos and building, and fail unless the renders are identical to each other
   and to the composed source.
5. Write each room's layout (data/layouts/<Layout>/map.bin, border.bin and its
   layouts.json size and tilesets), the 2x renders in design/phase2/img/, the
   metatile sheet and catalog, the generated tables in the set's TILES doc and
   each room module's ROOMS doc, and each room variant's setmetatile script in
   its map's scripts.pory.

The same machinery builds more than one set: a RoomSet names the tileset, its
art module and its docs, and each room spec says which set it is built from
("set", default "ergasteria"). limen_build.py builds gTileset_Limen with it.

Rooms are data in Python: the builder rewrites their blockdata on every run,
so metatile ids may move freely. Edit a room in its module, not in Porymap.

Room spec keys beyond oikia's (see aegina_homes.py for the rest):
  set       the RoomSet that builds it (default "ergasteria")
  floors    more grid characters, each to another floor
  walls     more grid characters, each to another wall style
  blocked   grid characters whose floor can't be walked on (the Deigma's sea)
  variants  {name: {"swap": {stamp: other stamp}, "drop": [stamp, ...],
            "script": label}}: the room as it looks after an event. Its cells
            join the tileset, and the cells that differ from the room as built
            become a setmetatile script (`label`) in the map's scripts.pory.

Usage: /usr/bin/python3 tools/ichor/art/ergasteria_build.py [--no-compile] [--preview DIR]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))

import ergasteria_art as EA  # noqa: E402
import oikia_build as OB  # noqa: E402  (Cell, over, cut, check_spots, ...)

PARTNER = "gTileset_Aethos"
PRIMARY = "gTileset_Oikos"          # what the rooms' layouts use
IMG = ROOT / "design/phase2/img"
MAGENTA = np.array([255, 0, 255], np.uint8)
FIRST_METATILE = 0x200
FIRST_TILE = 512
SECONDARY_PALS = range(6, 13)
MAX_METATILES = 512
MAX_TILES = 504                     # door animations overwrite tiles 504-511

WALK, SOLID, WARP = OB.WALK, OB.SOLID, OB.WARP
Cell, over, empty, cut = OB.Cell, OB.over, OB.empty, OB.cut


class RoomSet:
    """One secondary tileset built from composed rooms."""

    def __init__(self, name, tileset, art, tiles_doc, catalog=None, budget=None,
                 default_rooms_doc=None, sheet_cats=()):
        self.name = name                    # "ergasteria"; the data/tilesets/secondary folder
        self.tileset = tileset              # "gTileset_Ergasteria"
        self.A = art                        # the art module: PALETTES, FLOORS, WALLS, VOID, RUGS, STAMPS
        self.ts = ROOT / "data/tilesets/secondary" / name
        self.src = self.ts / "porytiles_src"
        self.bin = self.ts / "porytiles_bin"
        self.tiles_doc = tiles_doc
        self.catalog = catalog or (lambda: {})
        self.budget = budget                # a soft ceiling: warn above it
        self.default_rooms_doc = default_rooms_doc
        self.sheet_cats = sheet_cats        # (catalog name, image name) rendered to design/phase2/img/
        self.pal_sets = {n: set(p.values()) for n, p in art.PALETTES.items()}

    def log(self, msg):
        print(f"{self.name}: {msg}")


def room_modules():
    """The modules whose ROOMS dicts are built from these sets."""
    import aegina_homes
    import emporion_rooms
    import eleusa_rooms
    return [aegina_homes, emporion_rooms, eleusa_rooms]


# --------------------------------------------------------------------------
# Composition. oikia's composer, generalized: a room can mix floors (one per
# grid character) and wall styles (one per grid character, any height).
#   grid chars: '.' the room's floor; any key of spec["floors"] another floor;
#               'W' the room's wall; any key of spec["walls"] another wall;
#               '#' void.
# --------------------------------------------------------------------------

def compose(rs, spec, stamps=None):
    A = rs.A
    stamps = stamps or A.STAMPS
    grid = spec["grid"]
    H, W = len(grid), len(grid[0])
    assert all(len(r) == W for r in grid), f"{spec.get('title')}: ragged grid"
    cells = [[Cell() for _ in range(W)] for _ in range(H)]
    floors = {".": spec["floor"]}
    floors.update(spec.get("floors", {}))
    walls = {"W": spec["wall"]}
    walls.update(spec.get("walls", {}))
    blocked = set(spec.get("blocked", ""))

    def ch(x, y):
        return grid[y][x] if 0 <= x < W and 0 <= y < H else "#"

    for (name, sx, sy) in spec["stamps"]:
        st = stamps[name]
        for cy in range(st["h"]):
            for cx in range(st["w"]):
                x, y = sx + cx, sy + cy
                if not (0 <= x < W and 0 <= y < H):
                    raise ValueError(f"{name} at ({sx},{sy}) runs off the room")
                sub = cut(st["img"], cx, cy)
                top = cut(st["top"], cx, cy) if st["top"] is not None else None
                if empty(sub) and empty(top):
                    continue
                c = cells[y][x]
                if not empty(sub):
                    if st["flatten"]:
                        c.flat = over(getattr(c, "flat", np.zeros((16, 16, 4), np.uint8)), sub)
                    else:
                        c.middle = sub.copy() if c.middle is None else over(c.middle, sub)
                if not empty(top):
                    c.top = top.copy() if c.top is None else over(c.top, top)
                if c.covered and c.block == SOLID and (cx, cy) in st["walk"]:
                    pass        # a walkable overlay keeps what's under it blocked
                elif (cx, cy) in st["walk"]:
                    c.block = WARP if (cx, cy) in st["behavior"] else WALK
                else:
                    c.block = SOLID
                c.covered = True
                if (cx, cy) in st["behavior"]:
                    c.behavior = st["behavior"][(cx, cy)]

    rug_at = {}
    for (design, rx, ry, rw, rh) in spec.get("rugs", []):
        assert rw >= 2 and rh >= 2, "rugs are at least 2x2"
        img = A.RUGS[design]
        for j in range(rh):
            for i in range(rw):
                pi = 0 if i == 0 else 2 if i == rw - 1 else 1
                pj = 0 if j == 0 else 2 if j == rh - 1 else 1
                rug_at[(rx + i, ry + j)] = cut(img, pi, pj)

    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            g = ch(x, y)
            if g in walls:
                style = A.WALLS[walls[g]]
                k = 0
                while ch(x, y - 1 - k) in walls:
                    k += 1
                c.bottom = cut(style, 0, min(k, style.shape[0] // 16 - 1)).copy()
                if not c.covered:
                    c.block = SOLID
            elif g == "#":
                c.bottom = A.VOID.copy()
                if not c.covered:
                    c.block = SOLID
            elif (x, y) in rug_at:
                c.bottom = rug_at[(x, y)].copy()
            elif g in floors:
                mat = A.FLOORS[floors[g]]
                same = floors if g not in blocked else {g: None}
                top_sh = ch(x, y - 1) not in same
                left_sh = ch(x - 1, y) not in same
                if top_sh and left_sh:
                    v = "corner"
                elif top_sh:
                    v = "top"
                elif left_sh:
                    v = "left"
                elif "alt" in mat and not c.covered and OB.alt_floor(x, y):
                    v = "alt"
                else:
                    v = "plain"
                if v not in mat:
                    v = "top" if v == "corner" and "top" in mat else "plain"
                c.bottom = mat[v].copy()
                if g in blocked:
                    c.block = SOLID
            else:
                raise ValueError(f"{spec.get('title')}: unknown grid char {g!r} at ({x},{y})")
            if hasattr(c, "flat"):
                c.bottom = over(c.bottom, c.flat)
            assert (c.bottom[..., 3] == 255).all(), f"hole in bottom layer at ({x},{y})"
            if c.middle is not None and c.top is not None:
                raise ValueError(f"({x},{y}) would need three layers; flatten the stamp")
    return cells


def variant_spec(spec, var):
    """The room spec as one of its variants: stamps swapped or dropped."""
    swap, drop = var.get("swap", {}), set(var.get("drop", ()))
    stamps = [(swap.get(n, n), x, y) for (n, x, y) in spec["stamps"] if n not in drop]
    stamps += list(var.get("add", ()))
    return dict(spec, stamps=stamps)


image_of = OB.image_of


# --------------------------------------------------------------------------
# Checks on the art
# --------------------------------------------------------------------------

def check_palettes(rs):
    taken = OB.aethos_colors()
    for name, pal in rs.A.PALETTES.items():
        assert len(pal) <= 15, f"palette {name} has {len(pal)} colors"
        for ch, rgb in pal.items():
            assert all(v % 8 == 0 for v in rgb), f"{name}.{ch} {rgb} is not a multiple of 8"
            assert rgb not in taken, f"{name}.{ch} {rgb} is also an aethos color"
            assert rgb != (255, 0, 255), "magenta is Porytiles' transparency"


def check_subtiles(rs, layer, where):
    for qy in (0, 8):
        for qx in (0, 8):
            q = layer[qy:qy + 8, qx:qx + 8]
            cols = {tuple(int(v) for v in c) for c in q[q[..., 3] > 0][:, :3]}
            if not cols:
                continue
            if not any(cols <= s for s in rs.pal_sets.values()):
                raise ValueError(f"8x8 tile at {where} +({qx},{qy}) mixes palettes: {sorted(cols)}")


# --------------------------------------------------------------------------
# Tileset sources
# --------------------------------------------------------------------------

def basic_cells(rs):
    """(name, cell) for the bare floors, walls, void and rug pieces."""
    A = rs.A
    out = []
    for mat, vs in A.FLOORS.items():
        for v in ("plain", "alt", "top", "left", "corner"):
            if v in vs:
                c = Cell()
                c.bottom = vs[v]
                out.append((f"floor {mat}, {v}", c))
    for style, img in A.WALLS.items():
        for k in range(img.shape[0] // 16):
            c = Cell()
            c.bottom = cut(img, 0, k).copy()
            c.block = SOLID
            out.append((f"wall {style}, row {k}", c))
    c = Cell()
    c.bottom = A.VOID
    c.block = SOLID
    out.append(("void (outside the room)", c))
    for design, img in A.RUGS.items():
        for pj in range(3):
            for pi in range(3):
                c = Cell()
                c.bottom = cut(img, pi, pj).copy()
                part = ["top-left", "top", "top-right", "left", "middle", "right",
                        "bottom-left", "bottom", "bottom-right"][pj * 3 + pi]
                out.append((f"rug {design}, {part}", c))
    return out


def collect(rs, layouts):
    order, index = [], {}

    def add(c):
        k = c.key()
        if k not in index:
            index[k] = len(order)
            order.append(c)
        return index[k]

    for _, c in basic_cells(rs):
        add(c)
    ids = {}
    for name, cells in layouts.items():
        ids[name] = [[FIRST_METATILE + add(c) for c in row] for row in cells]
    return order, ids


def write_sources(rs, order):
    n = len(order)
    if n > MAX_METATILES:
        raise SystemExit(f"{rs.name}: {n} metatiles is over the {MAX_METATILES} limit")
    rows = (n + 7) // 8
    imgs = {k: np.zeros((rows * 16, 128, 4), np.uint8) for k in ("bottom", "middle", "top")}
    for k in imgs:
        imgs[k][..., :3] = MAGENTA
        imgs[k][..., 3] = 255
    attrs = ["id,behavior"]
    for i, c in enumerate(order):
        y, x = (i // 8) * 16, (i % 8) * 16
        for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
            if layer is None:
                continue
            check_subtiles(rs, layer, f"metatile {FIRST_METATILE + i:#x} {k}")
            reg = imgs[k][y:y + 16, x:x + 16]
            m = layer[..., 3] > 0
            reg[m, :3] = layer[m, :3]
        if c.behavior != "MB_NORMAL":
            attrs.append(f"{i},{c.behavior}")
    rs.src.mkdir(parents=True, exist_ok=True)
    for k, img in imgs.items():
        Image.fromarray(img, "RGBA").save(rs.src / f"{k}.png")
    (rs.src / "attributes.csv").write_text("\n".join(attrs) + "\n")
    rs.log(f"{n} metatiles written to {rs.src.relative_to(ROOT)}")


def porytiles(rs):
    exe = shutil.which("porytiles") or os.path.expanduser("~/.local/bin/porytiles")
    # Porytiles only compiles a secondary against a primary it manages, so
    # the set is paired with aethos, as oikia is. It never keeps an aethos
    # tile or palette (unshare_primary_tiles and check_compiled see to that),
    # so aethos's checksum cache, which can lag its sources, isn't verified.
    cmd = [exe, "compile-tileset", rs.tileset,
           "--primary-pairing-mode", "manual", "--primary-pairing-partners", PARTNER,
           "--no-verify-checksums"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"{rs.name}: porytiles failed")
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr).strip())


def unshare_primary_tiles(rs):
    """oikia_build's fix: copy each solid tile Porytiles borrowed from aethos
    into the set's own tiles.png."""
    prim = OB.tiles_of(np.array(Image.open(ROOT / "data/tilesets/primary/aethos/porytiles_bin/tiles.png")) % 16)
    im = Image.open(rs.bin / "tiles.png")
    assert im.mode == "P"
    own = list(OB.tiles_of(np.array(im)))
    meta = np.fromfile(rs.bin / "metatiles.bin", "<u2")
    used = max((int(e) & 0x3FF) for e in meta if (int(e) & 0x3FF) >= FIRST_TILE)
    own = own[:used - FIRST_TILE + 1]
    copies = {}
    for i, e in enumerate(meta):
        e = int(e)
        idx, pal = e & 0x3FF, e >> 12
        if idx == 0 or idx >= FIRST_TILE:
            continue
        if idx not in copies:
            copies[idx] = FIRST_TILE + len(own)
            own.append((prim[idx] + pal * 16).astype(np.uint8))
        meta[i] = (e & ~0x3FF) | copies[idx]
    if not copies:
        return 0
    rows = (len(own) + 15) // 16
    sheet = np.zeros((rows * 16, 8, 8), np.uint8)
    sheet[:len(own)] = np.stack(own)
    arr = sheet.reshape(rows, 16, 8, 8).swapaxes(1, 2).reshape(rows * 8, 128)
    out = Image.fromarray(arr, "P")
    out.putpalette(im.getpalette())
    out.save(rs.bin / "tiles.png")
    meta.astype("<u2").tofile(rs.bin / "metatiles.bin")
    cache = ROOT / f"porytiles/tilesets/{rs.tileset}/tileset.cache.json"
    data = json.loads(cache.read_text())
    for f in ("tiles.png", "metatiles.bin"):
        key = str((rs.bin / f).relative_to(ROOT))
        if key in data:
            data[key] = hashlib.md5((rs.bin / f).read_bytes()).hexdigest()
    cache.write_text(json.dumps(data, indent=2) + "\n")
    rs.log(f"copied {len(copies)} solid tiles Porytiles had borrowed from aethos")
    return len(copies)


def check_compiled(rs):
    meta = np.fromfile(rs.bin / "metatiles.bin", "<u2").reshape(-1, 8)
    bad, pals = [], set()
    for i, row in enumerate(meta):
        for e in row:
            idx, pal = int(e) & 0x3FF, int(e) >> 12
            if idx == 0:
                continue
            if idx < FIRST_TILE or pal not in SECONDARY_PALS:
                bad.append((FIRST_METATILE + i, idx, pal))
            pals.add(pal)
    if bad:
        raise SystemExit(f"{rs.name}: metatiles reach outside {rs.name}: {bad[:8]}")
    used = len({int(e) & 0x3FF for e in meta.ravel() if int(e) & 0x3FF >= FIRST_TILE})
    top = max(int(e) & 0x3FF for e in meta.ravel()) - FIRST_TILE + 1
    if top > MAX_TILES:
        raise SystemExit(f"{rs.name}: tiles reach {top}, over {MAX_TILES} (504-511 belong to door animations)")
    if rs.budget and used > rs.budget:
        rs.log(f"WARNING {used} tiles is over the budget of {rs.budget}")
    rs.log(f"compiled {len(meta)} metatiles, {used} tiles, palettes {sorted(pals)}")
    return len(meta), used, sorted(pals)


# --------------------------------------------------------------------------
# ergasteria's catalogs: every piece on the floors and walls it stands on, so a
# room can be re-dressed by hand, and so the sheet shows the set.
# --------------------------------------------------------------------------

WALL_HUNG = ["window", "niche", "herbs", "jar_shelf", "honey_shelf", "die_rack", "vault_door",
             "shield_spear", "tongs_rack"]
BACK = ["ant_shrine"]
FREE = ["kline", "klismos_r", "klismos_l", "stool", "bench", "table", "table_round",
        "amphora", "amphora_plain", "pithos", "pots", "myrtle", "fish_basket",
        "knucklebones", "lampstand", "column", "anvil", "brazier_small", "scales",
        "turtle_chest", "coin_table", "anthill_pot", "cistern", "hearth_floor", "ant_trail", "mat",
        "smith_anvil", "quench_trough", "votive_shelf", "charcoal_basket"]
GALLERY = ["gallery_door", "gallery_rail", "gallery_blanket", "gallery_lamp", "ladder"]


def _row_pack(A, names, width, y0, x0=1, gap=1):
    out, x, y, rowh = [], x0, y0, 0
    for n in names:
        w, h = A.STAMPS[n]["w"], A.STAMPS[n]["h"]
        if x + w > width:
            x, y, rowh = x0, y + rowh + gap, 0
        out.append((n, x, y))
        x += w + gap
        rowh = max(rowh, h)
    return out, y + rowh


def ergasteria_catalog():
    A = EA
    cats = {}
    for floor, wall in (("terracotta", "blue"), ("flags", "stone")):
        placed, x = [], 0
        for n in WALL_HUNG:
            placed.append((n, x, 0))
            x += A.STAMPS[n]["w"]
        placed += [("soot", x, 0), ("hearth", x, 2)]
        x += 2
        for n in BACK:
            placed.append((n, x, 3 - A.STAMPS[n]["h"]))
            x += A.STAMPS[n]["w"]
        width = max(24, x)
        free, bottom = _row_pack(A, FREE, width, 5)
        placed += free
        rug_y = bottom + 1
        height = rug_y + 4
        grid = ["W" * width, "W" * width] + ["." * width for _ in range(height - 2)]
        cats[f"catalog_{floor}"] = {
            "title": f"Catalog on {floor}, {wall} wall",
            "floor": floor, "wall": wall, "grid": grid,
            "rugs": [("red", 1, rug_y, 3, 3), ("blue", 5, rug_y, 3, 3)],
            "stamps": placed, "spots": [],
        }
    # the gallery, over its own wall, with the turtle mosaic on flags below it
    gw = 12
    grid = ["G" * gw, "G" * gw, "G" * gw] + ["." * gw for _ in range(5)]
    placed = [(n, i * 2, 0 if n != "ladder" else 1) for i, n in enumerate(GALLERY)]
    placed.append(("mosaic_turtle", 1, 4))
    cats["catalog_gallery"] = {
        "title": "The inn's gallery and courtyard",
        "floor": "flags", "wall": "blue", "walls": {"G": "gallery"}, "grid": grid,
        "rugs": [], "stamps": placed, "spots": [],
    }
    # the forge, cold and lit, on the smithy's earth under its smoke-black wall
    grid = ["WWWWWWWWWW", "WWWWWWWWWW"] + ["." * 10 for _ in range(3)]
    cats["catalog_forge"] = {
        "title": "The Hephaisteion's forge, cold and lit",
        "floor": "earth", "wall": "smoke", "grid": grid, "rugs": [],
        "stamps": [("forge_hood", 0, 0), ("forge_cold", 0, 2), ("bellows", 3, 2),
                   ("forge_hood_lit", 5, 0), ("forge_lit", 5, 2), ("bellows", 8, 2)],
        "spots": [],
    }
    return cats


ERGASTERIA = RoomSet(
    "ergasteria", "gTileset_Ergasteria", EA,
    tiles_doc=ROOT / "design/phase2/TILES_ergasteria.md",
    catalog=ergasteria_catalog, budget=None,
    default_rooms_doc=ROOT / "design/phase2/ROOMS_ergasteria.md",
    sheet_cats=(("catalog_terracotta", "ergasteria_catalog.png"),
                ("catalog_gallery", "ergasteria_gallery.png"),
                ("catalog_forge", "ergasteria_forge.png")))


# --------------------------------------------------------------------------
# Rendering, layouts, docs
# --------------------------------------------------------------------------

def blockdata(cells, ids):
    return OB.blockdata(cells, ids)


def render_compiled(rs, blocks, width, primary):
    import render_map as RM
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(primary, syms)),
                    RM.Tileset(RM.resolve_tileset(rs.tileset, syms)))
    return np.array(RM.render_blocks(r, blocks, width))


save_scaled = OB.save_scaled


def update_layouts_json(rs, sizes, primary=PRIMARY):
    """Point each room's layouts.json entry at the set with its size.
    Only the four fields that change are edited, in place, so the rest of the
    file keeps its formatting."""
    path = ROOT / "data/layouts/layouts.json"
    text = path.read_text()
    out = text
    for folder, (w, h) in sizes.items():
        key = f'"blockdata_filepath": "data/layouts/{folder}/map.bin"'
        at = out.index(key)
        start = out.rindex("{", 0, at)
        end = out.index("}", at)
        block = out[start:end]
        new = block
        for field, value in (("width", str(w)), ("height", str(h)),
                             ("primary_tileset", f'"{primary}"'), ("secondary_tileset", f'"{rs.tileset}"')):
            new, n = re.subn(rf'("{field}": )[^,\n]+', lambda m: m.group(1) + value, new)
            assert n == 1, f"{folder}: no {field} in layouts.json"
        out = out[:start] + new + out[end:]
    json.loads(out)
    if out != text:
        path.write_text(out)
        rs.log("layouts.json updated")


def room_doc(rs, name, spec, cells):
    H, W = len(cells), len(cells[0])
    marks = {}
    for i, spot in enumerate(spec["spots"], 1):
        tiles = spot[2] if spot[0] == "warp" else [spot[2]]
        for t in tiles:
            marks.setdefault(t, str(i) if i < 10 else chr(ord("a") + i - 10))
    lines = [f"### {spec['title']}", ""]
    lines.append(f"- Map: `{spec['map']}`. Layout: `data/layouts/{spec['layout']}/map.bin`, "
                 f"**{W}x{H}** blocks, `gTileset_Oikos` + `{rs.tileset}`.")
    floors = ", ".join([spec["floor"]] + list(spec.get("floors", {}).values()))
    walls = ", ".join([spec["wall"]] + list(spec.get("walls", {}).values()))
    lines.append(f"- Floor: {floors}. Wall: {walls}. Render: `design/phase2/img/{spec['render']}` (2x).")
    for vname, var in spec.get("variants", {}).items():
        lines.append(f"- Variant `{vname}`: `{var['script']}` in the map's scripts.pory swaps its cells.")
    lines.append("")
    lines.append("Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; "
                 "a bg event is marked on its furniture tile.")
    lines.append("")
    lines.append("```")
    lines.append("    " + "".join(f"{x % 10}" for x in range(W)))
    for y in range(H):
        row = ""
        for x in range(W):
            row += marks.get((x, y), "." if cells[y][x].block != SOLID else "#")
        lines.append(f"{y:3d} {row}")
    lines.append("```")
    lines.append("")
    lines.append("| # | Kind | Tile | Read from | What |")
    lines.append("|---|---|---|---|---|")
    for i, spot in enumerate(spec["spots"], 1):
        kind, label = spot[0], spot[1]
        key = str(i) if i < 10 else chr(ord("a") + i - 10)
        if kind == "warp":
            tile, frm = ", ".join(f"({x},{y})" for x, y in spot[2]), ""
        elif kind == "npc":
            tile, frm = f"({spot[2][0]},{spot[2][1]})", f"faces {spot[3]}"
        elif kind == "coord":
            tile, frm = f"({spot[2][0]},{spot[2][1]})", ""
        else:
            tile = f"({spot[2][0]},{spot[2][1]})"
            fx, fy, facing = spot[3]
            frm = f"({fx},{fy}) facing {facing}"
        lines.append(f"| {key} | {kind} | {tile} | {frm} | {label} |")
    lines.append("")
    return "\n".join(lines)


def stamp_doc(rs, composed, ids, cats, rooms):
    """Where each stamp first appears (a catalog if it's in one, else a room)."""
    A = rs.A
    where = {}
    for cat, spec in list(cats.items()) + list(rooms.items()):
        for (n, sx, sy) in spec["stamps"]:
            if n in where:
                continue
            st = A.STAMPS[n]
            rows = []
            for cy in range(st["h"]):
                row = []
                for cx in range(st["w"]):
                    sub = cut(st["img"], cx, cy)
                    row.append(f"{ids[cat][sy + cy][sx + cx]:03X}" if not empty(sub) else "---")
                rows.append(" ".join(row))
            where[n] = (cat.replace("catalog_", ""), " / ".join(rows))
    lines = ["| Stamp | Cells | Palette | From | Metatiles (where) | What it is |",
             "|---|---|---|---|---|---|"]
    for n, st in A.STAMPS.items():
        if n not in where:
            continue
        cat, ids_ = where[n]
        lines.append(f"| `{n}` | {st['w']}x{st['h']} | {st['pal']} | {st.get('source', rs.name)} | "
                     f"{ids_} ({cat}) | {st['note']} |")
    return "\n".join(lines)


def base_doc(rs, order):
    index = {c.key(): FIRST_METATILE + i for i, c in enumerate(order)}
    lines = ["| Piece | Metatile |", "|---|---|"]
    for name, c in basic_cells(rs):
        lines.append(f"| {name} | `{index[c.key()]:03X}` |")
    return "\n".join(lines)


def splice(path, text, tag="ergasteria_build", comment=("<!-- ", " -->")):
    begin = f"{comment[0]}{tag}: begin generated{comment[1]}"
    end = f"{comment[0]}{tag}: end generated{comment[1]}"
    doc = path.read_text()
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


def check_spots(name, spec, cells):
    """oikia_build's check. A "perch" is a person or Pokémon placed on a piece
    of furniture (Pheidon's Chelonet on the anvil): it's checked like a bg
    event, from the tile the player talks to it from."""
    spots = [("bg",) + tuple(s[1:]) if s[0] == "perch" else s for s in spec["spots"]]
    OB.check_spots(name, dict(spec, spots=spots), cells)


def all_rooms():
    rooms = {}
    for mod in room_modules():
        for n, spec in mod.ROOMS.items():
            assert n not in rooms, f"room {n} defined twice"
            rooms[n] = dict(spec, _module=mod)
    return rooms


def rooms_of(rs):
    return {n: s for n, s in all_rooms().items() if s.get("set", "ergasteria") == rs.name}


def variant_script(spec, vname, var, base_cells, base_ids, var_cells, var_ids):
    """A poryscript that turns the room as built into its variant."""
    lines = [f"script {var['script']} {{"]
    H, W = len(base_cells), len(base_cells[0])
    for y in range(H):
        for x in range(W):
            if base_ids[y][x] != var_ids[y][x] or base_cells[y][x].block != var_cells[y][x].block:
                solid = "TRUE" if var_cells[y][x].block == SOLID else "FALSE"
                lines.append(f"    setmetatile({x}, {y}, 0x{var_ids[y][x]:03X}, {solid})")
    lines.append("    return")
    lines.append("}")
    return "\n".join(lines)


def build(rs, args):
    """Compose, compile and check one set; write its rooms. Returns the composed rooms."""
    check_palettes(rs)
    rooms = rooms_of(rs)
    cats = rs.catalog()
    layouts = {n: compose(rs, s) for n, s in list(rooms.items()) + list(cats.items())}
    for n, spec in rooms.items():
        check_spots(n, spec, layouts[n])
        for vname, var in spec.get("variants", {}).items():
            layouts[f"{n}@{vname}"] = compose(rs, variant_spec(spec, var))
    order, ids = collect(rs, layouts)
    rs.log(f"{len(order)} unique metatiles")

    if args.preview:
        d = Path(args.preview)
        for n, cells in layouts.items():
            save_scaled(image_of(cells), d / f"{n.replace('@', '_')}.png", 3)

    if args.no_compile:
        for c in order:
            for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
                if layer is not None:
                    check_subtiles(rs, layer, k)
        return rooms, layouts

    write_sources(rs, order)
    porytiles(rs)
    unshare_primary_tiles(rs)
    nmeta, ntiles, pals = check_compiled(rs)

    void_id = None
    for name, c in basic_cells(rs):
        if name.startswith("void"):
            void_id = FIRST_METATILE + [o.key() for o in order].index(c.key())
    sizes = {}
    scripts = {}
    for n, cells in layouts.items():
        H, W = len(cells), len(cells[0])
        blocks = blockdata(cells, ids[n])
        want = image_of(cells)
        got = {p: render_compiled(rs, blocks, W, p) for p in (PRIMARY, "gTileset_Aethos", "gTileset_Building")}
        if not np.array_equal(got[PRIMARY], want):
            raise SystemExit(f"{rs.name}: {n} does not render as composed")
        for p, img in got.items():
            if not np.array_equal(img, want):
                raise SystemExit(f"{rs.name}: {n} renders differently on {p}")
        if n in rooms:
            spec = rooms[n]
            d = ROOT / "data/layouts" / spec["layout"]
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | SOLID] * 4, "<u2").tofile(d / "border.bin")
            save_scaled(got[PRIMARY], IMG / spec["render"], 2)
            sizes[spec["layout"]] = (W, H)
            rs.log(f"{n} {W}x{H} -> data/layouts/{spec['layout']}, design/phase2/img/{spec['render']}")
        elif "@" in n:
            base, vname = n.split("@")
            spec = rooms[base]
            save_scaled(got[PRIMARY], IMG / spec["render"].replace(".png", f"_{vname}.png"), 2)
            scripts.setdefault(spec["layout"], []).append(
                variant_script(spec, vname, spec["variants"][vname], layouts[base], ids[base], cells, ids[n]))
    update_layouts_json(rs, sizes)
    for layout, texts in scripts.items():
        pory = ROOT / "data/maps" / layout / "scripts.pory"
        splice(pory, f"// Written by tools/ichor/art/{rs.name}_build.py; don't edit by hand.\n\n"
               + "\n\n".join(texts), tag=f"{rs.name}_build", comment=("// ", ""))
    for cat, img in rs.sheet_cats:
        cells = layouts[cat]
        save_scaled(render_compiled(rs, blockdata(cells, ids[cat]), len(cells[0]), PRIMARY), IMG / img, 2)
    sheet = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", rs.name,
                            "--primary", "oikos", "--scale", "2", "-o", str(IMG / f"{rs.name}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
    if sheet.returncode != 0:
        sys.stderr.write(sheet.stderr)
        raise SystemExit(f"{rs.name}: sheet render failed")
    docs = {}
    for n, s in rooms.items():
        doc = getattr(s["_module"], "ROOMS_DOC", rs.default_rooms_doc)
        docs.setdefault(doc, []).append(room_doc(rs, n, s, layouts[n]))
    for doc, texts in docs.items():
        if doc.exists():
            splice(doc, "\n".join(texts), tag=f"{rs.name}_build")
    if rs.tiles_doc.exists():
        stats = (f"Built: **{len(order)}** metatiles (`0x200`-`{FIRST_METATILE + len(order) - 1:#05x}`) "
                 f"of 512, **{ntiles}** tiles of {MAX_TILES}, palettes {pals[0]}-{pals[-1]}.\n\n")
        splice(rs.tiles_doc, stats + base_doc(rs, order) + "\n\n" + stamp_doc(rs, layouts, ids, cats, rooms),
               tag=f"{rs.name}_build")
    rs.log(f"identical on oikos, aethos and building; {nmeta} metatiles, {ntiles} tiles, palettes {pals}")
    return rooms, layouts


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="compose and check only; leave Porytiles' files alone")
    ap.add_argument("--preview", metavar="DIR", help="also write source-composed previews here (3x)")
    return ap.parse_args()


def main():
    build(ERGASTERIA, parse_args())


if __name__ == "__main__":
    main()
