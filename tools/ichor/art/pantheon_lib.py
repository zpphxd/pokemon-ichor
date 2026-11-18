"""Shared toolkit for the four Pantheon seats' secondaries (design/maps/Olympus_Pantheon.md).

Each seat of the Elite Four has its own tileset, so each hall has its own
palette and its own set pieces:

  gTileset_SeatAres      the war hall: bloodred floor, trophy armor, spear racks, braziers, bronze Ares
  gTileset_SeatPoseidon  the sea hall: the basin, coral columns, the trireme, the trident
  gTileset_SeatAthena    the hall of lamps: owls, scroll walls, lampstands, the sacred olive
  gTileset_SeatHera      the peacock hall: feather columns, torches up the aisle, the throne

The drawing layer is chion_lib's (Layer, Struct, validate, pack, write_sources),
switched onto each seat's palette with use(); the compile is chion_build's,
generalized: every seat is compiled against an empty stand-in primary, so its
metatiles use only its own tiles and palettes 6-12 and it works on any primary.

Palette rule (STYLE.md §4.3): every 8x8 tile of every layer draws from ONE
group of at most 15 colors; validate() enforces it.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chion_lib as base  # noqa: E402
from chion_lib import Layer, Struct, composite, pack, preview, validate, write_sources  # noqa: E402,F401

ROOT = base.ROOT
TILE_LIMIT = 504          # tiles 504-511 of a secondary belong to the door animations


def use(C, GROUPS):
    """Point chion_lib's drawing and validation at one seat's palette."""
    for g, names in GROUPS.items():
        assert len(names) <= 15, (g, len(names))
        assert len(set(names)) == len(names), g
        for n in names:
            assert n in C, n
    for n, c in C.items():
        assert all(v % 8 == 0 and 0 <= v <= 248 for v in c), (n, c)
    assert len(set(C.values())) == len(C), "two names share a color"
    assert len(GROUPS) <= 7, "a secondary has seven palettes"
    base.C.clear()
    base.C.update(C)
    base.GROUPS.clear()
    base.GROUPS.update(GROUPS)
    base.GROUP_RGB.clear()
    base.GROUP_RGB.update({g: {C[n] for n in names} for g, names in GROUPS.items()})
    base.RGB2NAME.clear()
    base.RGB2NAME.update({c: n for n, c in C.items()})


def h(*args):
    return base.h(*args)


# --------------------------------------------------------------------------
# Drawing helpers shared by the four halls
# --------------------------------------------------------------------------

def cyl(L, x0, y0, w, hgt, ramp, light=0.32):
    """A vertical cylinder lit from the left: ramp is dark..light names; the
    highlight band sits a third of the way across, the shadow on the right."""
    n = len(ramp)
    for i in range(w):
        t = (i + 0.5) / w
        d = abs(t - light)
        if t < light:
            v = 1 - d / light * 0.55
        else:
            v = 1 - (t - light) / (1 - light)
        idx = max(0, min(n - 1, int(round(v * (n - 1)))))
        L.vline(x0 + i, y0, y0 + hgt - 1, ramp[idx])


def outline(L, ink, inside=None):
    """A 1 px ink outline round every opaque pixel's silhouette (in place)."""
    a = L.a[..., 3] > 0
    edge = np.zeros_like(a)
    edge[1:, :] |= a[:-1, :]
    edge[:-1, :] |= a[1:, :]
    edge[:, 1:] |= a[:, :-1]
    edge[:, :-1] |= a[:, 1:]
    edge &= ~a
    ys, xs = np.nonzero(edge)
    for y, x in zip(ys, xs):
        L.px(int(x), int(y), ink)


def sel_outline(L, ink, lit=None):
    """Selective outline: ink round the silhouette, except the top-left edge which
    takes `lit` (a dark of the material) when given."""
    a = L.a[..., 3] > 0
    ys, xs = np.nonzero(a)
    out = []
    H, W = a.shape
    for y, x in zip(ys, xs):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            X, Y = x + dx, y + dy
            if 0 <= X < W and 0 <= Y < H and not a[Y, X]:
                out.append((X, Y, dx, dy))
    for X, Y, dx, dy in out:
        L.px(int(X), int(Y), lit if (lit and (dx < 0 or dy < 0)) else ink)


def layer_from(arr):
    L = Layer(arr.shape[1], arr.shape[0])
    L.a[:] = arr
    return L


