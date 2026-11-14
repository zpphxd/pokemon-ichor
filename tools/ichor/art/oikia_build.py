#!/usr/bin/env python3
"""Build gTileset_Oikia and the Phase 1 home rooms.

1. Compose every cell of every room, and of the catalog layouts, from the
   pieces in oikia_art.py (floor or wall on the bottom layer, furniture on the
   middle layer, overhangs on the top layer).
2. Deduplicate the cells into metatiles and write Porytiles' sources:
   data/tilesets/secondary/oikia/porytiles_src/{bottom,middle,top}.png and
   attributes.csv.
3. Compile with Porytiles, paired with gTileset_Aethos.
4. Check the result: every 8x8 tile fits one oikia palette, the compiled
   metatiles use only oikia's own tiles and palettes 6-12, and every room
   renders the same on the aethos and building primaries as it was composed.
5. Write each room's blockdata to design/phase1/rooms/<room>.bin and render
   it to design/phase1/img/rooms_<room>.png (3x), plus the metatile sheet
   and catalog images.

Usage: /usr/bin/python3 tools/ichor/art/oikia_build.py [--no-compile]
"""
import argparse
import hashlib
import json
import os
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

import oikia_art as A  # noqa: E402
import oikia_rooms as R  # noqa: E402

TILESET = "gTileset_Oikia"
PARTNER = "gTileset_Aethos"
TS = ROOT / "data/tilesets/secondary/oikia"
SRC = TS / "porytiles_src"
BIN = TS / "porytiles_bin"
ROOMS_DIR = ROOT / "design/phase1/rooms"
IMG = ROOT / "design/phase1/img"
MAGENTA = np.array([255, 0, 255], np.uint8)
FIRST_METATILE = 0x200
FIRST_TILE = 512
SECONDARY_PALS = range(6, 13)
MAX_METATILES = 512
MAX_TILES = 512

# Collision and elevation, as in vanilla interiors: floor is passable at
# elevation 3, furniture and walls are blocked at elevation 0, warp tiles are
# passable at elevation 0.
WALK, SOLID, WARP = 0x3000, 0x0400, 0x0000


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------

class Cell:
    def __init__(self):
        self.bottom = None   # (16,16,4), opaque
        self.middle = None
        self.top = None
        self.behavior = "MB_NORMAL"
        self.block = WALK
        self.covered = False

    def key(self):
        h = hashlib.sha1()
        for layer in (self.bottom, self.middle, self.top):
            h.update(b"-" if layer is None else layer.tobytes())
        h.update(self.behavior.encode())
        return h.hexdigest()


def over(dst, src):
    """Alpha-composite src onto dst (both (16,16,4))."""
    out = dst.copy()
    m = src[..., 3] > 0
    out[m] = src[m]
    return out


def empty(img):
    return img is None or not (img[..., 3] > 0).any()


def cut(img, cx, cy):
    return img[cy * 16:(cy + 1) * 16, cx * 16:(cx + 1) * 16]


def alt_floor(x, y):
    """A sprinkling of the alternate floor tile on empty floor."""
    return ((x * 7 + y * 11 + x * y * 3) % 6) == 0


