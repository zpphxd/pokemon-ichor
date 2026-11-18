#!/usr/bin/env python3
"""Fail on connection seams that draw a neighbor's cells with the wrong tiles.

In Gen 3 a connected map is drawn with the *current* map's tilesets. A neighbor
cell whose metatile id is in the secondary range (>= 0x200) therefore draws
from the current map's secondary tileset, and looks like garbage unless that
metatile happens to be identical in both (some secondaries are built to share a
run of metatiles, e.g. styx_falls and kyllene).

For every connection in data/maps/*/map.json this takes the neighbor's cells the
player can see from the current map and checks that each one renders the same
pixels under the current map's tilesets as under its own. The visible strip
follows design/MAP_DESIGN.md: 6 rows along an up/down seam, 8 columns along a
left/right one (the camera shows 4 rows above the player, 5 below and 7 each
side, plus one while scrolling). Along the seam it spans the overlap widened by
the engine's MAP_OFFSET (7) each way, since fieldmap.c fills that far past the
current map's corners and the camera shows it from a corner. A cell counts only
when some cell the player can reach (tools/ichor/mapdata.py's walker, with surf
and every relic) is close enough for the camera to show it. Every map's own
connection list is checked, so each seam is checked from both sides.

When a tileset's graphics can't be resolved, a cell fails if its id is in the
secondary range and the secondaries differ.

Usage: seam_audit.py [-v] [--rows N] [--cols N]   exit 1 on any violation.
"""
import json
import re
import struct
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
NUM_PRIMARY = 0x200           # NUM_METATILES_IN_PRIMARY and NUM_TILES_IN_PRIMARY
NUM_PALS_IN_PRIMARY = 6
MAP_OFFSET = 7
ROWS, COLS = 6, 8


def load():
    layouts = {l["id"]: l for l in json.loads((REPO / "data/layouts/layouts.json").read_text())["layouts"] if "id" in l}
    maps = {}
    for p in sorted((REPO / "data/maps").glob("*/map.json")):
        m = json.loads(p.read_text())
        maps[m["id"]] = m
    return layouts, maps


_bins = {}


def grid(lay):
    key = lay["blockdata_filepath"]
    if key not in _bins:
        raw = (REPO / key).read_bytes()
        v = struct.unpack(f"<{len(raw) // 2}H", raw)
        w = lay["width"]
        _bins[key] = [[c & 0x3FF for c in v[y * w:(y + 1) * w]] for y in range(lay["height"])]
    return _bins[key]


# --- tileset graphics -------------------------------------------------------------
@lru_cache(None)
def _sources():
    hdr = (REPO / "src/data/tilesets/headers.h").read_text()
    gfx = (REPO / "src/data/tilesets/graphics.h").read_text()
    mts = (REPO / "src/data/tilesets/metatiles.h").read_text()
    sets = {}
    for m in re.finditer(r"const struct Tileset (\w+) =\s*\{(.*?)\};", hdr, re.S):
        fields = dict(re.findall(r"\.(\w+)\s*=\s*(\w+)", m.group(2)))
        sets[m.group(1)] = fields
    return sets, gfx, mts


