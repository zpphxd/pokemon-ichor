#!/usr/bin/env python3
"""Compose, compile and check the road west's room secondaries.

The machinery behind tools/ichor/maps/westrooms.py, which holds the rooms and
is the script to run. Adapted from thyrsa_rooms_build.py (batch 1's rooms),
which follows oikia_build.py and emporion_build.py:

1. compose()   builds every cell of a room: the floor, wall or void on the
               bottom layer (with any flattened art), furniture on the middle
               layer, overhangs on the top layer, plus collision and behavior.
2. collect()   deduplicates cells into metatiles from 0x200, the bare floors
               and walls first.
3. write_sources() writes porytiles_src/{bottom,middle,top}.png and
               attributes.csv, checking that every 8x8 tile takes its colors
               from one palette.
4. compile()   runs Porytiles in build/<dir>_porytiles against an empty
               primary, so the set uses only its own tiles and palettes 6-12.
5. verify()    checks every metatile entry and the tile budget (504: interior
               secondaries keep 504-511 clear for door animations).
6. render()    draws a layout from the compiled tiles over gTileset_Oikos, the
               rooms' real primary.
"""
from __future__ import annotations

import hashlib
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

import westrooms_art as A  # noqa: E402

# Nine rooms of new art come to about 1,200 tiles; one secondary holds 504. So
# they are split over three secondaries, grouped by the art they share
# (tools/ichor/maps/westrooms.py says which room uses which). use() points this
# module at one.
TILESETS = {
    "stone": ("gTileset_WestStone", "west_stone"),      # Lebadeia's pilgrims' hall and mason's: rock, rubble, cut stone
    "harbor": ("gTileset_WestHarbor", "west_harbor"),   # Kirrha's inn, stall, muleteer's and sweeper's
    "homes": ("gTileset_WestHomes", "west_homes"),      # Herkyna's river house, Tisamenos's and Helike's
}


def use(which):
    global SYMBOL, DIR, TS, SRC, BIN, CFG, SCRATCH
    SYMBOL, DIR = TILESETS[which]
    TS = ROOT / "data/tilesets/secondary" / DIR
    SRC = TS / "porytiles_src"
    BIN = TS / "porytiles_bin"
    CFG = ROOT / "porytiles/tilesets" / SYMBOL
    SCRATCH = ROOT / f"build/{DIR}_porytiles"


use("stone")
FIRST_METATILE = 0x200
FIRST_TILE = 512
TILE_LIMIT = 504
MAX_METATILES = 512
MAGENTA = (255, 0, 255)

# Collision and elevation, as in vanilla interiors: floor is passable at
# elevation 3, walls and furniture are blocked, warp tiles are passable at 0.
WALK, SOLID, WARP = 0x3000, 0x0400, 0x0000


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------

class Cell:
    __slots__ = ("bottom", "middle", "top", "flat", "behavior", "block", "covered", "kind")

    def __init__(self):
        self.bottom = None
        self.middle = None
        self.top = None
        self.flat = None
        self.behavior = "MB_NORMAL"
        self.block = WALK
        self.covered = False
        self.kind = "floor"

    def key(self):
        h = hashlib.sha1()
        for layer in (self.bottom, self.middle, self.top):
            h.update(b"-" if layer is None else layer.tobytes())
        h.update(self.behavior.encode())
        return h.hexdigest()


def cut(img, cx, cy):
    return img[cy * 16:(cy + 1) * 16, cx * 16:(cx + 1) * 16]


def empty(img):
    return img is None or not (img[..., 3] > 0).any()


def alt_floor(x, y):
    return ((x * 7 + y * 11 + x * y * 3) % 6) == 0