def art(rows, legend):
    return base.grid_art(rows, legend)


def struct(key, title, section, w, h, walk=None, notes="", names=None, floor=None, floor_layer="bottom"):
    """A Struct with its floor painted under every cell (floor: a 16x16 RGBA or a
    function (cx, cy) -> 16x16 RGBA)."""
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    if floor is not None:
        for cy in range(h):
            for cx in range(w):
                f = floor(cx, cy) if callable(floor) else floor
                s.layers[floor_layer].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = f
    return s


def paint(s, arr, x, y, layer="middle"):
    """Paste an RGBA art array onto a struct layer at pixel (x, y)."""
    s.layers[layer].paste(arr, x, y)


def split_top(s, rows_top):
    """Move the struct's middle-layer pixels in its top `rows_top` metatile rows
    to the top layer (drawn over the player), for walk-behind tops."""
    M, T = s.layers["middle"], s.layers["top"]
    hpx = rows_top * 16
    T.a[:hpx] = M.a[:hpx]
    M.a[:hpx] = 0


# --------------------------------------------------------------------------
# The compile: chion_build's, for any seat
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"pantheon: failed: {' '.join(map(str, cmd))}")
    return r


class Seat:
    """One seat's tileset: its name, folder, palette and sections."""

    def __init__(self, name, folder, C, GROUPS, sections, section_rows, swaps=()):
        self.name, self.folder = name, folder
        self.C, self.GROUPS = C, GROUPS
        self.sections_fn, self.section_rows = sections, section_rows
        self.swaps = swaps
        self.ts = ROOT / "data/tilesets/secondary" / folder
        self.src, self.bin = self.ts / "porytiles_src", self.ts / "porytiles_bin"
        self.cfg = ROOT / "porytiles/tilesets" / name
        self.scratch = ROOT / f"build/{folder}_porytiles"
        self.catalog_path = self.ts / "catalog.json"

    def hints_yaml(self):
        lines = ["  tiles:", "    sharing:", "      packing: biased", "      alignment: greedy",
                 "  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
        for g, names in self.GROUPS.items():
            lines.append(f"        - name: {g}")
            lines.append("          colors:")
            for n in names:
                r, gg, b = self.C[n]
                lines.append(f"            - [{r}, {gg}, {b}]")
        return "\n".join(lines) + "\n"

    def scratch_project(self):
        S = self.scratch
        if S.exists():
            shutil.rmtree(S)
        for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                    "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                    "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
            dst = S / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        fresh = not (self.cfg / "tileset-manifest.json").exists()
        if fresh:
            # porytiles create-tileset declares the tileset itself: hide ours
            short = self.name[len("gTileset_"):]
            for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                        "src/data/tilesets/metatiles.h"):
                f = S / rel
                text = f.read_text()
                tag = f"// Ichor: {self.folder}"
                if tag in text:
                    a = text.index(tag)
                    if rel.endswith("headers.h"):
                        b = text.index("};", text.index(f"const struct Tileset {self.name} =", a)) + 2
                    else:
                        b = text.find("\n// Ichor:", a + 5)
                        b = len(text) if b < 0 else b
                    text = text[:a] + text[b:]
                assert f"PorytilesManaged_{short}" not in text or not rel.endswith("headers.h"), rel
                f.write_text(text)
        (S / "data/tilesets/primary").mkdir(parents=True)
        (S / "data/tilesets/secondary").mkdir(parents=True)
        pt = porytiles()
        stub_name = self.name + "Stub"
        run([pt, "create-tileset", "-C", S, stub_name])
        stub_dir = next((S / "data/tilesets/primary").iterdir())
        stub = stub_dir / "porytiles_src"
        shutil.rmtree(stub / "anim", ignore_errors=True)
        (stub / "attributes.csv").write_text("id,behavior\n")
        for n in ("bottom", "middle", "top"):
            Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
        run([pt, "compile-tileset", "-C", S, stub_name])
        cfg = S / "porytiles/tilesets" / self.name
        cfg.mkdir(parents=True)
        pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stub_name}]\n"
        (cfg / "config.yaml").write_text(pairing)
        sec = S / "data/tilesets/secondary" / self.folder
        if not fresh and self.bin.exists():
            for f in ("tileset-manifest.json", "tileset.cache.json"):
                shutil.copy2(self.cfg / f, cfg / f)
            sec.mkdir(parents=True, exist_ok=True)
            shutil.copytree(self.bin, sec / "porytiles_bin")
        else:
            run([pt, "create-tileset", "-C", S, "--secondary", self.name])
            made = [d for d in (S / "data/tilesets/secondary").iterdir()]
            assert len(made) == 1, made
            if made[0] != sec:
                made[0].rename(sec)
            shutil.rmtree(sec / "porytiles_src")
        shutil.copytree(self.src, sec / "porytiles_src")
        (cfg / "config.yaml").write_text(pairing + self.hints_yaml())
        return sec

    def compile(self):
        sec = self.scratch_project()
        r = run([porytiles(), "compile-tileset", "-C", self.scratch, "--no-verify-checksums", self.name])
        if r.stdout.strip() or r.stderr.strip():
            print((r.stdout + r.stderr)[-2000:])
        if self.bin.exists():
            shutil.rmtree(self.bin)
        shutil.copytree(sec / "porytiles_bin", self.bin)
        self.cfg.mkdir(parents=True, exist_ok=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(self.scratch / "porytiles/tilesets" / self.name / f, self.cfg / f)
        (self.cfg / "config.yaml").write_text(
            f"# Per-tileset Porytiles config for {self.name}, a seat of the Pantheon.\n"
            "# Written by tools/ichor/art/pantheon_build.py, which compiles it against an\n"
            "# empty stand-in primary and checks its metatiles use only its own tiles and\n"
            "# palettes 6-12. Pair it with oikos when compiling it directly.\n"
            "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n"
            + self.hints_yaml())

    def verify(self, rows):
        raw = np.fromfile(self.bin / "metatiles.bin", "<u2").reshape(-1, 8)
        assert len(raw) >= rows * 8, (len(raw), rows)
        bad = [(0x200 + i, hex(int(e))) for i, entries in enumerate(raw) for e in entries
               if not (int(e) & 0x3FF == 0 and int(e) >> 12 == 0)
               and (int(e) & 0x3FF < 512 or not (6 <= int(e) >> 12 <= 12))]
        if bad:
            sys.exit(f"pantheon: {self.name} entries outside its tiles/palettes 6-12: {bad[:10]}")
        a = np.array(Image.open(self.bin / "tiles.png"))
        tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
        used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
        late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                       if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
        if used > TILE_LIMIT or late:
            sys.exit(f"pantheon: {self.name}: {used} tiles used and tiles {late[:8]} referenced; "
                     f"a secondary may use at most {TILE_LIMIT}")
        print(f"{self.name}: verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
        return used

    def write_catalog(self, secs, used):
        data = {"tileset": self.name, "primary": "gTileset_Oikos", "tiles_used": used, "pieces": []}
        for name, structs in secs:
            for s in structs:
                data["pieces"].append({
                    "key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                    "ids": s.ids, "walk": s.walk, "notes": s.notes,
                    "names": {k: list(v) for k, v in s.names.items()},
                    "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                })
        self.catalog_path.write_text(json.dumps(data, indent=1) + "\n")

    def sheet(self, out, scale=2):
        sys.path.insert(0, str(ROOT / "tools/ichor"))
        import render_map as rm
        rm.read_fieldmap_constants()
        syms = rm.scan_tileset_symbols()
        r = rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Oikos", syms)),
                        rm.Tileset(rm.tileset_from_dir(self.ts)))
        img = rm.render_sheet(r, 0x200, len(r.s.metatiles), scale)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        img.save(out)

    def build(self, compile_=True, preview_out=None, sheet_out=None):
        use(self.C, self.GROUPS)
        secs = self.sections_fn()
        allst = [s for _, ss in secs for s in ss]
        probs = validate(allst)
        for p in probs[:40]:
            print("PROBLEM:", p)
        if preview_out:
            preview(allst).save(preview_out)
            print(preview_out)
        if probs:
            sys.exit(1)
        rows = pack([(self.section_rows[n], ss) for n, ss in secs])
        write_sources(allst, rows, self.src)
        if compile_:
            self.compile()
            used = self.verify(rows)
            self.write_catalog(secs, used)
            if sheet_out:
                self.sheet(sheet_out)
        return secs


def catalog(folder):
    """{key: piece} from a seat's compiled catalog."""
    data = json.loads((ROOT / "data/tilesets/secondary" / folder / "catalog.json").read_text())
    return {p["key"]: p for p in data["pieces"]}


# --------------------------------------------------------------------------
# Shapes: masks filled with a ramp, lit from the top left, then outlined
# --------------------------------------------------------------------------

def mask(w, h):
    return np.zeros((h, w), bool)


def m_rect(m, x, y, w, h):
    m[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = True
    return m


def m_poly(m, pts):
    from PIL import ImageDraw
    img = Image.new("1", (m.shape[1], m.shape[0]), 0)
    ImageDraw.Draw(img).polygon(pts, fill=1)
    m |= np.array(img, bool)
    return m


def m_ellipse(m, x0, y0, x1, y1):
    from PIL import ImageDraw
    img = Image.new("1", (m.shape[1], m.shape[0]), 0)
    ImageDraw.Draw(img).ellipse([x0, y0, x1, y1], fill=1)
    m |= np.array(img, bool)
    return m


def shade(L, m, ramp, light=0.3, ox=0, oy=0, vert=0.0):
    """Fill mask m with ramp (dark..light), lit from the left: each row's span is
    shaded like a cylinder; `vert` > 0 also darkens toward the mask's bottom."""
    n = len(ramp)
    H, W = m.shape
    ys = np.nonzero(m.any(axis=1))[0]
    if not len(ys):
        return
    y0, y1 = ys[0], ys[-1]
    for y in range(H):
        xs = np.nonzero(m[y])[0]
        if not len(xs):
            continue
        a, b = xs[0], xs[-1]
        span = max(1, b - a + 1)
        for x in xs:
            t = (x - a + 0.5) / span
            v = 1 - abs(t - light) / light if t < light else 1 - (t - light) / (1 - light)
            v = 0.2 + 0.8 * v
            if vert:
                v -= vert * (y - y0) / max(1, y1 - y0)
            idx = max(0, min(n - 1, int(v * n)))
            L.px(ox + int(x), oy + y, ramp[idx])


def flat(L, m, c, ox=0, oy=0):
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        L.px(ox + int(x), oy + int(y), c)


def ink_edge(L, m, ink, lit=None, ox=0, oy=0):
    """Outline mask m's silhouette into L: ink below and right, `lit` above and left."""
    H, W = m.shape
    for y in range(H):
        for x in range(W):
            if m[y, x]:
                continue
            nb = [(x + 1, y, "l"), (x - 1, y, "r"), (x, y + 1, "t"), (x, y - 1, "b")]
            hit = [d for X, Y, d in nb if 0 <= X < W and 0 <= Y < H and m[Y, X]]
            if hit:
                c = lit if (lit and all(d in "lt" for d in hit)) else ink
                L.px(ox + x, oy + y, c)


def tiled(fn, w=16, h=16, ox=0, oy=0):
    """A w x h RGBA from a pixel function fn(X, Y) -> color name or None, at world
    offset (ox, oy) so neighbouring cells line up seamlessly."""
    L = Layer(w, h)
    for y in range(h):
        for x in range(w):
            c = fn(ox + x, oy + y)
            if c:
                L.px(x, y, c)
    return L.a.copy()


def flagstones(X, Y, ramp, grout, seed, slab_w=16, slab_h=8, period=32, marks=(), period_y=None, bond=True):
    """A seamless flagstone floor: running-bond slabs with a bevel (light top-left,
    dark bottom-right), each slab a shade picked by its position. ramp: (shadow,
    base, alt, light). marks: extra (fn(X, Y) -> color or None) layered on.
    The pattern repeats every `period` px across and `period_y` (default
    `period`) down; lay its cells by map position so the bond lines up."""
    py = period_y or period
    x, y = X % period, Y % py
    row = y // slab_h
    off = (slab_w // 2) * (row % 2) if bond else 0
    sx = (x + off) % period
    col = sx // slab_w
    ix, iy = sx % slab_w, y % slab_h
    if iy == 0 or ix == 0:
        return grout
    pick = (base.h(seed, row, col) % 5)
    face = ramp[2] if pick == 0 else ramp[1]
    if iy == 1 or ix == 1:
        return ramp[3]
    if iy == slab_h - 1 or ix == slab_w - 1:
        return ramp[0]
    for f in marks:
        c = f(X, Y)
        if c:
            return c
    return face
