#!/usr/bin/env python3
"""Build gTileset_Chalkeon and the Black Sea's rooms laid out from it.

Works like world-act1's ergasteria_build.py (and oikia_build.py before it),
whose generic pieces it reuses or carries over:

1. Compose every cell of every room in tools/ichor/maps/pontos_rooms.py, and
   of the catalog layout, from the pieces in chalkeon_art.py and
   chalkeon_pieces.py: floor or wall on the bottom layer, furniture on the
   middle layer, overhangs on the top layer.
2. Deduplicate the cells into metatiles and write Porytiles' sources to
   data/tilesets/secondary/chalkeon/porytiles_src/.
3. Compile with Porytiles, paired with gTileset_Aethos, and copy back any
   solid tile Porytiles borrowed from it, so chalkeon uses only its own tiles
   and palettes 6-12 and works on any primary.
4. Render every room through tools/ichor/render_map.py on oikos, aethos and
   building, and fail unless the renders match each other and the composed
   source.
5. Write each room's layout (data/layouts/<Layout>/map.bin, border.bin, and
   its layouts.json size and tilesets), the 2x renders and the contact sheet
   in design/oikoumene/img/, the metatile sheet and catalog, the generated
   tables in design/oikoumene/ROOMS_pontos.md, and each room variant's
   setmetatile script in its map's scripts.pory.

Rooms are data in Python: the builder rewrites their blockdata on every run,
so metatile ids may move freely. Edit a room in pontos_rooms.py, not in
Porymap. Batch 2's palace hall adds its rooms to the same set by listing its
module in room_modules().

Room spec keys (pontos_rooms.py's docstring has the rest):
  floors    more grid characters, each to another floor
  walls     more grid characters, each to another wall style
  variants  {name: {"swap": {stamp: other}, "drop": [...], "script": label}}

Usage: /usr/bin/python3 tools/ichor/art/chalkeon_build.py [--no-compile] [--preview DIR]
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
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))

import chalkeon_art as CA  # noqa: E402
import oikia_build as OB  # noqa: E402  (Cell, over, cut, tiles_of, ...)

NAME = "chalkeon"
TILESET = "gTileset_Chalkeon"
PARTNER = "gTileset_Aethos"
PRIMARY = "gTileset_Oikos"          # what the rooms' layouts use
TS = ROOT / "data/tilesets/secondary" / NAME
SRC = TS / "porytiles_src"
BIN = TS / "porytiles_bin"
IMG = ROOT / "design/oikoumene/img"
DOC = ROOT / "design/oikoumene/ROOMS_pontos.md"
MAGENTA = np.array([255, 0, 255], np.uint8)
FIRST_METATILE = 0x200
FIRST_TILE = 512
SECONDARY_PALS = range(6, 13)
MAX_METATILES = 512
MAX_TILES = 504                     # door animations overwrite tiles 504-511
BUDGET = 410                        # leave batch 2's palace hall about 95 tiles

WALK, SOLID, WARP = OB.WALK, OB.SOLID, OB.WARP
Cell, over, empty, cut = OB.Cell, OB.over, OB.empty, OB.cut
PAL_SETS = {n: set(p.values()) for n, p in CA.PALETTES.items()}


def log(msg):
    print(f"{NAME}: {msg}")


def room_modules():
    """The modules whose ROOMS dicts are built from chalkeon."""
    import pontos_rooms
    return [pontos_rooms]


# --------------------------------------------------------------------------
# Composition: oikia's composer, generalized. A room can mix floors (one per
# grid character) and wall styles (one per grid character, any height).
#   '.' the room's floor; any key of spec["floors"] another floor;
#   'W' the room's wall; any key of spec["walls"] another wall; '#' void.
# --------------------------------------------------------------------------

def compose(spec, stamps=None):
    stamps = stamps or CA.STAMPS
    grid = spec["grid"]
    H, W = len(grid), len(grid[0])
    assert all(len(r) == W for r in grid), f"{spec.get('title')}: ragged grid"
    cells = [[Cell() for _ in range(W)] for _ in range(H)]
    floors = {".": spec["floor"]}
    floors.update(spec.get("floors", {}))
    walls = {"W": spec["wall"]}
    walls.update(spec.get("walls", {}))

    def ch(x, y):
        return grid[y][x] if 0 <= x < W and 0 <= y < H else "#"

    for (name, sx, sy) in spec["stamps"]:
        st = stamps[name]
        for cy in range(st["h"]):
            for cx in range(st["w"]):
                x, y = sx + cx, sy + cy
                if not (0 <= x < W and 0 <= y < H):
                    raise ValueError(f"{spec.get('title')}: {name} at ({sx},{sy}) runs off the room")
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

    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            g = ch(x, y)
            if g in walls:
                style = CA.WALLS[walls[g]]
                k = 0
                while ch(x, y - 1 - k) in walls:
                    k += 1
                c.bottom = cut(style, 0, min(k, style.shape[0] // 16 - 1)).copy()
                if not c.covered:
                    c.block = SOLID
            elif g == "#":
                c.bottom = CA.VOID.copy()
                if not c.covered:
                    c.block = SOLID
            elif g in floors:
                mat = CA.FLOORS[floors[g]]
                top_sh = ch(x, y - 1) not in floors
                left_sh = ch(x - 1, y) not in floors
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
                c.bottom = mat[v].copy()
            else:
                raise ValueError(f"{spec.get('title')}: unknown grid char {g!r} at ({x},{y})")
            if hasattr(c, "flat"):
                c.bottom = over(c.bottom, c.flat)
            assert (c.bottom[..., 3] == 255).all(), f"hole in bottom layer at ({x},{y})"
            if c.middle is not None and c.top is not None:
                raise ValueError(f"{spec.get('title')}: ({x},{y}) would need three layers")
    return cells


def variant_spec(spec, var):
    swap, drop = var.get("swap", {}), set(var.get("drop", ()))
    stamps = [(swap.get(n, n), x, y) for (n, x, y) in spec["stamps"] if n not in drop]
    stamps += list(var.get("add", ()))
    return dict(spec, stamps=stamps)


image_of = OB.image_of


# --------------------------------------------------------------------------
# Checks on the art
# --------------------------------------------------------------------------

def check_palettes():
    taken = OB.aethos_colors()
    for name, pal in CA.PALETTES.items():
        assert len(pal) <= 15, f"palette {name} has {len(pal)} colors"
        for ch, rgb in pal.items():
            assert all(v % 8 == 0 for v in rgb), f"{name}.{ch} {rgb} is not a multiple of 8"
            assert rgb not in taken, f"{name}.{ch} {rgb} is also an aethos color"
            assert rgb != (255, 0, 255), "magenta is Porytiles' transparency"
    assert len(CA.PALETTES) <= 7, "a secondary has 7 palettes"


def check_subtiles(layer, where):
    for qy in (0, 8):
        for qx in (0, 8):
            q = layer[qy:qy + 8, qx:qx + 8]
            cols = {tuple(int(v) for v in c) for c in q[q[..., 3] > 0][:, :3]}
            if not cols:
                continue
            if not any(cols <= s for s in PAL_SETS.values()):
                raise ValueError(f"8x8 tile at {where} +({qx},{qy}) mixes palettes: {sorted(cols)}")


# --------------------------------------------------------------------------
# Tileset sources
# --------------------------------------------------------------------------

def basic_cells():
    """(name, cell) for the bare floors, walls and void."""
    out = []
    for mat, vs in CA.FLOORS.items():
        for v in ("plain", "alt", "top", "left", "corner"):
            if v in vs:
                c = Cell()
                c.bottom = vs[v]
                out.append((f"floor {mat}, {v}", c))
    for style, img in CA.WALLS.items():
        for k in range(img.shape[0] // 16):
            c = Cell()
            c.bottom = cut(img, 0, k).copy()
            c.block = SOLID
            out.append((f"wall {style}, row {k}", c))
    c = Cell()
    c.bottom = CA.VOID
    c.block = SOLID
    out.append(("void (outside the room)", c))
    return out


def collect(layouts):
    order, index = [], {}

    def add(c):
        k = c.key()
        if k not in index:
            index[k] = len(order)
            order.append(c)
        return index[k]

    for _, c in basic_cells():
        add(c)
    ids = {}
    for name, cells in layouts.items():
        ids[name] = [[FIRST_METATILE + add(c) for c in row] for row in cells]
    return order, ids


def write_sources(order):
    n = len(order)
    if n > MAX_METATILES:
        raise SystemExit(f"{NAME}: {n} metatiles is over the {MAX_METATILES} limit")
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
            check_subtiles(layer, f"metatile {FIRST_METATILE + i:#x} {k}")
            reg = imgs[k][y:y + 16, x:x + 16]
            m = layer[..., 3] > 0
            reg[m, :3] = layer[m, :3]
        if c.behavior != "MB_NORMAL":
            attrs.append(f"{i},{c.behavior}")
    SRC.mkdir(parents=True, exist_ok=True)
    for k, img in imgs.items():
        Image.fromarray(img, "RGBA").save(SRC / f"{k}.png")
    (SRC / "attributes.csv").write_text("\n".join(attrs) + "\n")
    log(f"{n} metatiles written to {SRC.relative_to(ROOT)}")


def write_config():
    """Porytiles' per-tileset config: paired with aethos, and the seven
    palettes as packing hints. Every 8x8 tile already fits one of them
    (check_subtiles), so with the hints the packing is immediate; without
    them Porytiles' backtracking search can run for many minutes."""
    lines = ["# Generated by tools/ichor/art/chalkeon_build.py; edit PALETTES in chalkeon_art.py.",
             "# chalkeon is compiled against aethos, the Porytiles-managed primary, but must work",
             "# on any primary: it uses only its own tiles and palettes 6-12, which the builder",
             "# checks after every compile.",
             "tileset:",
             "  primary_pairing:",
             "    mode: manual",
             f"    partners: [{PARTNER}]",
             "  palettes:",
             "    packing:",
             "      hints_enabled: true",
             "      hints:"]
    for name in CA.PALETTE_ORDER:
        lines.append(f"        - name: {name}")
        lines.append("          colors:")
        for rgb in CA.PALETTES[name].values():
            lines.append(f"            - [{rgb[0]}, {rgb[1]}, {rgb[2]}]")
    path = ROOT / f"porytiles/tilesets/{TILESET}/config.yaml"
    path.write_text("\n".join(lines) + "\n")


