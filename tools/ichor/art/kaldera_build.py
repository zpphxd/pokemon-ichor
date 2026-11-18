#!/usr/bin/env python3
"""Paint, slice, compile and register gTileset_Kaldera (design/AWE_PASS.md item 3).

1. Paints Kaldera whole (kaldera_art.paint) in each animation frame, and once
   more with the bronze man's eyes lit (the after-Laurel-6 swap).
2. Snaps every 8x8 tile of every layer to the one palette group it fits best
   (kaldera_art.GROUPS), then slices the scene into distinct 16x16 cells: one
   metatile each. Plain sea cells stay aethos's 0x170; cells where the sea
   shows through borrow aethos's animated sea under their art.
3. Runs kythera_build's pipeline: pack, Porytiles in a scratch project, the
   borrowed sea, registration in src/data/tilesets/*.h, verification against
   the 504-tile limit.
4. Writes tools/ichor/maps/kaldera_tiles.py (the map's metatile grid, its walk
   codes and the eyes-lit swap) for tools/ichor/maps/kaldera.py, and previews
   in build/render/kaldera/.

Usage: /usr/bin/python3 tools/ichor/art/kaldera_build.py [--no-compile] [--preview]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kaldera_art as KA  # noqa: E402
import kythera_build as KB  # noqa: E402
import kythera_lib as K  # noqa: E402
import agros_lib as A  # noqa: E402

ROOT = K.ROOT
OUT = ROOT / "build/render/kaldera"
TILES_PY = ROOT / "tools/ichor/maps/kaldera_tiles.py"
SEA = 0x170
FRAMES = 3
MERGE_PX = 12
FIGURE_PX = 4

SPEC = {
    "symbol": "gTileset_Kaldera", "dir": "kaldera", "label": "Kaldera",
    "title": "Kaldera, Thera's caldera, the white town and the bronze man",
    "groups": KA.GROUPS,
    "rows": {"scene": 0},
}

GROUP_RGB = {g: np.array([KA.P[n] for n in names], np.int32) for g, names in KA.GROUPS.items()}
WEIGHT = np.array([3, 4, 2])


def snap_tile(tiles):
    """Snap a list of 8x8 RGBA tiles (one tile over its frames) to the best group."""
    stack = np.stack(tiles)
    m = stack[..., 3] > 0
    if not m.any():
        return
    px = stack[..., :3][m].astype(np.int32)
    best, best_err, best_idx = None, None, None
    for g, pal in GROUP_RGB.items():
        d = (((px[:, None, :] - pal[None, :, :]) ** 2) * WEIGHT).sum(-1)
        idx = d.argmin(1)
        err = d[np.arange(len(px)), idx].sum()
        if best_err is None or err < best_err:
            best, best_err, best_idx = g, err, idx
    stack[..., :3][m] = GROUP_RGB[best][best_idx].astype(np.uint8)
    for t, s in zip(tiles, stack):
        t[:] = s


def layers_of(cv):
    """Split a painted canvas into per-cell bottom/middle/top and borrowed sea."""
    Hp, Wp = cv.U.shape[:2]
    B = np.zeros_like(cv.U)
    M = np.zeros_like(cv.U)
    T = cv.T.copy()
    sea = set()
    aethos = set()
    for y in range(KA.H):
        for x in range(KA.W):
            sl = np.s_[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16]
            u = cv.U[sl]
            holes = (u[..., 3] == 0).any()
            if holes:
                if not (u[..., 3] > 0).any() and not (T[sl][..., 3] > 0).any():
                    aethos.add((x, y))
                    continue
                sea.add((x, y))
                M[sl] = u
                if (T[sl][..., 3] > 0).any() and (u[..., 3] > 0).any():
                    # borrowed ground can't use both upper layers: fold the top down
                    t = T[sl]
                    mm = t[..., 3] > 0
                    M[sl][mm] = t[mm]
                    T[sl] = 0
            else:
                B[sl] = u
    return B, M, T, sea, aethos


def paint_all():
    frames = [KA.paint(frame=f) for f in range(FRAMES)]
    eyes = KA.paint(frame=0, eyes=True)
    return frames, eyes


def build(compile_=True, preview_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    frames, eyes = paint_all()
    split = [layers_of(cv) for cv in frames]
    B0, M0, T0, sea, aethos_cells = split[0]
    E = layers_of(eyes)
    cv0 = frames[0]
    # snap: per cell, per layer tile, union over frames
    stacks = {"bottom": [s[0] for s in split], "middle": [s[1] for s in split],
              "top": [s[2] for s in split]}
    eyes_l = {"bottom": E[0], "middle": E[1], "top": E[2]}
    for ln, arrs in stacks.items():
        for ty in range(KA.H * 2):
            for tx in range(KA.W * 2):
                sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                snap_tile([a[sl] for a in arrs])
                snap_tile([eyes_l[ln][sl]])
    preview(stacks, sea, aethos_cells, OUT / "kaldera_scene.png")
    if preview_only:
        return
    # the scene as a kythera Struct, with its animation frames
    s = K.struct("scene", "Kaldera", KA.W, KA.H, "scene",
                 walk=["".join(ch if ch in "GDSW" else "." for ch in row) for row in cv0.walk])
    s.layers["bottom"].a[:] = stacks["bottom"][0]
    s.layers["middle"].a[:] = stacks["middle"][0]
    s.layers["top"].a[:] = stacks["top"][0]
    for ln, an in (("bottom", "lava"), ("middle", "lavas"), ("top", "seam")):
        fr = []
        for f in range(1, FRAMES):
            L = A.Layer(KA.W * 16, KA.H * 16)
            L.a[:] = stacks[ln][f]
            fr.append(L)
        if any(not np.array_equal(f_.a, s.layers[ln].a) for f_ in fr):
            s.anims[an] = {"layer": ln, "frames": fr}
    for cell in sea:
        s.ground[cell] = "sea"
    KB.ANIM_ORDER.update({"lava": ["0", "1", "2"], "lavas": ["0", "1", "2"], "seam": ["0", "1", "2"]})
    # distinct cells
    def cell_key(x, y, layers):
        sl = np.s_[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16]
        parts = [layers[ln][f][sl].tobytes() for ln in ("bottom", "middle", "top")
                 for f in range(len(layers[ln]))]
        return (b"".join(parts), (x, y) in sea, s.walk[y][x] if s.walk[y][x] in "GDSW" else ".")

    uniq, where = {}, {}
    for y in range(KA.H):
        for x in range(KA.W):
            if (x, y) in aethos_cells:
                continue
            k = cell_key(x, y, stacks)
            if k not in uniq:
                uniq[k] = f"c{len(uniq)}"
                s.names[uniq[k]] = (x, y)
            where[(x, y)] = uniq[k]
    # the eyes-lit cells: painted into a second struct and sliced the same way
    swaps = []
    es = K.struct("eyes", "Kaldera, eyes lit", KA.W, KA.H, "scene")
    for ln in ("bottom", "middle", "top"):
        es.layers[ln].a[:] = eyes_l[ln]
    for y in range(KA.H):
        for x in range(KA.W):
            sl = np.s_[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16]
            if any(not np.array_equal(eyes_l[ln][sl], stacks[ln][0][sl]) for ln in eyes_l):
                swaps.append((x, y))
                if (x, y) in sea:
                    es.ground[(x, y)] = "sea"
                es.names[f"e{len(swaps) - 1}"] = (x, y)
    print(f"kaldera: {len(uniq)} distinct cells, {len(swaps)} eye cells, "
          f"{len(aethos_cells)} plain sea, {len(sea)} on borrowed sea")
    cells = K.pick(s, [f"c{i}" for i in range(len(uniq))], w=8, key="cells", section="scene")
    struct_list = [cells]
    if swaps:
        struct_list.append(K.pick(es, [f"e{i}" for i in range(len(swaps))], w=8, key="eyes",
                                  section="scene"))
    group_rgb = {g: {KA.P[n] for n in names} for g, names in KA.GROUPS.items()}
    probs = K.validate(struct_list, group_rgb)
    if not probs:
        before = len(K.tiles_of(struct_list))
        animated = {id(st): K.anim_tiles(st) for st in struct_list}
        merges = merge_layered(struct_list, group_rgb)
        resync(struct_list, animated)
        print(f"kaldera: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(K.tiles_of(struct_list))}")
        probs = K.validate(struct_list, group_rgb)
    for p in probs[:30]:
        print("PROBLEM:", p)
    if probs:
        sys.exit(f"{len(probs)} problems")
    sp = dict(SPEC, sections=[("scene", struct_list)])
    KB.fix_keys(struct_list)
    KB.check_anim_keys(struct_list)
    print(f"kaldera: {len(K.tiles_of(struct_list))} tiles after the animation keys")
    rows, used = KB.pack(sp)
    print(f"kaldera: {rows} sheet rows ({rows * 8} metatile slots)")
    KB.write_sources(sp, struct_list, rows, used)
    ids = {}
    for name, (sx, sy) in cells.names.items():
        ids[name] = cells.ids[sy][sx]
    grid = [[SEA if (x, y) in aethos_cells else ids[where[(x, y)]] for x in range(KA.W)]
            for y in range(KA.H)]
    swap_ids = []
    if swaps:
        e = struct_list[1]
        for i, (x, y) in enumerate(swaps):
            ex, ey = e.names[f"e{i}"]
            swap_ids.append((x, y, e.ids[ey][ex]))
    write_tiles_py(grid, cv0, swap_ids)
    if not compile_:
        return
    animated = KB.compile_tileset(sp, KA.GROUPS)
    cfg = ROOT / "porytiles/tilesets" / SPEC["symbol"] / "config.yaml"
    cfg.write_text(cfg.read_text().replace("kythera_build.py", "kaldera_build.py"))
    patched = KB.borrow_ground(sp, struct_list)
    register(sp, animated)
    n_tiles, n_meta = KB.verify(sp, rows, patched)
    print(f"kaldera: {n_tiles} tiles, {n_meta} metatiles")
    KB.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", SPEC["symbol"],
            "--primary", "aethos", "--scale", "2", "-o", str(OUT / "kaldera_sheet.png")])


def merge_layered(structs, group_rgb):
    """kythera_lib.merge_near_duplicates with a limit per layer: ground and cliffs
    (bottom, middle) merge within MERGE_PX pixels, the figures drawn over the
    player (top: the bronze man, roofs, the pediment) only within FIGURE_PX, so
    a face or a hand is never redrawn as its neighbor."""
    occ = K.tiles_of(structs, include_anim=False)
    keys = list(occ)
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    tops = {id(s.layers["top"]) for s in structs}

    def lim(k):
        return FIGURE_PX if any(id(o[1]) in tops for o in occ[k]) else MERGE_PX

    def grp(k):
        a = arr[k]
        m = a[..., 3] > 0
        return K.which_group({tuple(int(v) for v in p) for p in a[m][:, :3]}, group_rgb)
    groups = {k: grp(k) for k in keys}
    limits = {k: lim(k) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in K._flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= MERGE_PX)[0]:
            if j > i and best[j] <= min(limits[k], limits[keys[j]]):
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), []
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped or groups[a] != groups[b]:
            continue
        if ((arr[a][..., 3] > 0) != (arr[b][..., 3] > 0)).any() and \
                all(((v[..., 3] > 0) != (arr[a][..., 3] > 0)).any() for v in K._flips(arr[b])):
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (_, layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            best = min(K._flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
            if ((best[..., 3] > 0) != (cur[..., 3] > 0)).any():
                continue
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = best
        dropped.add(drop)
        kept.add(keep)
        merges.append(d)
    return merges


def resync(structs, animated):
    """A merge redraws static tiles on the base layer only: copy them into the
    animation frames too, so they don't turn into spurious animated tiles."""
    for st in structs:
        at = animated[id(st)]
        for an_name, an in st.anims.items():
            base = st.layers[an["layer"]].a
            for ty in range(st.h * 2):
                for tx in range(st.w * 2):
                    if (an["layer"], tx, ty) in at:
                        continue
                    sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    for f in an["frames"]:
                        f.a[sl] = base[sl]