def compose(spec, stamps=None):
    stamps = stamps or A.STAMPS
    grid = spec["grid"]
    H, W = len(grid), len(grid[0])
    assert all(len(r) == W for r in grid), f"{spec.get('title')}: ragged grid"
    floors = spec.get("floors") or {".": spec["floor"]}
    walls = spec.get("walls") or {"W": spec["wall"]}
    cells = [[Cell() for _ in range(W)] for _ in range(H)]

    def ch(x, y):
        return grid[y][x] if 0 <= x < W and 0 <= y < H else "#"

    # stamps
    for (name, sx, sy) in spec["stamps"]:
        st = stamps[name]
        for cy in range(st["h"]):
            for cx in range(st["w"]):
                x, y = sx + cx, sy + cy
                if not (0 <= x < W and 0 <= y < H):
                    raise ValueError(f"{spec['title']}: {name} at ({sx},{sy}) runs off the room")
                sub = cut(st["img"], cx, cy)
                top = cut(st["top"], cx, cy) if st["top"] is not None else None
                flat = cut(st["flat"], cx, cy) if st["flat"] is not None else None
                if empty(sub) and empty(top) and empty(flat) and (cx, cy) not in st["behavior"]:
                    continue
                c = cells[y][x]
                if not empty(sub):
                    c.middle = sub.copy() if c.middle is None else A.over(c.middle, sub)
                if not empty(top):
                    c.top = top.copy() if c.top is None else A.over(c.top, top)
                if not empty(flat):
                    c.flat = flat.copy() if c.flat is None else A.over(c.flat, flat)
                c.covered = True
                if (cx, cy) in st["walk"]:
                    c.block = WARP if (cx, cy) in st["behavior"] else WALK
                else:
                    c.block = SOLID
                if (cx, cy) in st["behavior"]:
                    c.behavior = st["behavior"][(cx, cy)]

    # bottom layer
    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            g = ch(x, y)
            if g in walls:
                style = A.WALLS[walls[g]]
                k = 0
                while ch(x, y - 1 - k) == g:
                    k += 1
                n = k + 1
                while ch(x, y + n - k) == g:
                    n += 1
                course = max(0, len(style) - n + k)
                course = min(course, len(style) - 1)
                variants = style[course]
                c.bottom = variants[x % len(variants)].copy()
                c.kind = f"wall:{walls[g]}:{course}"
                if not c.covered:
                    c.block = SOLID
            elif g == "#":
                c.bottom = A.VOID.copy()
                c.kind = "void"
                if not c.covered:
                    c.block = SOLID
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
                elif "alt" in mat and not c.covered and alt_floor(x, y):
                    v = "alt"
                else:
                    v = "plain"
                c.bottom = mat[v].copy()
                c.kind = f"floor:{floors[g]}"
            else:
                raise ValueError(f"{spec['title']}: unknown grid char {g!r} at ({x},{y})")
            if c.flat is not None:
                c.bottom = A.over(c.bottom, c.flat)
            assert (c.bottom[..., 3] == 255).all(), f"{spec['title']}: hole in bottom layer at ({x},{y})"

    for y in range(H):
        for x in range(W):
            c = cells[y][x]
            if c.middle is not None and c.top is not None:
                raise ValueError(f"{spec['title']}: ({x},{y}) would need three layers")
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
                    px = A.over(px, layer)
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
            assert rgb != MAGENTA


PAL_SETS = {n: set(p.values()) for n, p in A.PALETTES.items()}


def subtile_problems(layer):
    """The 8x8 tiles of a layer whose colors fit no one palette."""
    bad = []
    for qy in (0, 8):
        for qx in (0, 8):
            q = layer[qy:qy + 8, qx:qx + 8]
            cols = {tuple(int(v) for v in c) for c in q[q[..., 3] > 0][:, :3]}
            if cols and not any(cols <= s for s in PAL_SETS.values()):
                bad.append(((qx, qy), sorted(cols)))
    return bad


def check_stamps():
    """Every stamp's 8x8 tiles fit one palette each (over any base)."""
    errs = []
    for name, st in A.STAMPS.items():
        for key in ("img", "top", "flat"):
            img = st[key]
            if img is None:
                continue
            for cy in range(st["h"]):
                for cx in range(st["w"]):
                    for (q, cols) in subtile_problems(cut(img, cx, cy)):
                        names = []
                        for c in cols:
                            hit = [f"{p}.{k}" for p, d in A.PALETTES.items() for k, v in d.items() if v == c]
                            names.append(hit[0] if hit else str(c))
                        errs.append(f"{name}.{key} cell ({cx},{cy}) +{q}: {names}")
    if errs:
        raise SystemExit("westrooms: tiles that mix palettes:\n  " + "\n  ".join(errs[:40]))


# --------------------------------------------------------------------------
# Metatiles
# --------------------------------------------------------------------------