def porytiles():
    write_config()
    exe = shutil.which("porytiles") or os.path.expanduser("~/.local/bin/porytiles")
    # Porytiles only compiles a secondary against a primary it manages, so
    # chalkeon is paired with aethos, as oikia is. It never keeps an aethos
    # tile or palette (unshare_primary_tiles and check_compiled see to that).
    cmd = [exe, "compile-tileset", TILESET,
           "--primary-pairing-mode", "manual", "--primary-pairing-partners", PARTNER,
           "--no-verify-checksums"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"{NAME}: porytiles failed")
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr).strip())


def unshare_primary_tiles():
    """oikia_build's fix: copy each solid tile Porytiles borrowed from aethos
    into chalkeon's own tiles.png."""
    prim = OB.tiles_of(np.array(Image.open(ROOT / "data/tilesets/primary/aethos/porytiles_bin/tiles.png")) % 16)
    im = Image.open(BIN / "tiles.png")
    assert im.mode == "P"
    own = list(OB.tiles_of(np.array(im)))
    meta = np.fromfile(BIN / "metatiles.bin", "<u2")
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
    out.save(BIN / "tiles.png")
    meta.astype("<u2").tofile(BIN / "metatiles.bin")
    cache = ROOT / f"porytiles/tilesets/{TILESET}/tileset.cache.json"
    if cache.exists():
        data = json.loads(cache.read_text())
        for f in ("tiles.png", "metatiles.bin"):
            key = str((BIN / f).relative_to(ROOT))
            if key in data:
                data[key] = hashlib.md5((BIN / f).read_bytes()).hexdigest()
        cache.write_text(json.dumps(data, indent=2) + "\n")
    log(f"copied {len(copies)} solid tiles Porytiles had borrowed from aethos")
    return len(copies)


