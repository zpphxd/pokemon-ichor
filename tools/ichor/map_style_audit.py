#!/usr/bin/env python3
"""Measure outdoor maps against the look rules in design/STYLE.md §4.2.

map_audit.py checks how a map plays; this checks how it looks. Numbers per map:

  flat     share of walkable cells that are the single most common metatile.
           Open ground wants a base (70-85%) plus variants and accents.
           FAIL above 90%.
  barren   share of 15x10 screens with 6 or fewer distinct metatiles: screens
           with nothing to look at. WARN above 10%, FAIL above 25%.
  straight longest straight run (cells) of a boundary between walkable and
           blocked ground with no step. WARN above 10 (STYLE.md asks for a
           step, notch or object every 6), FAIL above 20.
  levels   distinct ground elevations plus ledges and stairs; 0 means a flat
           map. WARN when a town or route has no height at all.
  props    distinct metatiles across the map; low numbers read as placeholder.
           WARN under 30.

  tools/ichor/map_style_audit.py                 every outdoor Ichor map
  tools/ichor/map_style_audit.py ThyrsaCity ...  just these maps
  tools/ichor/map_style_audit.py --root DIR      another tree (e.g. a worktree)

A score orders the list worst first. These are heuristics for where to look,
not artistic approval: always render and judge (STYLE.md §4.4).
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import REPO, Map, Repo  # noqa: E402

SKIP_TYPES = {"MAP_TYPE_INDOOR", "MAP_TYPE_SECRET_BASE", "MAP_TYPE_UNDERGROUND", "MAP_TYPE_OCEAN_ROUTE"}


def measure(m):
    walk, ids_all = [], Counter()
    for y in range(m.h):
        for x in range(m.w):
            mid, col, elev = m.cell(x, y)
            ids_all[mid] += 1
            if m.open(x, y):
                walk.append((x, y, mid, elev))
    ids = Counter(mid for _, _, mid, _ in walk)
    flat = ids.most_common(1)[0][1] / len(walk) if walk else 0

    screens = barren = 0
    for sy in range(0, max(1, m.h - 9), 10):
        for sx in range(0, max(1, m.w - 14), 15):
            seen = {m.cell(x, y)[0] for y in range(sy, min(m.h, sy + 10)) for x in range(sx, min(m.w, sx + 15))}
            screens += 1
            barren += len(seen) <= 6

    def run_length(cells_fn, outer, inner):
        best = 0
        for a in range(outer):
            run = 0
            for b in range(inner):
                if cells_fn(a, b):
                    run += 1
                    best = max(best, run)
                else:
                    run = 0
        return best

    op = {(x, y) for x, y, _, _ in walk}
    blocked = lambda x, y: 0 <= x < m.w and 0 <= y < m.h and (x, y) not in op  # noqa: E731
    horiz = max(run_length(lambda y, x: (x, y) in op and blocked(x, y + d), m.h, m.w) for d in (-1, 1))
    vert = max(run_length(lambda x, y: (x, y) in op and blocked(x + d, y), m.w, m.h) for d in (-1, 1))
    straight = max(horiz, vert)

    elevs = {e for _, _, _, e in walk if e not in (0, 15)}
    ledges = sum(1 for y in range(m.h) for x in range(m.w)
                 if (m.behavior_at(x, y) or "").startswith(("MB_JUMP", "MB_STAIRS", "MB_SIDEWAYS_STAIRS")))
    levels = max(0, len(elevs) - 1) + (1 if ledges else 0)

    return {"flat": flat, "barren": barren / screens if screens else 0, "straight": straight,
            "levels": levels, "props": len(ids_all), "size": f"{m.w}x{m.h}"}


def verdicts(r):
    out = []
    if r["flat"] > 0.90:
        out.append(("FAIL", f"ground is {r['flat']:.0%} one metatile"))
    elif r["flat"] > 0.85:
        out.append(("WARN", f"ground is {r['flat']:.0%} one metatile"))
    if r["barren"] > 0.25:
        out.append(("FAIL", f"{r['barren']:.0%} of screens are barren"))
    elif r["barren"] > 0.10:
        out.append(("WARN", f"{r['barren']:.0%} of screens are barren"))
    if r["straight"] > 20:
        out.append(("FAIL", f"a {r['straight']}-cell straight edge"))
    elif r["straight"] > 10:
        out.append(("WARN", f"a {r['straight']}-cell straight edge"))
    if r["levels"] == 0:
        out.append(("WARN", "no height: no ledge, stair or elevation change"))
    if r["props"] < 30:
        out.append(("WARN", f"only {r['props']} distinct metatiles"))
    return out


def score(r):
    return (max(0, r["flat"] - 0.80) * 100 + r["barren"] * 60 + max(0, r["straight"] - 6) * 1.5
            + (8 if r["levels"] == 0 else 0) + max(0, 40 - r["props"]) * 0.5)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("maps", nargs="*")
    ap.add_argument("--root", default=REPO)
    ap.add_argument("--json", help="also write the numbers here")
    a = ap.parse_args()
    repo = Repo(a.root)
    names = a.maps or [n for n in repo.names
                       if repo.map_json(n).get("map_type") not in SKIP_TYPES
                       and not n.startswith(("Littleroot", "Oldale", "Route1", "Inside", "Battle"))]
    rows = []
    for n in names:
        try:
            m = Map(repo, n)
        except Exception as e:  # a map the tree can't load
            print(f"{n}: can't load ({e})", file=sys.stderr)
            continue
        r = measure(m)
        r["name"], r["score"], r["verdicts"] = n, score(r), verdicts(r)
        rows.append(r)
    rows.sort(key=lambda r: -r["score"])
    print(f"{'map':32s} {'size':>7s} {'flat':>5s} {'barren':>6s} {'straight':>8s} {'levels':>6s} {'props':>5s} {'score':>6s}")
    for r in rows:
        print(f"{r['name']:32s} {r['size']:>7s} {r['flat']:5.0%} {r['barren']:6.0%} {r['straight']:8d} "
              f"{r['levels']:6d} {r['props']:5d} {r['score']:6.1f}")
        for level, text in r["verdicts"]:
            print(f"    {level} {text}")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1))
    sys.exit(1 if any(l == "FAIL" for r in rows for l, _ in r["verdicts"]) else 0)


if __name__ == "__main__":
    main()
