#!/usr/bin/env python3
"""Build gTileset_Megaron and the Troad's rooms laid out from it.

Works like oikia_build.py (design/phase1/TILES_oikia.md), whose generic parts it
reuses, and like world-act1's ergasteria_build.py, whose room format it takes
(a room may mix floors and walls, and have variants):

1. Compose every cell of every room in tools/ichor/maps/troad_rooms.py, and of
   a catalog of every piece, from megaron_art.py: floor or wall on the bottom
   layer, furniture on the middle layer, overhangs on the top layer.
2. Deduplicate the cells into metatiles and write Porytiles' sources to
   data/tilesets/secondary/megaron/porytiles_src/.
3. Compile with Porytiles, paired with gTileset_Aethos, and copy back any solid
   tile Porytiles borrowed from it, so megaron uses only its own tiles and
   palettes 6-12 and works on any primary.
4. Check that, render every room on oikos, aethos and building, and fail
   unless the renders match each other and the composed source.
5. Write each room's map.bin and border.bin and its layouts.json size and
   tilesets, the 2x renders in design/oikoumene/img/, the contact sheet, the
   generated tables in design/oikoumene/ROOMS_troad.md, and each variant's
   setmetatile script in its map's scripts.pory.

Rooms are data in Python: the builder rewrites their blockdata on every run, so
metatile ids may move freely. Re-dress a room in troad_rooms.py, not Porymap.

Usage: /usr/bin/python3 tools/ichor/art/megaron_build.py [--no-compile] [--preview DIR]
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

import megaron_art as A  # noqa: E402
import oikia_build as OB  # noqa: E402  (Cell, over, cut, check_spots, ...)

NAME = "megaron"
TILESET = "gTileset_Megaron"
PARTNER = "gTileset_Aethos"
PRIMARY = "gTileset_Oikos"
TS = ROOT / "data/tilesets/secondary" / NAME
SRC = TS / "porytiles_src"
BIN = TS / "porytiles_bin"
IMG = ROOT / "design/oikoumene/img"
DOC = ROOT / "design/oikoumene/ROOMS_troad.md"
MAGENTA = np.array([255, 0, 255], np.uint8)
FIRST_METATILE = 0x200
FIRST_TILE = 512
SECONDARY_PALS = range(6, 13)
MAX_METATILES = 512
MAX_TILES = 504                     # door animations overwrite tiles 504-511

WALK, SOLID, WARP = OB.WALK, OB.SOLID, OB.WARP
Cell, over, empty, cut = OB.Cell, OB.over, OB.empty, OB.cut
PAL_SETS = {n: set(p.values()) for n, p in A.PALETTES.items()}


def log(msg):
    print(f"{NAME}: {msg}")


# --------------------------------------------------------------------------
# Composition: oikia's composer, generalized as ergasteria's is.
#   grid chars: '.' the room's floor; any key of spec["floors"] another floor;
#               'W' the room's wall; any key of spec["walls"] another wall;
#               '#' void.
# --------------------------------------------------------------------------

def compose(spec):
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
        st = A.STAMPS[name]
        for cy in range(st["h"]):
            for cx in range(st["w"]):
                x, y = sx + cx, sy + cy
                if not (0 <= x < W and 0 <= y < H):
                    raise ValueError(f"{spec['title']}: {name} at ({sx},{sy}) runs off the room")
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
                raise ValueError(f"{spec['title']}: ({x},{y}) would need three layers")
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
    for name, pal in A.PALETTES.items():
        assert len(pal) <= 15, f"palette {name} has {len(pal)} colors"
        for ch, rgb in pal.items():
            assert all(v % 8 == 0 for v in rgb), f"{name}.{ch} {rgb} is not a multiple of 8"
            assert rgb not in taken, f"{name}.{ch} {rgb} is also an aethos color"
            assert rgb != (255, 0, 255), "magenta is Porytiles' transparency"


def check_subtiles(layer, where):
    for qy in (0, 8):
        for qx in (0, 8):
            q = layer[qy:qy + 8, qx:qx + 8]
            cols = {tuple(int(v) for v in c) for c in q[q[..., 3] > 0][:, :3]}
            if cols and not any(cols <= s for s in PAL_SETS.values()):
                raise ValueError(f"8x8 tile at {where} +({qx},{qy}) mixes palettes: {sorted(cols)}")


# --------------------------------------------------------------------------
# Tileset sources
# --------------------------------------------------------------------------

def basic_cells():
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


def porytiles():
    exe = shutil.which("porytiles") or os.path.expanduser("~/.local/bin/porytiles")
    # Porytiles compiles a secondary only against a primary it manages, so
    # megaron is paired with aethos, as oikia is; unshare_primary_tiles and
    # check_compiled make sure it keeps no aethos tile or palette.
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
    into megaron's own tiles.png."""
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
    log(f"compiled {len(meta)} metatiles, {used} tiles, palettes {sorted(pals)}")
    return len(meta), used, sorted(pals)