def basics(floors=None, walls=None):
    out = []
    for mat, vs in A.FLOORS.items():
        if floors is not None and mat not in floors:
            continue
        for v in ("plain", "alt", "top", "left", "corner"):
            if v in vs:
                c = Cell()
                c.bottom = vs[v].copy()
                out.append(c)
    for name, style in A.WALLS.items():
        if walls is not None and name not in walls:
            continue
        for course in style:
            for img in course:
                c = Cell()
                c.bottom = img.copy()
                c.block = SOLID
                out.append(c)
    c = Cell()
    c.bottom = A.VOID.copy()
    c.block = SOLID
    c.kind = "void"
    out.append(c)
    return out


def collect(layouts, base):
    """base: the bare floor, wall and void cells (basics()), listed first."""
    order, index = [], {}

    def add(c):
        k = c.key()
        if k not in index:
            index[k] = len(order)
            order.append(c)
        return index[k]

    for c in base:
        add(c)
    ids = {}
    for name, cells in layouts.items():
        ids[name] = [[FIRST_METATILE + add(c) for c in row] for row in cells]
    return order, ids


def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def _norm(t):
    t = t.copy()
    t[t[..., 3] == 0] = 0
    return t


NO_MERGE = ("ships", "rubble")


def merge_near_duplicates(layouts, limit=2):
    """Redraw each 8x8 tile within `limit` pixels of another as that other
    tile, flips included (as emporion_build.py does), so it is stored once.
    Works on the composed cells in place; returns how many tiles it merged.
    Never merges across a change in a tile's transparent shape or palette, and
    never touches the walls whose small differences are the point: the ship
    frieze's numbers and the mason's loose stone (NO_MERGE)."""
    occ = {}
    for cells in layouts.values():
        for row in cells:
            for c in row:
                if any(c.kind.startswith(f"wall:{w}:") for w in NO_MERGE):
                    continue
                for ln in ("bottom", "middle", "top"):
                    layer = getattr(c, ln)
                    if layer is None:
                        continue
                    for qy in (0, 8):
                        for qx in (0, 8):
                            t = _norm(layer[qy:qy + 8, qx:qx + 8])
                            if not (t[..., 3] > 0).any():
                                continue
                            k = min(v.tobytes() for v in _flips(t))
                            occ.setdefault(k, []).append((c, ln, qx, qy))
    keys = list(occ)
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    alpha = flat[..., 3] > 0
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in _flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j <= i or not (alpha[i] == alpha[j]).all():
                continue
            cols = {tuple(c) for c in flat[i][alpha[i]][:, :3]} | {tuple(c) for c in flat[j][alpha[j]][:, :3]}
            if any(cols <= ps for ps in PAL_SETS.values()):
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, n = set(), set(), 0
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped:
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (c, ln, qx, qy) in occ[drop]:
            layer = getattr(c, ln).copy()
            cur = layer[qy:qy + 8, qx:qx + 8]
            layer[qy:qy + 8, qx:qx + 8] = min(_flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
            setattr(c, ln, layer)
        dropped.add(drop)
        kept.add(keep)
        n += 1
    return n


def count_tiles(order):
    seen = set()
    for c in order:
        for layer in (c.bottom, c.middle, c.top):
            if layer is None:
                continue
            for qy in (0, 8):
                for qx in (0, 8):
                    t = _norm(layer[qy:qy + 8, qx:qx + 8])
                    if (t[..., 3] > 0).any():
                        seen.add(min(v.tobytes() for v in _flips(t)))
    return len(seen)


def write_sources(order):
    n = len(order)
    if n > MAX_METATILES:
        raise SystemExit(f"westrooms: {n} metatiles is over the {MAX_METATILES} limit")
    rows = (n + 7) // 8
    imgs = {k: np.zeros((rows * 16, 128, 4), np.uint8) for k in ("bottom", "middle", "top")}
    for k in imgs:
        imgs[k][..., :3] = MAGENTA
        imgs[k][..., 3] = 255
    attrs = ["id,behavior"]
    bad = []
    for i, c in enumerate(order):
        y, x = (i // 8) * 16, (i % 8) * 16
        for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
            if layer is None:
                continue
            for (q, cols) in subtile_problems(layer):
                bad.append(f"{FIRST_METATILE + i:#x} {k} +{q}: {cols[:6]}")
            reg = imgs[k][y:y + 16, x:x + 16]
            m = layer[..., 3] > 0
            reg[m, :3] = layer[m, :3]
        if c.behavior != "MB_NORMAL":
            attrs.append(f"{i},{c.behavior}")
    if bad:
        raise SystemExit("westrooms: 8x8 tiles that mix palettes:\n  " + "\n  ".join(bad[:30]))
    SRC.mkdir(parents=True, exist_ok=True)
    for k, img in imgs.items():
        Image.fromarray(img, "RGBA").save(SRC / f"{k}.png")
    (SRC / "attributes.csv").write_text("\n".join(attrs) + "\n")


# --------------------------------------------------------------------------
# Porytiles, in a scratch project against an empty primary
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f"westrooms: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml():
    y = "  palettes:\n    packing:\n      hints_enabled: true\n      hints:\n"
    for g in A.PALETTE_ORDER:
        y += f"        - name: {g}\n          colors:\n"
        for (r, gg, b) in A.PALETTES[g].values():
            y += f"            - [{r}, {gg}, {b}]\n"
    return y


def scratch_project():
    S = SCRATCH
    if S.exists():
        shutil.rmtree(S)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml",
                "data/layouts/layouts.json"):
        dst = S / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (S / "data/tilesets/primary").mkdir(parents=True)
    (S / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    stub_name = f"{SYMBOL}Stub"
    run([pt, "create-tileset", "-C", S, stub_name])
    stubdir = next((S / "data/tilesets/primary").iterdir())
    stub = stubdir / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", S, stub_name])
    cfg = S / f"porytiles/tilesets/{SYMBOL}"
    sec = S / f"data/tilesets/secondary/{DIR}"
    if (CFG / "tileset-manifest.json").exists():
        cfg.mkdir(parents=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            if (CFG / f).exists():
                shutil.copy2(CFG / f, cfg / f)
        sec.mkdir(parents=True)
        if BIN.exists():
            shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        short = SYMBOL.replace("gTileset_", "")
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = S / rel
            t = p.read_text()
            t = re.sub(rf"const struct Tileset {SYMBOL} =\s*\{{.*?\}};", "", t, flags=re.S)
            t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\] =\s*\{{.*?\}};",
                       "", t, flags=re.S)
            t = re.sub(rf"const u\d+ g\w+_PorytilesManaged_{short}\[\] = [^\n]*\n", "", t)
            p.write_text(t)
        run([pt, "create-tileset", SYMBOL, "-C", S, "--secondary",
             "--primary-pairing-mode", "manual", "--primary-pairing-partners", stub_name])
        assert sec.exists(), f"porytiles made no {sec}"
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [" + stub_name + "]\n" + hints_yaml())
    if (sec / "porytiles_src").exists():
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    return sec


def compile():
    sec = scratch_project()
    r = run([porytiles(), "compile-tileset", "-C", SCRATCH, "--no-verify-checksums", SYMBOL])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        p = SCRATCH / f"porytiles/tilesets/{SYMBOL}/{f}"
        if p.exists():
            shutil.copy2(p, CFG / f)
    (CFG / "config.yaml").write_text(
        "# Written by tools/ichor/art/westrooms_build.py; edit PALETTES in westrooms_art.py.\n"
        "# The build compiles in a scratch project against an empty primary; this config pairs\n"
        "# with aethos so a direct Porytiles compile also works.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n" + hints_yaml())


def verify():
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    bad, pals = [], set()
    for i, entries in enumerate(raw):
        for e in entries:
            e = int(e)
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0:
                continue
            pals.add(pal)
            if tile < FIRST_TILE or not (6 <= pal <= 12):
                bad.append((hex(FIRST_METATILE + i), hex(e)))
    if bad:
        raise SystemExit(f"westrooms: entries outside its own tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    if used > TILE_LIMIT:
        raise SystemExit(f"westrooms: {used} tiles; the set may use at most {TILE_LIMIT}")
    return len(raw), used, sorted(pals)


# --------------------------------------------------------------------------
# Rendering and blockdata
# --------------------------------------------------------------------------

def blockdata(cells, ids):
    H, W = len(cells), len(cells[0])
    out = np.zeros(H * W, "<u2")
    for y in range(H):
        for x in range(W):
            out[y * W + x] = ids[y][x] | cells[y][x].block
    return out


def render_compiled(blocks, width, primary="gTileset_Oikos"):
    import render_map as RM
    RM.read_fieldmap_constants()
    syms = RM.scan_tileset_symbols()
    r = RM.Renderer(RM.Tileset(RM.resolve_tileset(primary, syms)),
                    RM.Tileset(RM.tileset_from_dir(TS)))
    return np.array(RM.render_blocks(r, blocks, width))


def save_scaled(arr, path, scale):
    im = Image.fromarray(arr)
    if scale > 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
