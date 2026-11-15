#!/usr/bin/env python3
"""Region interior secondaries: the furnishings a region's rooms need, and no more.

gTileset_Oikia and gTileset_Civic are the slice's interiors. Their metatile ids
are fixed by the slice's rooms, and they are nearly full, so later regions don't
add to them. Each region instead gets a pair of its own secondaries, built from
the rooms that use them:

  an oikia kind, for homes and workshops: oikia's floors, walls and rugs, every
    oikia stamp its rooms use, and the region's own stamps (drawn in oikia's
    palettes, with a few colors added where the free slots allow);
  a civic kind, for the Asclepeions and Agoras: every gTileset_Civic metatile
    its halls use, and the region's own halls pieces (drawn in civic's palettes).

A region's tilesets carry exactly the cells its rooms compose, so they stay well
inside the limits however many pieces the region draws, and a later region
(Lakonia, Delphoi) repeats the recipe: a <region>_art.py with its pieces, a
rooms script that composes with OikiaKit and CivicKit, and two tilesets
registered in src/data/tilesets (see design/phase4/ROOMS_aegean.md).

Both kinds are compiled in a scratch project against an empty stand-in primary,
as temple_demeter_build.py does, so they use only their own tiles and palettes
6-12 and work on any interior primary (they are meant for oikos). The builder
then checks every metatile entry and the 504-tile door limit.
"""
from __future__ import annotations

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

import oikia_art as A  # noqa: E402
import oikia_build as B  # noqa: E402

MAGENTA = (255, 0, 255)
FIRST_METATILE = 0x200
MAX_METATILES = 512
# Door animations copy their frames over the last 8 secondary tiles
# (DOOR_TILE_START_SIZE1 in src/field_door.c), so a secondary keeps to 504.
MAX_TILES = 504
COLS = 8


def porytiles_exe():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def tileset_dir(symbol):
    """gTileset_OikiaAegean -> oikia_aegean, as Porytiles names it."""
    name = symbol.removeprefix("gTileset_")
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def _run(cmd, what):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f"{what}: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml(groups):
    """Porytiles palette-packing hints: groups is {name: [(r, g, b), ...]}."""
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for name, cols in groups.items():
        lines.append(f"        - name: {name}")
        lines.append("          colors:")
        for r, g, b in cols:
            lines.append(f"            - [{r}, {g}, {b}]")
    return "\n".join(lines) + "\n"