def check_compiled():
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
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
        raise SystemExit(f"{NAME}: metatiles reach outside {NAME}: {bad[:8]}")
    used = len({int(e) & 0x3FF for e in meta.ravel() if int(e) & 0x3FF >= FIRST_TILE})
    top = max(int(e) & 0x3FF for e in meta.ravel()) - FIRST_TILE + 1
    if top > MAX_TILES:
        raise SystemExit(f"{NAME}: tiles reach {top}, over {MAX_TILES} (504-511 belong to door animations)")
    if used > BUDGET:
        log(f"WARNING {used} tiles is over the budget of {BUDGET}")
    log(f"compiled {len(meta)} metatiles, {used} tiles, palettes {sorted(pals)}")
    return len(meta), used, sorted(pals)


# --------------------------------------------------------------------------
# The catalog: every piece once, on the floors and walls it stands on, so the
# sheet shows the set and batch 2 can see what it has to work with.
# --------------------------------------------------------------------------

def _row_pack(names, width, y0, x0=1, gap=1):
    out, x, y, rowh = [], x0, y0, 0
    for n in names:
        w, h = CA.STAMPS[n]["w"], CA.STAMPS[n]["h"]
        if x + w > width:
            x, y, rowh = x0, y + rowh + gap, 0
        out.append((n, x, y))
        x += w + gap
        rowh = max(rowh, h)
    return out, y + rowh


