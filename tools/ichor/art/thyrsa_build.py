#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Thyrsa, Thyrsa City's secondary tileset.

The pipeline is emporion_build.py's, reused function for function:
1. thyrsa_art.build() draws every structure; each 8x8 tile must draw from one of
   thyrsa_lib.GROUPS. Tiles within 2 px of another are redrawn as that one.
2. Packs them into the 8-wide sheet from 0x200, section by section.
3. Writes data/tilesets/secondary/thyrsa/porytiles_src.
4. Compiles with Porytiles in a scratch project against an empty stand-in primary,
   so the art uses only its own tiles and palettes 6-12.
5. Borrows aethos's ground: every cell drawn on grass or path gets its bottom
   layer pointed at aethos's metatile. Rebuild whenever aethos is repainted.
6. Verifies every entry and fails past 504 tiles (the door animations own
   504-511). Writes build/thyrsa/catalog.json, the sheet, the pieces preview and
   design/phase3/TILES_thyrsa.md (keeping its hand-written passes section).

Usage: /usr/bin/python3 tools/ichor/art/thyrsa_build.py [--no-compile] [--preview out.png]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_build as EB  # noqa: E402
import emporion_lib as E  # noqa: E402
import thyrsa_art  # noqa: E402
import thyrsa_lib as T  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

ROOT = T.ROOT
IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/TILES_thyrsa.md"
# Thyrsa merges tiles within 4 px (Emporion's 2): the masonry's speckle is noise anyway,
# and the polish pass checked every 4 px merge by eye (TILES_thyrsa.md, "Polish pass")
NEAR_DUPLICATE_PX = 4
# Thyrsa City uses no animated door (every door is MB_NON_ANIMATED_DOOR, asserted in
# main()), so nothing ever writes tiles 504-511: the set may use all 512.
EB.TILE_LIMIT = 512
# A second, looser merge for opaque masonry and vine-leaf tiles only (merge_noise)
NOISE_PX = 6
PASSES_MARK = "<!-- passes: hand-written below this line; thyrsa_build.py keeps it -->"


def spec():
    name = "thyrsa"
    return SimpleNamespace(
        name=name, dir=name, symbol="gTileset_Thyrsa", groups=T.GROUPS, art=thyrsa_art,
        temple=False,
        src=ROOT / f"data/tilesets/secondary/{name}/porytiles_src",
        bin=ROOT / f"data/tilesets/secondary/{name}/porytiles_bin",
        cfg=ROOT / "porytiles/tilesets/gTileset_Thyrsa",
        scratch=ROOT / f"build/{name}_porytiles",
        out=ROOT / f"build/{name}",
        sheet=IMG / f"{name}_sheet.png",
        pieces=IMG / f"{name}_pieces.png")


# --------------------------------------------------------------------------
# The catalog
# --------------------------------------------------------------------------