def compile_secondary(symbol, hints, what):
    """Compile data/tilesets/secondary/<dir>/porytiles_src into porytiles_bin.

    Runs Porytiles in build/<dir>_porytiles, a scratch copy of the project's
    fieldmap headers with an empty stand-in primary, so nothing can be borrowed
    from a real primary. The committed manifest and cache are carried over
    between builds."""
    d = tileset_dir(symbol)
    sec_dir = ROOT / "data/tilesets/secondary" / d
    src, binp = sec_dir / "porytiles_src", sec_dir / "porytiles_bin"
    cfg = ROOT / "porytiles/tilesets" / symbol
    scratch = ROOT / f"build/{d}_porytiles"
    stub = f"{symbol}Stub"
    pt = porytiles_exe()
    if scratch.exists():
        shutil.rmtree(scratch)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (scratch / "data/tilesets/primary").mkdir(parents=True)
    (scratch / "data/tilesets/secondary").mkdir(parents=True)
    _run([pt, "create-tileset", "-C", scratch, stub], what)
    stub_src = scratch / "data/tilesets/primary" / tileset_dir(stub) / "porytiles_src"
    shutil.rmtree(stub_src / "anim", ignore_errors=True)
    (stub_src / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (*MAGENTA, 255)).save(stub_src / f"{n}.png")
    _run([pt, "compile-tileset", "-C", scratch, stub], what)
    scfg = scratch / "porytiles/tilesets" / symbol
    scfg.mkdir(parents=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stub}]\n"
    (scfg / "config.yaml").write_text(pairing)
    ssec = scratch / "data/tilesets/secondary" / d
    if (cfg / "tileset-manifest.json").exists() and binp.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(cfg / f, scfg / f)
        shutil.copytree(binp, ssec / "porytiles_bin")
    else:
        # first build: the scratch C tables must not already declare the tileset
        tail = symbol.removeprefix("gTileset_")
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = scratch / rel
            t = p.read_text()
            t = re.sub(rf"(//[^\n]*\n)*const struct Tileset {symbol}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
            t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{tail}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                       "", t, flags=re.S)
            t = "\n".join(line for line in t.split("\n")
                          if not re.search(rf"PorytilesManaged_{tail}\b", line))
            p.write_text(t)
        _run([pt, "create-tileset", "-C", scratch, "--secondary", symbol], what)
        shutil.rmtree(ssec / "porytiles_src")
    shutil.copytree(src, ssec / "porytiles_src")
    (scfg / "config.yaml").write_text(pairing + hints)
    r = _run([pt, "compile-tileset", "-C", scratch, "--no-verify-checksums", symbol], what)
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if binp.exists():
        shutil.rmtree(binp)
    shutil.copytree(ssec / "porytiles_bin", binp)
    cfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(scfg / f, cfg / f)
    (cfg / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {symbol}. Written by\n"
        f"# tools/ichor/art/interiors_lib.py, which compiles it against an empty stand-in\n"
        f"# primary: it uses only its own tiles and palettes 6-12, so it works on any\n"
        f"# interior primary. Rebuild it with the rooms script that uses it.\n"
        f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n" + hints)


def verify(symbol, n_metatiles, what):
    """Every entry is tile 0 or the secondary's own tile in palettes 6-12; the
    tiles fit under the door limit. Returns (metatiles, tiles used)."""
    binp = ROOT / "data/tilesets/secondary" / tileset_dir(symbol) / "porytiles_bin"
    raw = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    if len(raw) < n_metatiles:
        raise SystemExit(f"{what}: compiled {len(raw)} metatiles, expected {n_metatiles}")
    bad = []
    for i, entries in enumerate(raw):
        for e in entries:
            idx, pal = int(e) & 0x3FF, int(e) >> 12
            if idx == 0:
                continue
            if idx < 512 or not 6 <= pal <= 12:
                bad.append((FIRST_METATILE + i, idx, pal))
    if bad:
        raise SystemExit(f"{what}: metatiles reach outside {symbol}: {bad[:8]}")
    used = max((int(e) & 0x3FF) - 511 for e in raw.ravel() if int(e) & 0x3FF >= 512)
    if used > MAX_TILES:
        raise SystemExit(f"{what}: {used} tiles is over the {MAX_TILES}-tile limit")
    return len(raw), used


# --------------------------------------------------------------------------
# The oikia kind: composed from stamps, deduplicated into metatiles
# --------------------------------------------------------------------------

class OikiaKit:
    """Homes and workshops in oikia's style. stamps and floors extend oikia's
    STAMPS and FLOORS (oikia's own tables are left alone)."""

    def __init__(self, symbol, palettes, stamps, floors=None):
        self.symbol = symbol
        self.palettes = palettes
        self.pal_sets = {n: set(p.values()) for n, p in palettes.items()}
        self.stamps = dict(A.STAMPS)
        clash = set(stamps) & set(A.STAMPS)
        assert not clash, f"region stamps shadow oikia's: {clash}"
        self.stamps.update(stamps)
        self.floors = dict(A.FLOORS)
        clash = set(floors or {}) & set(A.FLOORS)
        assert not clash, f"region floors shadow oikia's: {clash}"
        self.floors.update(floors or {})
        self.order = None
        self.index = None

    def compose(self, spec):
        """oikia_build.compose, with a second floor: grid cells marked ','
        take spec['floor2'] (a yard's grass beside the house's paving). Both
        floors count as floor for the wall shadows."""
        grid = spec["grid"]
        H, W = len(grid), len(grid[0])
        assert all(len(r) == W for r in grid), "ragged grid"
        flat = dict(spec, grid=[r.replace(",", ".") for r in grid])
        saved = dict(A.FLOORS)
        A.FLOORS.update(self.floors)
        try:
            cells = B.compose(flat, self.stamps)
        finally:
            A.FLOORS.clear()
            A.FLOORS.update(saved)
        if "floor2" in spec:
            rugs = {(rx + i, ry + j) for (_, rx, ry, rw, rh) in spec.get("rugs", [])
                    for j in range(rh) for i in range(rw)}

            def ch(x, y):
                return grid[y][x] if 0 <= x < W and 0 <= y < H else "#"
            for y in range(H):
                for x in range(W):
                    if ch(x, y) != "," or (x, y) in rugs:
                        continue
                    mat = self.floors[spec["floor2"]]
                    c = cells[y][x]
                    top_sh = ch(x, y - 1) not in ".,"
                    left_sh = ch(x - 1, y) not in ".,"
                    if top_sh and left_sh:
                        v = "corner"
                    elif top_sh:
                        v = "top"
                    elif left_sh:
                        v = "left"
                    elif "alt" in mat and not c.covered and B.alt_floor(x, y):
                        v = "alt"
                    else:
                        v = "plain"
                    c.bottom = mat[v].copy()
                    if hasattr(c, "flat"):
                        c.bottom = B.over(c.bottom, c.flat)
        return cells

    def basics(self):
        """oikia's bare floors, walls, void and rugs, then the region's floors."""
        out = B.basics()
        for mat, vs in self.floors.items():
            if mat in A.FLOORS:
                continue
            for v in ("plain", "alt", "top", "left", "corner"):
                if v in vs:
                    c = B.Cell()
                    c.bottom = vs[v]
                    out.append(c)
        return out

    def collect(self, layouts):
        """layouts: {name: cells}. Basics first (oikia's have the same ids in
        every region), then each layout's new cells in order. Returns {name: ids}."""
        order, index = [], {}

        def add(c):
            k = c.key()
            if k not in index:
                index[k] = len(order)
                order.append(c)
            return index[k]
        for c in self.basics():
            add(c)
        ids = {name: [[FIRST_METATILE + add(c) for c in row] for row in cells]
               for name, cells in layouts.items()}
        if len(order) > MAX_METATILES:
            raise SystemExit(f"{self.symbol}: {len(order)} metatiles is over {MAX_METATILES}")
        self.order = order
        self.index = {c.key(): FIRST_METATILE + i for i, c in enumerate(order)}
        return ids

    def void_id(self):
        c = B.Cell()
        c.bottom = A.VOID
        c.block = B.SOLID
        return self.index[c.key()]

    def check_subtiles(self, layer, where):
        for qy in (0, 8):
            for qx in (0, 8):
                q = layer[qy:qy + 8, qx:qx + 8]
                cols = {tuple(int(v) for v in c) for c in q[q[..., 3] > 0][:, :3]}
                if cols and not any(cols <= s for s in self.pal_sets.values()):
                    raise ValueError(f"{self.symbol}: 8x8 tile at {where} +({qx},{qy}) "
                                     f"mixes palettes: {sorted(cols)}")

    def write_sources(self):
        src = ROOT / "data/tilesets/secondary" / tileset_dir(self.symbol) / "porytiles_src"
        n = len(self.order)
        rows = (n + COLS - 1) // COLS
        imgs = {k: np.zeros((rows * 16, 128, 4), np.uint8) for k in ("bottom", "middle", "top")}
        for img in imgs.values():
            img[..., :3] = MAGENTA
            img[..., 3] = 255
        attrs = ["id,behavior"]
        for i, c in enumerate(self.order):
            y, x = (i // COLS) * 16, (i % COLS) * 16
            for k, layer in (("bottom", c.bottom), ("middle", c.middle), ("top", c.top)):
                if layer is None:
                    continue
                self.check_subtiles(layer, f"metatile {FIRST_METATILE + i:#x} {k}")
                reg = imgs[k][y:y + 16, x:x + 16]
                m = layer[..., 3] > 0
                reg[m, :3] = layer[m, :3]
            if c.behavior != "MB_NORMAL":
                attrs.append(f"{i},{c.behavior}")
        src.mkdir(parents=True, exist_ok=True)
        for k, img in imgs.items():
            Image.fromarray(img, "RGBA").save(src / f"{k}.png")
        (src / "attributes.csv").write_text("\n".join(attrs) + "\n")

    def hints(self):
        return hints_yaml({n: list(dict.fromkeys(p.values())) for n, p in self.palettes.items()})

    def blocks(self, cells, ids):
        return B.blockdata(cells, ids)

    def build(self, compile_=True):
        self.write_sources()
        if not compile_:
            return len(self.order), None
        compile_secondary(self.symbol, self.hints(), self.symbol)
        return verify(self.symbol, len(self.order), self.symbol)


# --------------------------------------------------------------------------
# The civic kind: named metatiles (civic_tiles.py's and the region's own)
# --------------------------------------------------------------------------

class CivicKit:
    """Halls in civic's style. define() registers every metatile (civic's and
    the region's) into civic_tiles' METATILES; palettes is the plan each 8x8
    tile must fit (civic's own, unless the region needs more)."""

    def __init__(self, symbol, define, palettes):
        import civic_tiles as ct
        self.ct = ct
        self.symbol = symbol
        if not ct.METATILES:
            define()
        self.palettes = palettes
        self.names = None
        self.ids = None

    def collect(self, grids, extra=()):
        """grids: {room: [[name, ...], ...]}. The void comes first, then every
        name used (and every name in extra) in the order the metatiles were
        defined, so ids only move when a piece is added or dropped."""
        ct = self.ct
        used = {"void"}
        for g in grids.values():
            for row in g:
                used.update(row)
        used.update(extra)
        names = sorted(used, key=lambda n: ct.BY_NAME[n])
        assert names[0] == "void"
        if len(names) > MAX_METATILES:
            raise SystemExit(f"{self.symbol}: {len(names)} metatiles is over {MAX_METATILES}")
        self.names = names
        self.ids = {n: FIRST_METATILE + i for i, n in enumerate(names)}
        return self.ids

    def precheck(self):
        ct = self.ct
        misfits = {}
        for n in self.names:
            m = ct.METATILES[ct.BY_NAME[n]]
            for k in ("bottom", "middle", "top"):
                if m[k] is None:
                    continue
                for t in ct.tiles_of(m[k]):
                    cs = {ch for r in t for ch in r if ch != "."}
                    if cs and not any(cs <= set(p) for p in self.palettes.values()):
                        misfits.setdefault("".join(sorted(cs)), n)
        if misfits:
            for cs, n in misfits.items():
                print(f"  {n}: tile colors {cs} fit no palette")
            raise SystemExit(f"{self.symbol}: every 8x8 tile must draw from one palette")

    def write_sources(self):
        ct = self.ct
        self.precheck()
        src = ROOT / "data/tilesets/secondary" / tileset_dir(self.symbol) / "porytiles_src"
        n = len(self.names)
        rows = (n + COLS - 1) // COLS
        layers = {k: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for k in ("bottom", "middle", "top")}
        for img in layers.values():
            img[...] = (*MAGENTA, 255)
        attrs = ["id,behavior"]
        for i, name in enumerate(self.names):
            m = ct.METATILES[ct.BY_NAME[name]]
            y, x = divmod(i, COLS)
            for k in layers:
                if m[k] is not None:
                    layers[k][y * 16:y * 16 + 16, x * 16:x * 16 + 16] = ct.to_rgba(m[k])
            if m["behavior"] != "MB_NORMAL":
                attrs.append(f"{i},{m['behavior']}")
        src.mkdir(parents=True, exist_ok=True)
        for k, img in layers.items():
            Image.fromarray(img, "RGBA").save(src / f"{k}.png")
        (src / "attributes.csv").write_text("\n".join(attrs) + "\n")

    def hints(self):
        from civic_art import LEGEND
        return hints_yaml({n: [LEGEND[ch] for ch in cols] for n, cols in self.palettes.items()})

    def build(self, compile_=True):
        self.write_sources()
        if not compile_:
            return len(self.names), None
        compile_secondary(self.symbol, self.hints(), self.symbol)
        return verify(self.symbol, len(self.names), self.symbol)


# --------------------------------------------------------------------------
# Reference sheets
# --------------------------------------------------------------------------

def pieces_sheet(items, path, cols=10, scale=2):
    """A labelled sheet of pieces: items is [(label, rgb image (h, w, 3))]."""
    from PIL import ImageDraw, ImageFont
    font = ImageFont.load_default()
    pad, label_h = 6, 12
    cw = max(16 * 6, max(img.shape[1] for _, img in items)) + pad
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    heights = [max(img.shape[0] for _, img in r) + label_h + pad for r in rows]
    sheet = Image.new("RGB", (cols * cw + pad, sum(heights) + pad), (40, 40, 48))
    draw = ImageDraw.Draw(sheet)
    y = pad
    for r, h in zip(rows, heights):
        for i, (label, img) in enumerate(r):
            x = pad + i * cw
            draw.text((x, y), label[:cw // 6], fill=(230, 230, 200), font=font)
            sheet.paste(Image.fromarray(img), (x, y + label_h))
        y += h
    sheet = sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def stamp_preview(st, floor, wall=None, on_wall=False):
    """A stamp drawn over its backdrop: for a piece that hangs on the back
    wall, the wall (a 16x32 strip) behind its first two rows; floor elsewhere."""
    h, w = st["h"], st["w"]
    out = np.zeros((h * 16, w * 16, 4), np.uint8)
    for cy in range(h):
        for cx in range(w):
            base = floor
            if on_wall and wall is not None and cy < 2:
                base = wall[cy * 16:(cy + 1) * 16]
            out[cy * 16:(cy + 1) * 16, cx * 16:(cx + 1) * 16] = base
    for layer in (st["img"], st["top"]):
        if layer is not None:
            m = layer[..., 3] > 0
            out[m] = layer[m]
    return out[..., :3]