# chalkeon's own pieces, by where they stand. Hung pieces go on the wall rows,
# tall ones stand against the wall from row 0 or 1; the rest are packed on the
# floor below. oikia's shared furniture is in oikia's own catalog.
HUNG = ["window_lattice", "shutters_shut", "claw_marks", "dove_cage", "dove_cage_empty",
        "pheasants", "bull_head", "fleece_frame", "ram_panel", "linen_line"]
TALL = [("bull_fountain", 1), ("pithos_great", 1), ("cage_stack", 1), ("flax", 1),
        ("lime_sticks", 1), ("golden_maid", 1)]
FREE = ["asc_top_l", "asc_top_m", "asc_top_r", "stall_top_l", "stall_top_m", "stall_top_r",
        "table_bare", "ground_loom", "sledge", "workbench", "serpent_post", "log_post",
        "fire_jar", "wash_basin", "cold_krater", "fan", "tripod_wheels", "decoy_owl",
        "linen_bolts", "retting_tub"]
FRONTS = {"asc_top_l": "asc_front_l", "asc_top_m": "asc_front_rod", "asc_top_r": "asc_front_r",
          "stall_top_l": "stall_front_l", "stall_top_m": "stall_front_m", "stall_top_r": "stall_front_r"}


def catalog():
    width = 26
    placed, x = [], 0
    for n in HUNG:
        placed.append((n, x, 0))
        x += CA.STAMPS[n]["w"]
    x += 1
    for n, sy in TALL:
        placed.append((n, x, sy))
        x += CA.STAMPS[n]["w"]
    width = max(width, x)
    packed, bottom = _row_pack(FREE, width, 5, gap=1)
    for (n, px, py) in packed:
        placed.append((n, px, py))
        if n in FRONTS:
            placed.append((FRONTS[n], px, py + 1))
    placed.append(("asc_front_m", 0, 4))
    placed.append(("mat", width - 2, bottom + 2))
    height = bottom + 3
    grid = ["W" * width, "W" * width] + ["." * width for _ in range(height - 2)]
    return {"catalog": {"title": "chalkeon catalog", "floor": "planks", "wall": "bronze",
                        "grid": grid, "stamps": placed, "spots": []}}


# --------------------------------------------------------------------------
# Rendering, layouts, docs
# --------------------------------------------------------------------------

blockdata = OB.blockdata
save_scaled = OB.save_scaled


def render_compiled(blocks, width, primary):
    import render_map as RM
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(primary, syms)),
                    RM.Tileset(RM.resolve_tileset(TILESET, syms)))
    return np.array(RM.render_blocks(r, blocks, width))


def update_layouts_json(sizes, primary=PRIMARY):
    """Point each room's layouts.json entry at chalkeon with its size, editing
    only those four fields in place so the file keeps its formatting."""
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
                             ("primary_tileset", f'"{primary}"'), ("secondary_tileset", f'"{TILESET}"')):
            new, n = re.subn(rf'("{field}": )[^,\n]+', lambda m: m.group(1) + value, new)
            assert n == 1, f"{folder}: no {field} in layouts.json"
        out = out[:start] + new + out[end:]
    json.loads(out)
    if out != text:
        path.write_text(out)
        log("layouts.json updated")


def room_doc(name, spec, cells):
    H, W = len(cells), len(cells[0])
    marks = {}
    for i, spot in enumerate(spec["spots"], 1):
        tiles = spot[2] if spot[0] == "warp" else [spot[2]]
        for t in tiles:
            marks.setdefault(t, str(i) if i < 10 else chr(ord("a") + i - 10))
    lines = [f"### {spec['title']}", ""]
    lines.append(f"- Map: `{spec['map']}`. Layout: `data/layouts/{spec['layout']}/map.bin`, "
                 f"**{W}x{H}** blocks, `gTileset_Oikos` + `{TILESET}`.")
    floors = ", ".join([spec["floor"]] + list(spec.get("floors", {}).values()))
    walls = ", ".join([spec["wall"]] + list(spec.get("walls", {}).values()))
    lines.append(f"- Floor: {floors}. Wall: {walls}. Render: `design/oikoumene/img/{spec['render']}` (2x).")
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