INTRO = """\
# Thyrsa tileset catalog

`gTileset_Thyrsa` is Thyrsa City, the god's own city: Thebes renamed, walled on a long
hill, older and greyer than Corinth. Pair it with the `aethos` primary, which supplies
grass, paths, olives, cypresses, pines and the hillside outside the walls. Thyrsa's
interiors are `gTileset_ThyrsaRooms` (the rooms agent), the temple's is
`gTileset_TempleDionysus` and the theater's is `gTileset_Theater`.

**This file is generated** above the passes section. `tools/ichor/art/thyrsa_build.py`
draws the tileset, compiles it and rewrites the catalog. The art is in `thyrsa_walls.py`
(streets, walls and gates), `thyrsa_town.py` (the house kit, the Agora, the market and
the garlands), `thyrsa_civic.py` (the temple, the Asclepeion, Dirke, Semele's chamber) and
`thyrsa_vines.py`; the palette plan, the masonry and the painters are in `thyrsa_lib.py`.
The map is built by `tools/ichor/maps/thyrsa.py`, which places every piece by key and
part name from `build/thyrsa/catalog.json`.

![Every Thyrsa structure on its ground](img/thyrsa_pieces.png)

The numbered sheet is [img/thyrsa_sheet.png](img/thyrsa_sheet.png). The city's render is
[img/ThyrsaCity.png](img/ThyrsaCity.png).

## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}), so adding to one section never renumbers
another. `build/thyrsa/catalog.json` carries every structure's ids, walk codes, ground and
named parts.

**Collision and layers.** `X` impassable (collision 1), `.` passable, `D` a door (put the
warp here; `MB_NON_ANIMATED_DOOR`), `T` passable and drawn over the player. The vine rows
are `MB_TALL_GRASS`.

**Ground.** *aethos ground* (`grass`, `path`): the cell draws no ground of its own; the
build points its bottom layer at aethos's metatile (grass `0x001`, path `0x1D9`), so
rebuild whenever aethos is repainted. *flags* (`pave`): the street flags, drawn into the
bottom layer; the texture repeats every cell, so a prop on the flags meets the street
around it. *earth*: the vineyards' furrows. *none*: the art fills the cell.

**The masonry.** The city wall, the towers and the terrace walls share one Cyclopean
texture that repeats every 32 px. Pieces that continue a wall come as an even/odd pair:
put the even one on even map columns, or the blocks break at the joint. Wall pieces are
drawn for a wall whose battlement row is an even map row.

**Seams.** Keep this tileset out of the six rows nearest an up/down seam and the eight
columns nearest a left/right seam (MAP_DESIGN.md §5). Thyrsa's walls stand inside those
strips; the hillside outside them is aethos.

**Palettes.** Every 8x8 tile draws from one of seven groups (`thyrsa_lib.GROUPS`):

| Group | Use |
|---|---|
| stone | Theban stone: the Cyclopean walls, gates and towers, the street flags, kerbs, steps, terrace walls, Semele's chamber, Chthonia's house; ivy and smoke |
| clay | Terracotta roofs, ochre stucco, wine-purple doors and shutters, masks over doors |
| clay2 | The same, slot for slot, with limewash and vine-green paint |
| marble | The temple and the Asclepeion: marble, gold, painted blue and red; Dirke's water |
| fest | The festival: masks, garlands, ribbons, the awnings, the temple's painted doors |
| vine | The vineyards: vines, grapes, trellises, tilled earth; the fig |
| wood | The press, jars, barrels and stalls: timber, warm limestone, terracotta |

**Tile budget.** {tiles} of 512 tiles are used. Thyrsa has no animated door (every door is
`MB_NON_ANIMATED_DOOR`, and the build asserts it), so nothing writes tiles 504-511 and the
set may use all 512. Symmetric fronts are mirrored about a tile edge, the walls and flags
repeat on the 16 or 32 px grid, ivy is an overlay on the wall's own tiles, the limewashed
houses are free recolors, tiles within four pixels of another are redrawn as that tile,
and opaque masonry and vine-leaf tiles within six.

**Animation.** Semele's smoke has two frames. The build moves its six tiles to the
secondary's tiles 1-6 and writes the frames to `data/tilesets/secondary/thyrsa/anim/smoke/`;
`InitTilesetAnim_Thyrsa` in `src/tileset_anims.c` swaps them every 20 frames.
"""


def grid(ids):
    return [" ".join(f"0x{v:03X}" for v in r) for r in ids]


NAMED_GROUND = {"grass": "aethos grass", "path": "aethos path", "pave": "the street flags",
                "earth": "tilled earth", "sand": "aethos sand", "sea": "aethos sea"}


def structure_md(s):
    out = [f"### {s['title']}\n", f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n"]
    rows = grid(s["ids"])
    out.append("```text")
    out.append("ids".ljust(len(rows[0])) + "   walk")
    for r, w in zip(rows, s["walk"]):
        out.append(r + "   " + " ".join(w))
    out.append("```\n")
    kinds = {}
    for c, g in s.get("ground", {}).items():
        kinds.setdefault(g, []).append(c)
    shown = {k: v for k, v in kinds.items() if k != "none"}
    if shown:
        if len(kinds) == 1:
            out.append(f"Ground: all on {NAMED_GROUND[next(iter(shown))]}.\n")
        else:
            parts = []
            for kind, cells in sorted(shown.items()):
                cells = sorted(cells, key=lambda c: (int(c.split(',')[1]), int(c.split(',')[0])))
                parts.append(f"{NAMED_GROUND[kind]} at " + ", ".join(f"({c})" for c in cells))
            out.append("Ground: " + "; ".join(parts) + "; the rest draws its own.\n")
    for mb, label in (("MB_NON_ANIMATED_DOOR", "Door metatiles"),
                      ("MB_TALL_GRASS", "Tall grass (`MB_TALL_GRASS`)")):
        ids = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
               for c, b in s["behaviors"].items() if b == mb]
        if ids:
            out.append(f"{label}: {', '.join(ids)}.\n")
    names = s.get("names") or {}
    if names:
        out.append("Parts: " + ", ".join(f"`{n}` 0x{s['ids'][y][x]:03X}"
                                         for n, (x, y) in names.items()) + ".\n")
    return out