def compose(spec, stamps=A.STAMPS):
    grid = spec["grid"]
    H, W = len(grid), len(grid[0])
    assert all(len(r) == W for r in grid), "ragged grid"
    cells = [[Cell() for _ in range(W)] for _ in range(H)]
    floors = A.FLOORS[spec["floor"]]
    wall = A.WALLS[spec["wall"]]

    def ch(x, y):
        return grid[y][x] if 0 <= x < W and 0 <= y < H else "#"

    # stamps: middle / top layers, collision and behavior
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
                c.covered = True
                if (cx, cy) in st["walk"]:
                    c.block = WARP if (cx, cy) in st["behavior"] else WALK
                else:
                    c.block = SOLID
                if (cx, cy) in st["behavior"]:
                    c.behavior = st["behavior"][(cx, cy)]

    # rugs
    rug_at = {}
    for (design, rx, ry, rw, rh) in spec.get("rugs", []):
        assert rw >= 2 and rh >= 2, "rugs are at least 2x2"
        img = A.RUGS[design]
        for j in range(rh):
            for i in range(rw):
                pi = 0 if i == 0 else 2 if i == rw - 1 else 1
                pj = 0 if j == 0 else 2 if j == rh - 1 else 1
                rug_at[(rx + i, ry + j)] = cut(img, pi, pj)

    # bottom layer
    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            g = ch(x, y)
            if g == "W":
                k = 0
                while ch(x, y - 1 - k) == "W":
                    k += 1
                c.bottom = cut(wall, 0, min(k, 1)).copy()
                if not c.covered:
                    c.block = SOLID   # a stamp's walk cell (stairs) stays open
            elif g == "#":
                c.bottom = A.VOID.copy()
                if not c.covered:
                    c.block = SOLID
            elif (x, y) in rug_at:
                c.bottom = rug_at[(x, y)].copy()
            else:
                top_sh = ch(x, y - 1) != "."
                left_sh = ch(x - 1, y) != "."
                if top_sh and left_sh:
                    v = "corner"
                elif top_sh:
                    v = "top"
                elif left_sh:
                    v = "left"
                elif "alt" in floors and not c.covered and alt_floor(x, y):
                    v = "alt"
                else:
                    v = "plain"
                c.bottom = floors[v].copy()
            if hasattr(c, "flat"):
                c.bottom = over(c.bottom, c.flat)
            assert (c.bottom[..., 3] == 255).all(), f"hole in bottom layer at ({x},{y})"
            if c.middle is not None and c.top is not None:
                raise ValueError(f"({x},{y}) would need three layers; flatten the stamp")
    return cells


def image_of(cells):
    H, W = len(cells), len(cells[0])
    out = np.zeros((H * 16, W * 16, 3), np.uint8)
    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            px = c.bottom.copy()
            for layer in (c.middle, c.top):
                if layer is not None:
                    px = over(px, layer)
            out[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = px[..., :3]
    return out


# --------------------------------------------------------------------------
# Checks on the art
# --------------------------------------------------------------------------

def aethos_colors():
    out = set()
    for i in range(6):
        p = ROOT / f"data/tilesets/primary/aethos/porytiles_bin/palettes/{i:02d}.pal"
        vals = [int(v) for v in p.read_text().split()[3:]]
        for j in range(1, 16):
            out.add(tuple(vals[j * 3:j * 3 + 3]))
    return out


def check_palettes():
    taken = aethos_colors()
    for name, pal in A.PALETTES.items():
        assert len(pal) <= 15, f"palette {name} has {len(pal)} colors"
        for ch, rgb in pal.items():
            assert all(v % 8 == 0 for v in rgb), f"{name}.{ch} {rgb} is not a multiple of 8"
            assert rgb not in taken, f"{name}.{ch} {rgb} is also an aethos color"
            assert rgb != (255, 0, 255), "magenta is Porytiles' transparency"


PAL_SETS = {n: set(p.values()) for n, p in A.PALETTES.items()}


def check_subtiles(layer, where):
    for qy in (0, 8):
        for qx in (0, 8):
            q = layer[qy:qy + 8, qx:qx + 8]
            cols = {tuple(c) for c in q[q[..., 3] > 0][:, :3]}
            if not cols:
                continue
            if not any(cols <= s for s in PAL_SETS.values()):
                raise ValueError(f"8x8 tile at {where} +({qx},{qy}) mixes palettes: {sorted(cols)}")


# --------------------------------------------------------------------------
# Tileset sources
# --------------------------------------------------------------------------

def basics():
    """The bare floors, walls, void and rug pieces, listed first in the sheet."""
    out = []
    for mat, vs in A.FLOORS.items():
        for v in ("plain", "alt", "top", "left", "corner"):
            if v in vs:
                c = Cell()
                c.bottom = vs[v]
                out.append(c)
    for style, img in A.WALLS.items():
        for k in (0, 1):
            c = Cell()
            c.bottom = cut(img, 0, k).copy()
            c.block = SOLID
            out.append(c)
    c = Cell()
    c.bottom = A.VOID
    c.block = SOLID
    out.append(c)
    for design, img in A.RUGS.items():
        for pj in range(3):
            for pi in range(3):
                c = Cell()
                c.bottom = cut(img, pi, pj).copy()
                out.append(c)
    return out


def collect(layouts):
    """Assign metatile ids to unique cells, basics first, then each layout."""
    order, index = [], {}

    def add(c):
        k = c.key()
        if k not in index:
            index[k] = len(order)
            order.append(c)
        return index[k]

    for c in basics():
        add(c)
    ids = {}
    for name, cells in layouts.items():
        ids[name] = [[FIRST_METATILE + add(c) for c in row] for row in cells]
    return order, ids


def write_sources(order):
    n = len(order)
    if n > MAX_METATILES:
        raise SystemExit(f"oikia: {n} metatiles is over the {MAX_METATILES} limit")
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
    print(f"oikia: {n} metatiles written to {SRC.relative_to(ROOT)}")


def porytiles():
    exe = shutil.which("porytiles") or os.path.expanduser("~/.local/bin/porytiles")
    # Porytiles only compiles a secondary against a primary it manages, so
    # oikia is paired with aethos. It never borrows aethos tiles or palettes
    # (check_compiled proves that), so aethos's own checksum cache, which can
    # lag its committed sources, is not verified here.
    cmd = [exe, "compile-tileset", TILESET,
           "--primary-pairing-mode", "manual", "--primary-pairing-partners", PARTNER,
           "--no-verify-checksums"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit("oikia: porytiles failed")
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr).strip())