def stamp_doc(ids, specs):
    """Each stamp's metatiles, where it first appears."""
    where = {}
    for cat, spec in specs.items():
        for (n, sx, sy) in spec["stamps"]:
            if n in where:
                continue
            st = CA.STAMPS[n]
            rows = []
            for cy in range(st["h"]):
                row = []
                for cx in range(st["w"]):
                    sub = cut(st["img"], cx, cy)
                    row.append(f"{ids[cat][sy + cy][sx + cx]:03X}" if not empty(sub) else "---")
                rows.append(" ".join(row))
            where[n] = (cat, " / ".join(rows))
    lines = ["| Stamp | Cells | Palette | From | Metatiles (where) | What it is |",
             "|---|---|---|---|---|---|"]
    for n, st in CA.STAMPS.items():
        if n not in where:
            continue
        cat, ids_ = where[n]
        lines.append(f"| `{n}` | {st['w']}x{st['h']} | {st['pal']} | {st.get('source', NAME)} | "
                     f"{ids_} ({cat}) | {st['note']} |")
    return "\n".join(lines)


def base_doc(order):
    index = {c.key(): FIRST_METATILE + i for i, c in enumerate(order)}
    lines = ["| Piece | Metatile |", "|---|---|"]
    for name, c in basic_cells():
        lines.append(f"| {name} | `{index[c.key()]:03X}` |")
    return "\n".join(lines)


def splice(path, text, tag, comment=("<!-- ", " -->")):
    begin = f"{comment[0]}{tag}: begin generated{comment[1]}"
    end = f"{comment[0]}{tag}: end generated{comment[1]}"
    doc = path.read_text()
    if begin not in doc:
        doc = doc.rstrip("\n") + f"\n\n{begin}\n{end}\n"
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


def check_spots(name, spec, cells):
    """oikia_build's check. A "perch" is someone placed on a piece of
    furniture, checked like a bg event from the tile you talk to them from. A
    "counter" is someone behind a counter, talked to across it: the tile you
    stand on must be reachable and the cell between must be MB_COUNTER."""
    spots = [("bg",) + tuple(s[1:]) if s[0] == "perch" else s for s in spec["spots"] if s[0] != "counter"]
    OB.check_spots(name, dict(spec, spots=spots), cells)
    probe = dict(spec, spots=[s for s in spec["spots"] if s[0] == "warp"]
                 + [("npc", s[1], (s[3][0], s[3][1]), s[3][2]) for s in spec["spots"] if s[0] == "counter"])
    OB.check_spots(name, probe, cells)
    for s in spec["spots"]:
        if s[0] == "counter":
            (x, y), (fx, fy, facing) = s[2], s[3]
            dx, dy = OB.DIRS[facing]
            assert (fx + 2 * dx, fy + 2 * dy) == (x, y), f"{name}: counter '{s[1]}' isn't across from {(fx, fy)}"
            mid = cells[fy + dy][fx + dx]
            assert mid.behavior == "MB_COUNTER", f"{name}: counter '{s[1]}': {(fx + dx, fy + dy)} isn't MB_COUNTER"


def all_rooms():
    rooms = {}
    for mod in room_modules():
        for n, spec in mod.ROOMS.items():
            assert n not in rooms, f"room {n} defined twice"
            rooms[n] = dict(spec, _module=mod)
    return rooms


def variant_script(spec, var, base_cells, base_ids, var_cells, var_ids):
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


def contact_sheet(renders, path):
    """Every room at 2x, laid out in two rows with its name under it."""
    pad, label_h = 16, 18
    order = list(renders.items())
    rows = [order[:3], order[3:]]
    widths = [sum(img.shape[1] for _, img in r) + pad * (len(r) + 1) for r in rows]
    heights = [max(img.shape[0] for _, img in r) + label_h + pad for r in rows]
    W, H = max(widths), sum(heights) + pad
    sheet = Image.new("RGB", (W, H), (24, 20, 28))
    draw = ImageDraw.Draw(sheet)
    y = pad
    for r, h in zip(rows, heights):
        x = pad
        for title, img in r:
            sheet.paste(Image.fromarray(img), (x, y))
            draw.text((x, y + img.shape[0] + 3), title, fill=(232, 216, 176))
            x += img.shape[1] + pad
        y += h
    sheet.save(path)