def recipes_md(data):
    import thyrsa_town as TT
    out = ["## House recipes\n",
           "Houses from the kit, as id grids (top row first). The city map builds each of its "
           "households from these parts, every one different.\n"]
    for i, r in enumerate(TT.RECIPES, 1):
        cells = TT.recipe_cells(r)
        rows = [" ".join(f"0x{data[k]['ids'][data[k]['names'][n][1]][data[k]['names'][n][0]]:03X}"
                         for k, n in row) for row in cells]
        out.append(f"**{i}. {r[0]}** ({len(cells[0])} wide, {len(cells)} tall)\n")
        out.append("```text")
        out += rows
        out.append("```\n")
    return out


def write_catalog(used):
    data = {s["key"]: s for s in json.loads((ROOT / "build/thyrsa/catalog.json").read_text())}
    starts = ", ".join(f"{t.lower()} at 0x{0x200 + row * 8:03X}" for row, _, t, _ in thyrsa_art.SECTIONS)
    out = [INTRO.format(starts=starts, tiles=used)]
    for row, key, title, blurb in thyrsa_art.SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for s in data.values():
            if s["section"] == key:
                out += structure_md(s)
        if key == "houses":
            out += recipes_md(data)
    passes = ""
    if DOC.exists() and PASSES_MARK in DOC.read_text():
        passes = DOC.read_text().split(PASSES_MARK, 1)[1]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(out).rstrip() + "\n\n" + PASSES_MARK + (passes or "\n"))
    print(DOC)