# --------------------------------------------------------------------------
# The catalog: every piece on the floor or wall it stands on, so the sheet
# shows the whole set and a room can be re-dressed from it.
# --------------------------------------------------------------------------

def catalog():
    wall_hung = [n for n, s in A.STAMPS.items() if n in WALL_PIECES]
    free = [n for n in A.STAMPS if n not in WALL_PIECES and n not in ("mat",)]
    width = 26
    placed, x = [], 0
    for n in wall_hung:
        w, h = A.STAMPS[n]["w"], A.STAMPS[n]["h"]
        if x + w > width:
            break
        placed.append((n, x, 0 if h <= 2 else 0))
        x += w
    rest = wall_hung[len(placed):]
    rows_used, y, x, rowh = [], 3, 1, 0
    for n in rest + free:
        w, h = A.STAMPS[n]["w"], A.STAMPS[n]["h"]
        if x + w > width - 1:
            x, y, rowh = 1, y + rowh + 1, 0
        placed.append((n, x, y))
        x += w + 1
        rowh = max(rowh, h)
    height = y + rowh + 5
    placed.append(("mat", 1, height - 1))
    grid = ["W" * width, "W" * width] + ["." * width for _ in range(height - 2)]
    return {"catalog": {
        "title": "Catalog: every megaron piece on painted plaster",
        "floor": "plaster", "wall": "fresco", "grid": grid,
        "rugs": [("kilim", 4, height - 4, 3, 3)],
        "stamps": placed, "spots": [],
    }}


WALL_PIECES = {"window", "rod", "sea_window", "slit", "slit_draught", "stair", "horse_fresco", "fresco_troy",
               "bridles", "tools", "skeins", "shield", "wreath", "floats", "nets", "hay_rack"}


# --------------------------------------------------------------------------
# Rendering, layouts, docs
# --------------------------------------------------------------------------

def render_compiled(blocks, width, primary):
    import render_map as RM
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(primary, syms)),
                    RM.Tileset(RM.resolve_tileset(TILESET, syms)))
    return np.array(RM.render_blocks(r, blocks, width))


save_scaled = OB.save_scaled


def update_layouts_json(sizes, primary=PRIMARY):
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
    floors = ", ".join(dict.fromkeys([spec["floor"]] + list(spec.get("floors", {}).values())))
    walls = ", ".join(dict.fromkeys([spec["wall"]] + list(spec.get("walls", {}).values())))
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


def stamp_doc(composed, ids, layouts_order):
    where = {}
    for lname, spec in layouts_order:
        for (n, sx, sy) in spec["stamps"]:
            if n in where:
                continue
            st = A.STAMPS[n]
            rows = []
            for cy in range(st["h"]):
                row = []
                for cx in range(st["w"]):
                    sub = cut(st["img"], cx, cy)
                    tp = cut(st["top"], cx, cy) if st["top"] is not None else None
                    row.append(f"{ids[lname][sy + cy][sx + cx]:03X}" if not (empty(sub) and empty(tp)) else "---")
                rows.append(" ".join(row))
            where[n] = " / ".join(rows)
    lines = ["| Stamp | Cells | Palette | From | Metatiles (in the catalog) | What it is |",
             "|---|---|---|---|---|---|"]
    for n, st in A.STAMPS.items():
        if n in where:
            lines.append(f"| `{n}` | {st['w']}x{st['h']} | {st['pal']} | {st.get('source', NAME)} | "
                         f"{where[n]} | {st['note']} |")
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
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])


def check_spots(name, spec, cells):
    """oikia_build's check. A "perch" is someone placed on furniture, talked
    to from the tile given, like a bg event."""
    spots = [("bg",) + tuple(s[1:]) if s[0] == "perch" else s for s in spec["spots"] if s[0] != "counter"]
    OB.check_spots(name, dict(spec, spots=spots), cells)
    # Someone behind a counter: talked to from two tiles away, across a cell
    # whose behavior is MB_COUNTER, as at a vanilla Mart.
    probe = [s for s in spec["spots"] if s[0] in ("warp", "counter")]
    for spot in spec["spots"]:
        if spot[0] != "counter":
            continue
        at, (fx, fy, facing) = spot[2], spot[3]
        dx, dy = OB.DIRS[facing]
        mid = cells[fy + dy][fx + dx]
        assert mid.behavior == "MB_COUNTER", f"{name}: '{spot[1]}': ({fx + dx},{fy + dy}) is not a counter"
        assert (fx + 2 * dx, fy + 2 * dy) == at, f"{name}: '{spot[1]}': ({fx},{fy}) facing {facing} misses {at}"
        assert cells[at[1]][at[0]].block != SOLID, f"{name}: '{spot[1]}' stands on a solid cell {at}"
        OB.check_spots(name, dict(spec, spots=[probe[0], ("npc", spot[1] + " (talk spot)", (fx, fy), facing)]), cells)