def build(args):
    check_palettes()
    rooms = all_rooms()
    cats = catalog()
    layouts = {n: compose(s) for n, s in list(rooms.items()) + list(cats.items())}
    for n, spec in rooms.items():
        check_spots(n, spec, layouts[n])
        for vname, var in spec.get("variants", {}).items():
            layouts[f"{n}@{vname}"] = compose(variant_spec(spec, var))
    order, ids = collect(layouts)
    log(f"{len(order)} unique metatiles")

    if args.preview:
        d = Path(args.preview)
        for n, cells in layouts.items():
            save_scaled(image_of(cells), d / f"{n.replace('@', '_')}.png", 2)

    if args.no_compile:
        for c in order:
            for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
                if layer is not None:
                    check_subtiles(layer, k)
        return rooms, layouts

    write_sources(order)
    porytiles()
    unshare_primary_tiles()
    nmeta, ntiles, pals = check_compiled()

    void_id = None
    for name, c in basic_cells():
        if name.startswith("void"):
            void_id = FIRST_METATILE + [o.key() for o in order].index(c.key())
    sizes, scripts, renders = {}, {}, {}
    for n, cells in layouts.items():
        H, W = len(cells), len(cells[0])
        blocks = blockdata(cells, ids[n])
        want = image_of(cells)
        got = {p: render_compiled(blocks, W, p) for p in (PRIMARY, "gTileset_Aethos", "gTileset_Building")}
        for p, img in got.items():
            if not np.array_equal(img, want):
                raise SystemExit(f"{NAME}: {n} renders differently on {p}")
        if n in rooms:
            spec = rooms[n]
            d = ROOT / "data/layouts" / spec["layout"]
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | SOLID] * 4, "<u2").tofile(d / "border.bin")
            save_scaled(got[PRIMARY], IMG / spec["render"], 2)
            big = np.array(Image.fromarray(got[PRIMARY]).resize((W * 32, H * 32), Image.NEAREST))
            renders[spec["title"]] = big
            sizes[spec["layout"]] = (W, H)
            log(f"{n} {W}x{H} -> data/layouts/{spec['layout']}, design/oikoumene/img/{spec['render']}")
        elif "@" in n:
            base, vname = n.split("@")
            spec = rooms[base]
            save_scaled(got[PRIMARY], IMG / spec["render"].replace(".png", f"_{vname}.png"), 2)
            scripts.setdefault(spec["layout"], []).append(
                variant_script(spec, spec["variants"][vname], layouts[base], ids[base], cells, ids[n]))
        elif n in cats:
            save_scaled(got[PRIMARY], IMG / f"{NAME}_catalog.png", 2)
    update_layouts_json(sizes)
    for layout, texts in scripts.items():
        pory = ROOT / "data/maps" / layout / "scripts.pory"
        splice(pory, f"// Written by tools/ichor/art/{NAME}_build.py; don't edit by hand.\n\n"
               + "\n\n".join(texts), tag=f"{NAME}_build", comment=("// ", ""))
    contact_sheet(renders, IMG / "pontos_rooms.png")
    sheet = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", NAME,
                            "--primary", "oikos", "--scale", "2", "-o", str(IMG / f"{NAME}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
    if sheet.returncode != 0:
        sys.stderr.write(sheet.stderr)
        raise SystemExit(f"{NAME}: sheet render failed")
    if DOC.exists():
        splice(DOC, "\n".join(room_doc(n, s, layouts[n]) for n, s in rooms.items()), tag=f"{NAME}_build")
        stats = (f"Built: **{len(order)}** metatiles (`0x200`-`{FIRST_METATILE + len(order) - 1:#05x}`) "
                 f"of 512, **{ntiles}** tiles of {MAX_TILES}, palettes {pals[0]}-{pals[-1]}.\n\n")
        specs = dict(cats)
        specs.update(rooms)
        splice(DOC, stats + base_doc(order) + "\n\n" + stamp_doc(ids, specs), tag=f"{NAME}_tiles")
    log(f"identical on oikos, aethos and building; {nmeta} metatiles, {ntiles} tiles, palettes {pals}")
    return rooms, layouts


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="compose and check only; leave Porytiles' files alone")
    ap.add_argument("--preview", metavar="DIR", help="also write source-composed previews here (2x)")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