def merge_noise(structs, limit=NOISE_PX):
    """A second, looser merge for opaque tiles drawn only in the stone or vine groups:
    the Cyclopean masonry's speckle and the vine rows' leaves, where a few pixels'
    difference is noise. Masks, signs, doors and figures are never touched."""
    import numpy as np
    groups = [T.GROUP_RGB["stone"], T.GROUP_RGB["vine"]]
    occ = EB._tiles(structs)

    def noisy(k):
        a = np.frombuffer(k, np.uint8).reshape(8, 8, 4)
        cols = {tuple(int(c) for c in p[:3]) for p in a.reshape(64, 4)}
        return (a[..., 3] > 0).all() and any(cols <= g for g in groups)
    keys = [k for k in occ if noisy(k)]
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in EB._flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j > i:
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), 0
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped:
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = min(
                EB._flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
        dropped.add(drop)
        kept.add(keep)
        merges += 1
    return merges


# --------------------------------------------------------------------------
# Semele's smoke: the tileset's one animation
# --------------------------------------------------------------------------

ANIM_DIR = ROOT / "data/tilesets/secondary/thyrsa/anim/smoke"
SMOKE_FIRST_TILE = 1        # the frames land on tiles 1.. of the secondary (tile 0 is clear)
SMOKE_TILES = 6             # THYRSA_SMOKE_FIRST_TILE and _TILES in src/tileset_anims.c


def _read_pal(path):
    lines = path.read_text().split()
    n = int(lines[2])
    vals = [int(v) for v in lines[3:3 + 3 * n]]
    return [tuple(vals[i:i + 3]) for i in range(0, 3 * n, 3)]


def _flip(t, hf, vf):
    if hf:
        t = t[:, ::-1]
    if vf:
        t = t[::-1, :]
    return t


def animate_smoke(sp, structs):
    """Move Semele's smoke tiles to fixed slots (SMOKE_FIRST_TILE..) and write each
    frame's tiles as an indexed strip for src/tileset_anims.c. Every smoke tile must be
    the smoke's own (no other metatile uses it), or the walls would smoke too."""
    import numpy as np
    from PIL import Image
    import thyrsa_civic as TC
    sem = next(s for s in structs if s.key == "semele")
    frames = [None] + [finish_struct(TC.semele(frame=f)) for f in range(1, TC.SMOKE_FRAMES)]
    meta = np.fromfile(sp.bin / "metatiles.bin", "<u2").reshape(-1, 8)
    img = Image.open(sp.bin / "tiles.png")
    pal_img = img.getpalette()
    tiles_a = np.array(img)
    tiles = [tiles_a[y:y + 8, x:x + 8].copy() for y in range(0, tiles_a.shape[0], 8)
             for x in range(0, tiles_a.shape[1], 8)]
    pals = {p: _read_pal(sp.bin / f"palettes/{p:02d}.pal") for p in range(6, 13)}
    x0, y0, x1, y1 = TC.SMOKE_BOX
    slots = []          # (metatile index, entry, tx, ty)
    for ty in range(y0 // 8, y1 // 8):
        for tx in range(x0 // 8, x1 // 8):
            px = sem.T.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not (px[..., 3] > 0).any():
                continue
            cx, cy = tx // 2, ty // 2
            q = (ty % 2) * 2 + (tx % 2)
            m = sem.ids[cy][cx] - 0x200
            slots.append((m, 4 + q, tx, ty))
    # entries count tiles from the primary's start: the secondary's own are 512 and up
    SEC = 512
    used_by = {}
    for i, row in enumerate(meta):
        for j, e in enumerate(row):
            t = int(e) & 0x3FF
            if t >= SEC:
                used_by.setdefault(t - SEC, set()).add((i, j))
    assert len(slots) == SMOKE_TILES,         f"{len(slots)} smoke tiles: src/tileset_anims.c's THYRSA_SMOKE_TILES says {SMOKE_TILES}"
    smoke_tiles = []
    for (m, j, tx, ty) in slots:
        e = int(meta[m, j])
        t = (e & 0x3FF) - SEC
        assert t > 0, f"semele's smoke tile ({tx},{ty}) is empty in the compiled set"
        assert used_by[t] == {(m, j)}, \
            f"smoke tile {t} at ({tx},{ty}) is shared with {used_by[t]}: it would animate elsewhere"
        smoke_tiles.append(t)
    assert len(set(smoke_tiles)) == len(smoke_tiles)
    # swap each smoke tile into its slot, renumbering every entry that points at either
    order = list(range(len(tiles)))
    for k, t in enumerate(smoke_tiles):
        dst = SMOKE_FIRST_TILE + k
        cur = order.index(t)
        order[cur], order[dst] = order[dst], order[cur]
    new_index = {old: new for new, old in enumerate(order)}
    tiles = [tiles[old] for old in order]
    for i in range(len(meta)):
        for j in range(8):
            e = int(meta[i, j])
            t = e & 0x3FF
            if t >= SEC:
                meta[i, j] = (e & ~0x3FF) | (SEC + new_index[t - SEC])
    # Porytiles picks each tile's palette from frame 0's colors alone; a later frame may
    # need a color that palette lacks (smoke white beside a pale stone). Move each smoke
    # tile to a palette that holds every frame's colors, re-indexing frame 0 to match.
    for k, (m, j, tx, ty) in enumerate(slots):
        e = int(meta[m, j])
        old = pals[e >> 12]
        # tiles.png holds palette * 16 + color (Porytiles' debug layout; gbagfx keeps
        # the low nibble), color 0 clear
        rgb0 = [[old[v & 15] if v & 15 else None for v in row] for row in tiles[SMOKE_FIRST_TILE + k]]
        need = {c for row in rgb0 for c in row if c}
        for f in range(1, TC.SMOKE_FRAMES):
            px = frames[f].T.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            need |= {tuple(int(v) for v in p[:3]) for p in px.reshape(64, 4) if p[3]}
        fits = [p for p in range(6, 13) if need <= set(pals[p][1:])]
        assert fits, f"no palette holds smoke tile ({tx},{ty})'s colors {need}"
        p = (e >> 12) if (e >> 12) in fits else fits[0]
        tiles[SMOKE_FIRST_TILE + k] = np.array(
            [[p * 16 + pals[p].index(c, 1) if c else 0 for c in row] for row in rgb0], np.uint8)
        meta[m, j] = (e & 0x0FFF) | (p << 12)
    meta.astype("<u2").tofile(sp.bin / "metatiles.bin")
    cols = 16
    out = np.zeros_like(tiles_a)
    for n, tl in enumerate(tiles):
        out[(n // cols) * 8:(n // cols) * 8 + 8, (n % cols) * 8:(n % cols) * 8 + 8] = tl
    im = Image.fromarray(out, "P")
    im.putpalette(pal_img)
    im.save(sp.bin / "tiles.png")
    # the frames: frame 0 is the compiled tiles themselves; later frames are drawn
    # with the same palette and flips as the entries that show them
    ANIM_DIR.mkdir(parents=True, exist_ok=True)
    for f in range(TC.SMOKE_FRAMES):
        strip = np.zeros((8 * len(slots), 8), np.uint8)
        for k, (m, j, tx, ty) in enumerate(slots):
            e = int(meta[m, j])
            if f == 0:
                ind = tiles[SMOKE_FIRST_TILE + k]
            else:
                p = e >> 12
                pal = pals[p]
                px = frames[f].T.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                ind = np.zeros((8, 8), np.uint8)
                for yy in range(8):
                    for xx in range(8):
                        if px[yy, xx, 3]:
                            rgb = tuple(int(v) for v in px[yy, xx, :3])
                            assert rgb in pal[1:], f"smoke frame {f}: {rgb} isn't in palette {p}"
                            ind[yy, xx] = p * 16 + pal.index(rgb, 1)
                ind = _flip(ind, (e >> 10) & 1, (e >> 11) & 1)
            strip[k * 8:k * 8 + 8] = ind
        im = Image.fromarray(strip, "P")
        im.putpalette(pal_img)
        im.save(ANIM_DIR / f"{f}.png")
    x0, y0, x1, y1 = TC.SMOKE_BOX
    for f in range(1, TC.SMOKE_FRAMES):
        a = frames[f].T.a
        outside = a[..., 3].copy()
        for (m, j, tx, ty) in slots:
            outside[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = 0
        outside[:, :x0] = 0
        outside[:, x1:] = 0
        outside[y1:, :] = 0
        assert not outside.any(), f"smoke frame {f} draws outside frame 0's tiles"
    print(f"semele's smoke: {len(slots)} tiles at {SMOKE_FIRST_TILE}-"
          f"{SMOKE_FIRST_TILE + len(slots) - 1}, {TC.SMOKE_FRAMES} frames in "
          f"{ANIM_DIR.relative_to(ROOT)}")
    return len(slots)


def finish_struct(s):
    """A later frame of Semele's chamber, drawn fresh (thyrsa_civic.semele(frame=n));
    only the smoke's own tiles are read from it."""
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    sp = spec()
    sections = thyrsa_art.build()
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = T.validate(structs)
    if not probs:
        before = len(EB._tiles(structs))
        merges = EB.merge_near_duplicates(structs, limit=NEAR_DUPLICATE_PX)
        noise = merge_noise(structs)
        print(f"merged {len(merges)} near-duplicate tiles and {noise} masonry and leaf tiles: "
              f"{before} -> {len(EB._tiles(structs))} distinct tiles before palette sharing")
        probs = T.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        E.preview(structs, scale=2, cols=5).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    doors = [(s.key, c) for s in structs for c, b in s.behaviors.items() if b == "MB_ANIMATED_DOOR"]
    assert not doors, f"animated doors {doors}: they would overwrite tiles 504-511"
    rows = pack(sections)
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, sp.src)
    EB.catalog_json(sp, structs)
    if args.no_compile:
        return
    EB.compile_tileset(sp)
    patched = EB.borrow_ground(sp, structs)
    animate_smoke(sp, structs)
    used = EB.verify(sp, rows, patched)
    print("colors per palette 6-12:", EB.palette_report(sp))
    IMG.mkdir(parents=True, exist_ok=True)
    EB.images(sp, structs)
    write_catalog(used)


if __name__ == "__main__":
    main()