def register(sp, animated):
    """kythera_build's registration, with Kaldera's comment."""
    KB.register(sp, animated)
    hdr = ROOT / "src/data/tilesets/headers.h"
    t = hdr.read_text()
    t = t.replace(f"// Ichor: kaldera, {sp['title']} (Act III).",
                  "// Ichor: kaldera, Thera's caldera, the white town and the bronze man (Act II).")
    t = t.replace("tools/ichor/art/kythera_build.py for the aethos primary: its ground cells\n"
                  "// borrow aethos's grass, path, sand, sea, shallows and waterfall, so rebuild\n"
                  "// it whenever aethos changes.\nconst struct Tileset gTileset_Kaldera",
                  "tools/ichor/art/kaldera_build.py for the aethos primary: the map is painted\n"
                  "// whole and sliced into cells; cells over the sea borrow aethos's sea, so\n"
                  "// rebuild it whenever aethos changes.\nconst struct Tileset gTileset_Kaldera")
    hdr.write_text(t)


def write_tiles_py(grid, cv, swaps):
    walk = ["".join("X" if cv.solid[y, x] else cv.walk[y][x] for x in range(KA.W))
            for y in range(KA.H)]
    TILES_PY.write_text(
        '"""Kaldera\'s metatile grid on gTileset_Kaldera. Generated by\n'
        'tools/ichor/art/kaldera_build.py; do not edit.\n\n'
        "GRID: rows of metatile ids (0x170 is aethos's sea).\n"
        "WALK: rows of walk codes: X solid, . open, S sand, G scrub (tall grass),\n"
        "D door, W water (open sea, elevation 1).\n"
        "EYES: (x, y, metatile) the bronze man's eyes lit, swapped in after Laurel 6.\n"
        '"""\n\n'
        f"SYMBOL = 'gTileset_Kaldera'\n"
        f"GRID = {json.dumps(grid)}\n"
        f"WALK = {json.dumps(walk, indent=0)}\n"
        f"EYES = {json.dumps(swaps)}\n")


def preview(stacks, sea, aethos_cells, path, frame=0):
    img = np.zeros((KA.H * 16, KA.W * 16, 3), np.uint8)
    seapx = A.aethos(SEA)
    for y in range(KA.H):
        for x in range(KA.W):
            img[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16] = seapx
    for ln in ("bottom", "middle", "top"):
        a = stacks[ln][frame]
        m = a[..., 3] > 0
        img[m] = a[..., :3][m]
    Image.fromarray(img).save(path)
    Image.fromarray(img).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(
        str(path).replace(".png", "_2x.png"))
    print(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    build(not args.no_compile, args.preview)


if __name__ == "__main__":
    main()