def _incbins(text, sym):
    m = re.search(rf"\b{sym}\b\s*\[\][^=]*=\s*(\{{.*?\}};|INCBIN_U\d+\(\"[^\"]+\"\))", text, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def _read_pal(path):
    p = REPO / path
    jasc = p.with_suffix(".pal")
    if jasc.exists():
        lines = jasc.read_text().split()
        nums = list(map(int, lines[3:3 + 48]))
        return tuple(tuple(nums[i:i + 3]) for i in range(0, 48, 3))
    if p.exists():
        v = struct.unpack("<16H", p.read_bytes()[:32])
        return tuple(((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3) for c in v)
    return None


@lru_cache(None)
def tileset(name):
    """(metatiles[n,8], tiles[n,8,8] colour indices, palettes[16]) or None if unresolvable."""
    sets, gfx, mts = _sources()
    f = sets.get(name)
    if not f:
        return None
    try:
        tpath = _incbins(gfx, f["tiles"])[0]
        png = REPO / re.sub(r"\.4bpp(\.lz|\.smol|\.fastSmol)?$", ".png", tpath)
        im = np.array(Image.open(png))
        tiles = im.reshape(im.shape[0] // 8, 8, im.shape[1] // 8, 8).transpose(0, 2, 1, 3).reshape(-1, 8, 8) & 0xF
        pals = [_read_pal(p) for p in _incbins(gfx, f["palettes"])]
        mpath = _incbins(mts, f["metatiles"])[0]
        meta = np.frombuffer((REPO / mpath).read_bytes(), "<u2").reshape(-1, 8)
    except (IndexError, KeyError, OSError, ValueError):
        return None
    if None in pals or len(pals) < 13:
        return None
    return meta, tiles, pals


@lru_cache(None)
def render(pri, sec, mid):
    """A metatile's pixels under a primary/secondary pair, as a hashable signature."""
    P, S = tileset(pri), tileset(sec)
    meta = P[0] if mid < NUM_PRIMARY else S[0]
    i = mid if mid < NUM_PRIMARY else mid - NUM_PRIMARY
    if i >= len(meta):
        return ("missing metatile",)
    out = []
    for e in meta[i]:
        e = int(e)
        t, pal = e & 0x3FF, e >> 12
        src, ti = (P[1], t) if t < NUM_PRIMARY else (S[1], t - NUM_PRIMARY)
        if ti >= len(src):
            out.append(("missing tile",))
            continue
        px = src[ti]
        if e & 0x400:
            px = px[:, ::-1]
        if e & 0x800:
            px = px[::-1, :]
        colours = (P if pal < NUM_PALS_IN_PRIMARY else S)[2][pal]
        out.append(tuple(None if c == 0 else colours[c] for c in px.flat))
    return tuple(out)


def same_look(cur, nb, mid):
    cp, cs, np_, ns = cur["primary_tileset"], cur["secondary_tileset"], nb["primary_tileset"], nb["secondary_tileset"]
    if cp == np_ and cs == ns:
        return True
    if all(tileset(t) is not None for t in (cp, cs, np_, ns)):
        return render(cp, cs, mid) == render(np_, ns, mid)
    return cp == np_ and mid < NUM_PRIMARY


# --- the seams ----------------------------------------------------------------------
def visible_cells(cur, nb, direction, offset):
    """Yield (nx, ny) neighbor cells visible from the current map across this connection."""
    cw, ch, nw, nh = cur["width"], cur["height"], nb["width"], nb["height"]
    if direction in ("up", "down"):
        rows = range(nh - ROWS, nh) if direction == "up" else range(0, ROWS)
        for cx in range(-MAP_OFFSET, cw + MAP_OFFSET):
            nx = cx - offset
            if 0 <= nx < nw:
                for ny in rows:
                    if 0 <= ny < nh:
                        yield nx, ny
    else:
        cols = range(nw - COLS, nw) if direction == "left" else range(0, COLS)
        for cy in range(-MAP_OFFSET, ch + MAP_OFFSET):
            ny = cy - offset
            if 0 <= ny < nh:
                for nx in cols:
                    if 0 <= nx < nw:
                        yield nx, ny


def to_current(cur, nb, direction, offset, nx, ny):
    """A neighbor cell's position in the current map's coordinates."""
    if direction == "up":
        return nx + offset, ny - nb["height"]
    if direction == "down":
        return nx + offset, cur["height"] + ny
    if direction == "left":
        return nx - nb["width"], ny + offset
    return cur["width"] + nx, ny + offset


_reach = {}


def reachable(name):
    """Cells a player can stand on in this map (mapdata's walker, from every entry)."""
    if name not in _reach:
        from mapdata import Map, Repo, Walker, entries
        repo = _reach.setdefault("repo", Repo())
        m = Map(repo, name)
        w = Walker(m, surf=True, relics=True)
        starts = [s for _, tiles in entries(m) for s in w.starts(tiles)]
        _reach[name] = {(x, y) for x, y, _ in w.reach(starts)}
    return _reach[name]


def seen_from(cells, cx, cy):
    """Whether the camera shows (cx, cy) from any of these player cells: 8 columns
    each side, 5 rows above and 6 below, counting the step that scrolls."""
    return any(abs(cx - px) <= COLS and -(ROWS - 1) <= cy - py <= ROWS for px, py in cells)


def violations():
    layouts, maps = load()
    out, checked = [], 0
    for m in maps.values():
        cur = layouts.get(m["layout"])
        for c in m.get("connections") or []:
            if c["direction"] not in ("up", "down", "left", "right"):
                continue  # dive / emerge connections are full map changes
            nm = maps.get(c["map"])
            if cur is None or nm is None:
                continue
            nb = layouts[nm["layout"]]
            checked += 1
            g = grid(nb)
            bad = []
            for nx, ny in visible_cells(cur, nb, c["direction"], c["offset"]):
                if same_look(cur, nb, g[ny][nx]):
                    continue
                cx, cy = to_current(cur, nb, c["direction"], c["offset"], nx, ny)
                if not seen_from(reachable(m["name"]), cx, cy):
                    continue                     # no cell the player reaches is close enough
                bad.append((nx, ny, g[ny][nx]))
            if bad:
                out.append((m["name"], c["direction"], nm["name"], cur, nb, bad))
    return out, checked


def main(argv):
    global ROWS, COLS
    if "--rows" in argv:
        ROWS = int(argv[argv.index("--rows") + 1])
    if "--cols" in argv:
        COLS = int(argv[argv.index("--cols") + 1])
    problems, checked = violations()
    for name, d, nbname, cur, nb, bad in problems:
        print(f"SEAM FAIL: from {name} ({cur['secondary_tileset']}) looking {d} at {nbname} "
              f"({nb['secondary_tileset']}): {len(bad)} cells draw wrong")
        shown = bad if "-v" in argv else bad[:6]
        print("   " + ", ".join(f"({x},{y})=0x{v:03X}" for x, y, v in shown) + (" ..." if len(shown) < len(bad) else ""))
    if not problems:
        print(f"seam_audit: {checked} connections, every visible seam cell draws with the right tiles")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