def tiles_of(arr):
    h, w = arr.shape
    return arr.reshape(h // 8, 8, w // 8, 8).swapaxes(1, 2).reshape(-1, 8, 8)


def unshare_primary_tiles():
    """Give oikia its own copy of every tile Porytiles borrowed from aethos.

    When it compiles a secondary, Porytiles reuses any primary tile whose 4bpp
    pattern matches (in practice, solid-color tiles), drawn with a secondary
    palette. That works on aethos only. Copy each borrowed tile into oikia's
    tiles.png and repoint the metatiles at the copy, so oikia renders the same
    on any primary. Then refresh Porytiles' cache so its state stays coherent.
    """
    prim = tiles_of(np.array(Image.open(ROOT / "data/tilesets/primary/aethos/porytiles_bin/tiles.png")) % 16)
    im = Image.open(BIN / "tiles.png")
    assert im.mode == "P"
    own = list(tiles_of(np.array(im)))
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
    data = json.loads(cache.read_text())
    for f in ("tiles.png", "metatiles.bin"):
        key = str((BIN / f).relative_to(ROOT))
        if key in data:
            data[key] = hashlib.md5((BIN / f).read_bytes()).hexdigest()
    cache.write_text(json.dumps(data, indent=2) + "\n")
    print(f"oikia: copied {len(copies)} solid tiles Porytiles had borrowed from aethos")
    return len(copies)


def check_compiled():
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    bad = []
    pals = set()
    for i, row in enumerate(meta):
        for e in row:
            idx, pal = int(e) & 0x3FF, int(e) >> 12
            if idx == 0:
                continue  # the transparent tile
            if idx < FIRST_TILE or pal not in SECONDARY_PALS:
                bad.append((FIRST_METATILE + i, idx, pal))
            pals.add(pal)
    if bad:
        raise SystemExit(f"oikia: metatiles reach outside oikia: {bad[:8]}")
    tiles = Image.open(BIN / "tiles.png")
    ntiles = (tiles.width // 8) * (tiles.height // 8)
    if ntiles > MAX_TILES:
        raise SystemExit(f"oikia: {ntiles} tiles is over the {MAX_TILES} limit")
    print(f"oikia: compiled {len(meta)} metatiles, {ntiles} tiles, palettes {sorted(pals)}")
    return len(meta), ntiles, sorted(pals)


# --------------------------------------------------------------------------
# Rooms
# --------------------------------------------------------------------------

DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}


def check_spots(name, spec, cells):
    """Every warp, NPC, coord and bg-reading tile is walkable and reachable
    from the room's first warp, and each bg is read from the tile in front."""
    H, W = len(cells), len(cells[0])

    def open_(x, y):
        return 0 <= x < W and 0 <= y < H and cells[y][x].block != SOLID

    warps = [s for s in spec["spots"] if s[0] == "warp"]
    if not warps:
        return
    start = warps[0][2][0]
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in DIRS.values():
            n = (x + dx, y + dy)
            if n not in seen and open_(*n):
                seen.add(n)
                todo.append(n)
    for spot in spec["spots"]:
        kind, label = spot[0], spot[1]
        if kind == "warp":
            for t in spot[2]:
                assert t in seen, f"{name}: warp '{label}' at {t} is unreachable"
                assert cells[t[1]][t[0]].behavior != "MB_NORMAL", f"{name}: {t} is not a warp tile"
        elif kind in ("npc", "coord"):
            assert spot[2] in seen, f"{name}: {kind} '{label}' at {spot[2]} is unreachable"
        elif kind == "bg":
            at, (fx, fy, facing) = spot[2], spot[3]
            assert (fx, fy) in seen, f"{name}: bg '{label}' is read from {(fx, fy)}, which is unreachable"
            dx, dy = DIRS[facing]
            assert (fx + dx, fy + dy) == at, f"{name}: bg '{label}': {(fx, fy)} facing {facing} misses {at}"


def room_doc(name, spec, cells):
    """Markdown for one room: size, files, an ASCII walk map and its spots."""
    H, W = len(cells), len(cells[0])
    marks = {}
    for i, spot in enumerate(spec["spots"], 1):
        tiles = spot[2] if spot[0] == "warp" else [spot[2]]
        for t in tiles:
            marks.setdefault(t, str(i) if i < 10 else chr(ord("a") + i - 10))
    lines = [f"### {spec['title']}", ""]
    lines.append(f"- Map: `{spec['map']}`. Layout: `design/phase1/rooms/{name}.bin`, "
                 f"**{W}x{H}** blocks, secondary `gTileset_Oikia`.")
    lines.append(f"- Floor: {spec['floor']}. Wall: {spec['wall']} dado. "
                 f"Render: `design/phase1/img/rooms_{name}.png` (3x).")
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
            tile = ", ".join(f"({x},{y})" for x, y in spot[2])
            frm = ""
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


def stamp_doc(composed, ids):
    """Markdown table: every stamp with its metatile ids on each catalog."""
    where = {}
    for cat in ("catalog_terracotta", "catalog_boards", "catalog_flags"):
        spec = R.catalog(A.STAMPS)[cat]
        for (n, sx, sy) in spec["stamps"]:
            st = A.STAMPS[n]
            rows = []
            for cy in range(st["h"]):
                row = []
                for cx in range(st["w"]):
                    sub = cut(st["img"], cx, cy)
                    row.append(f"{ids[cat][sy + cy][sx + cx]:03X}" if not empty(sub) else "---")
                rows.append(" ".join(row))
            where.setdefault(n, {})[cat.split("_")[1]] = " / ".join(rows)
    lines = ["| Stamp | Cells | Palette | Terracotta, red wall | Boards, blue wall | Flags, red wall | What it is |",
             "|---|---|---|---|---|---|---|"]
    for n, st in A.STAMPS.items():
        w = where.get(n, {})
        lines.append(f"| `{n}` | {st['w']}x{st['h']} | {st['pal']} | {w.get('terracotta', '')} | "
                     f"{w.get('boards', '')} | {w.get('flags', '')} | {st['note']} |")
    return "\n".join(lines)


def base_doc(order):
    """Markdown table of the bare floors, walls, void and rug pieces."""
    index = {c.key(): FIRST_METATILE + i for i, c in enumerate(order)}
    b = basics()
    names = []
    for mat, vs in A.FLOORS.items():
        for v in ("plain", "alt", "top", "left", "corner"):
            if v in vs:
                names.append(f"floor {mat}, {v}")
    for style in A.WALLS:
        names += [f"wall {style}, upper", f"wall {style}, lower"]
    names.append("void (outside the room)")
    for design in A.RUGS:
        for part in ("top-left", "top", "top-right", "left", "middle", "right",
                     "bottom-left", "bottom", "bottom-right"):
            names.append(f"rug {design}, {part}")
    lines = ["| Piece | Metatile |", "|---|---|"]
    for name, c in zip(names, b):
        lines.append(f"| {name} | `{index[c.key()]:03X}` |")
    return "\n".join(lines)


def splice(path, text):
    """Replace the generated section of a hand-written doc."""
    begin, end = "<!-- oikia_build: begin generated -->", "<!-- oikia_build: end generated -->"
    doc = path.read_text()
    a, b = doc.index(begin) + len(begin), doc.index(end)
    path.write_text(doc[:a] + "\n\n" + text.strip() + "\n\n" + doc[b:])

def blockdata(cells, ids):
    H, W = len(cells), len(cells[0])
    out = np.zeros(H * W, "<u2")
    for y in range(H):
        for x in range(W):
            out[y * W + x] = ids[y][x] | cells[y][x].block
    return out


def render_compiled(blocks, width, primary):
    import render_map as RM
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(primary, syms)),
                    RM.Tileset(RM.resolve_tileset(TILESET, syms)))
    return np.array(RM.render_blocks(r, blocks, width))