def variant_script(var, base_cells, base_ids, var_cells, var_ids):
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
    """Every room at 1x on one sheet, labelled, then saved at 2x."""
    pad, label_h, cols = 8, 12, 4
    items = list(renders.items())
    col_w = max(img.shape[1] for _, img in items)
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    heights = [max(img.shape[0] for _, img in row) + label_h for row in rows]
    W = cols * (col_w + pad) + pad
    H = sum(heights) + pad * (len(rows) + 1)
    sheet = Image.new("RGB", (W, H), (24, 20, 20))
    d = ImageDraw.Draw(sheet)
    y = pad
    for row, rh in zip(rows, heights):
        x = pad
        for title, img in row:
            d.text((x, y), title, fill=(232, 224, 200))
            sheet.paste(Image.fromarray(img), (x, y + label_h))
            x += col_w + pad
        y += rh + pad
    sheet = sheet.resize((W * 2, H * 2), Image.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def build(args):
    import troad_rooms
    check_palettes()
    rooms = troad_rooms.ROOMS
    cats = catalog()
    layouts = {}
    for n, s in list(rooms.items()) + list(cats.items()):
        layouts[n] = compose(s)
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
        blocks = OB.blockdata(cells, ids[n])
        want = image_of(cells)
        got = {p: render_compiled(blocks, W, p) for p in (PRIMARY, "gTileset_Aethos", "gTileset_Building")}
        for p, img in got.items():
            if not np.array_equal(img, want):
                raise SystemExit(f"{NAME}: {n} renders differently on {p} than composed")
        if n in rooms:
            spec = rooms[n]
            d = ROOT / "data/layouts" / spec["layout"]
            d.mkdir(parents=True, exist_ok=True)
            blocks.tofile(d / "map.bin")
            np.array([void_id | SOLID] * 4, "<u2").tofile(d / "border.bin")
            save_scaled(got[PRIMARY], IMG / spec["render"], 2)
            renders[spec["title"].split(":")[0]] = got[PRIMARY]
            sizes[spec["layout"]] = (W, H)
            log(f"{n} {W}x{H} -> data/layouts/{spec['layout']}, design/oikoumene/img/{spec['render']}")
        elif "@" in n:
            base, vname = n.split("@")
            spec = rooms[base]
            save_scaled(got[PRIMARY], IMG / spec["render"].replace(".png", f"_{vname}.png"), 2)
            scripts.setdefault(spec["layout"], []).append(
                variant_script(spec["variants"][vname], layouts[base], ids[base], cells, ids[n]))
        else:
            save_scaled(got[PRIMARY], IMG / f"megaron_{n}.png", 2)
    update_layouts_json(sizes)
    for layout, texts in scripts.items():
        pory = ROOT / "data/maps" / layout / "scripts.pory"
        splice(pory, f"// Written by tools/ichor/art/{NAME}_build.py; don't edit by hand.\n\n"
               + "\n\n".join(texts), tag=f"{NAME}_build", comment=("// ", ""))
    contact_sheet(renders, IMG / "troad_rooms.png")
    sheet = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", NAME,
                            "--primary", "oikos", "--scale", "2", "-o", str(IMG / f"{NAME}_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
    if sheet.returncode != 0:
        sys.stderr.write(sheet.stderr)
        raise SystemExit(f"{NAME}: sheet render failed")
    if DOC.exists():
        splice(DOC, "\n".join(room_doc(n, s, layouts[n]) for n, s in rooms.items()), tag=f"{NAME}_build rooms")
        stats = (f"Built: **{len(order)}** metatiles (`0x200`-`{FIRST_METATILE + len(order) - 1:#05x}`) "
                 f"of 512, **{ntiles}** tiles of {MAX_TILES}, palettes {pals[0]}-{pals[-1]}.\n\n")
        splice(DOC, stats + base_doc(order) + "\n\n" + stamp_doc(layouts, ids, list(cats.items()) + list(rooms.items())),
               tag=f"{NAME}_build tiles")
    log(f"identical on oikos, aethos and building; {nmeta} metatiles, {ntiles} tiles, palettes {pals}")
    return rooms, layouts


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="compose and check only; leave Porytiles' files alone")
    ap.add_argument("--preview", metavar="DIR", help="also write source-composed previews here (2x)")
    return ap.parse_args()


if __name__ == "__main__":
    build(parse_args())