def save_scaled(arr, path, scale):
    im = Image.fromarray(arr)
    if scale > 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="compose and preview only; leave Porytiles' files alone")
    ap.add_argument("--preview", metavar="DIR", help="also write source-composed previews here")
    args = ap.parse_args()

    check_palettes()
    rooms = dict(R.ROOMS)
    cats = R.catalog(A.STAMPS)
    composed = {n: compose(s) for n, s in list(rooms.items()) + list(cats.items())}
    for n, spec in rooms.items():
        check_spots(n, spec, composed[n])
    order, ids = collect(composed)
    print(f"oikia: {len(order)} unique metatiles")

    if args.preview:
        d = Path(args.preview)
        for n, cells in composed.items():
            save_scaled(image_of(cells), d / f"{n}.png", 3)

    if args.no_compile:
        for c in order:
            for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
                if layer is not None:
                    check_subtiles(layer, k)
        return

    write_sources(order)
    porytiles()
    unshare_primary_tiles()
    nmeta, ntiles, pals = check_compiled()

    ROOMS_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}
    for n, cells in composed.items():
        H, W = len(cells), len(cells[0])
        blocks = blockdata(cells, ids[n])
        want = image_of(cells)
        got_a = render_compiled(blocks, W, "gTileset_Aethos")
        got_b = render_compiled(blocks, W, "gTileset_Building")
        if not np.array_equal(got_a, want):
            raise SystemExit(f"oikia: {n} does not render as composed")
        if not np.array_equal(got_a, got_b):
            raise SystemExit(f"oikia: {n} renders differently on the building primary")
        if n in rooms:
            blocks.tofile(ROOMS_DIR / f"{n}.bin")
            save_scaled(got_a, IMG / f"rooms_{n}.png", 3)
            summary[n] = {"width": W, "height": H}
    save_scaled(render_compiled(blockdata(composed["catalog_terracotta"], ids["catalog_terracotta"]),
                                len(composed["catalog_terracotta"][0]), "gTileset_Aethos"),
                IMG / "oikia_catalog.png", 2)
    sheet = subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "oikia",
                            "--primary", "aethos", "--scale", "2", "-o", str(IMG / "oikia_sheet.png")],
                           cwd=ROOT, capture_output=True, text=True)
    if sheet.returncode != 0:
        sys.stderr.write(sheet.stderr)
        raise SystemExit("oikia: sheet render failed")
    ROOMS_DOC = ROOT / "design/phase1/ROOMS_oikia.md"
    TILES_DOC = ROOT / "design/phase1/TILES_oikia.md"
    if ROOMS_DOC.exists():
        splice(ROOMS_DOC, "\n".join(room_doc(n, s, composed[n]) for n, s in rooms.items()))
    if TILES_DOC.exists():
        used = len({int(e) & 0x3FF for e in np.fromfile(BIN / "metatiles.bin", "<u2")
                    if int(e) & 0x3FF >= FIRST_TILE})
        stats = (f"Built: **{len(order)}** metatiles (`0x200`-`{FIRST_METATILE + len(order) - 1:#05x}`) "
                 f"of 512, **{used}** tiles of 512, palettes {pals[0]}-{pals[-1]}.\n\n")
        splice(TILES_DOC, stats + base_doc(order) + "\n\n" + stamp_doc(composed, ids))
    print(f"oikia: rooms {json.dumps(summary)}")
    print(f"oikia: identical on aethos and building; {nmeta} metatiles, {ntiles} tiles, palettes {pals}")


if __name__ == "__main__":
    main()
