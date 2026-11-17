#!/usr/bin/env python3
"""Check that every bit of open water a player can stand beside can be fished.

  tools/ichor/fishing_audit.py                 every Ichor map; exit 1 on a problem
  tools/ichor/fishing_audit.py Route8 Kirrha   maps, or name prefixes
  tools/ichor/fishing_audit.py -v              also list the maps that pass

A rod works on the cell the player faces only when the engine's checks pass
(src/field_player_avatar.c, IsPlayerFacingSurfableFishableWater):
  - the cell's behavior is MetatileBehavior_IsSurfableFishableWater's (pond,
    ocean, deep, interior deep or Sootopolis water, or a current),
  - it has no collision bit,
  - its elevation differs from the player's (so it reads as an elevation
    mismatch, not open ground), and isn't 0 or 15,
  - the player stands at the default elevation, 3.
The usual way to get all of that is water at elevation 1 with no collision,
beside land at elevation 3. Then the rod looks for the map's fishing table; a
map with none answers every cast with "Not even a nibble".

For each map this walks the player from every entry (mapdata.Walker, on foot,
with relics) and looks at every cell they can face. A cell counts as water if
its behavior is surfable water, or if it's drawn exactly like a fishable water
metatile of the map's tilesets (water painted with the wrong behavior), or if
it's a puddle or shallow-water metatile with collision (a puddle used as deep
water). It fails when:
  CAST   the player can face that water on foot but the rod can't be cast at it.
         Water at the player's own elevation with no collision is wadeable
         shallows, which is fine: they step in and cast from there.
  TABLE  the map has fishable water beside reachable land but no fishing table.

Water a player should not fish (a fountain, a basin in a building, a painted
backdrop) belongs in DECORATIVE below, with the reason. Python 3 stdlib, numpy
and Pillow (macOS's /usr/bin/python3 has both).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import DIRS, NEVER_STAND, UPSTREAM_PREFIXES, WATER, Repo, Walker, entries  # noqa: E402

# MetatileBehavior_IsSurfableFishableWater (src/metatile_behavior.c).
FISHABLE = {"MB_POND_WATER", "MB_OCEAN_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER",
            "MB_SOOTOPOLIS_DEEP_WATER", "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT",
            "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT"}
# Shallow-looking water a player may walk through; with collision it stands for deep water.
SHALLOW = {"MB_PUDDLE", "MB_SHALLOW_WATER"}
NOT_FISHABLE_WATER = {"MB_WATERFALL"}  # the rod refuses a waterfall (item_use.c, CanFish)
PLAYER_ELEVATION = 3  # ELEVATION_DEFAULT: IsPlayerFacingSurfableFishableWater needs it

# map -> (metatile ids, or None for all of the map's water; why the player isn't meant to fish it)
DECORATIVE = {
    "StyxFalls": (None, "nothing lives in the Styx: the pool under the fall is solid by design "
                        "(af9b59a670); Stygiad waits for the post-game Katabasis"),
    "Olympus_SeatOfPoseidon": (None, "the Pantheon seat's ornamental basin around its model trireme"),
    "Nemea": ({0x0B0, 0x0B1, 0x0B2, 0x0B8, 0x0B9, 0x0BA, 0x0C0, 0x0C1, 0x0C2},
              "the Langia spring's stone basin, a fountain (a Horn of Achelous hook); the river pool is fished"),
    "AktiTown": ({0x2A7},"a water cell inside the moored boat's stamp; the quay faces open sea all round it"),
}


class Looks:
    """Which metatiles of a tileset pair are drawn exactly like a fishable water metatile."""

    def __init__(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import render_map as rm
        rm.read_fieldmap_constants()
        self.rm, self.syms, self.cache = rm, rm.scan_tileset_symbols(), {}

    def water_like(self, m, prim, sec):
        key = (prim, sec)
        if key not in self.cache:
            rm = self.rm
            r = rm.Renderer(rm.Tileset(rm.resolve_tileset(prim, self.syms)),
                            rm.Tileset(rm.resolve_tileset(sec, self.syms)))
            ids = list(range(len(m.prim))) + [512 + i for i in range(len(m.sec))]
            images = {mid: r.metatile(mid)[0].tobytes() for mid in ids}
            water = {img for mid, img in images.items() if m.behavior(mid) in FISHABLE}
            self.cache[key] = {mid for mid, img in images.items() if img in water}
        return self.cache[key]


def is_water(m, mid, col, looks):
    b = m.behavior(mid)
    if b in NOT_FISHABLE_WATER:
        return False
    return b in WATER or mid in looks or (b in SHALLOW and col)


def can_cast(m, cell, elevation):
    mid, col, el = cell
    return (m.behavior(mid) in FISHABLE and not col and el not in (0, 15)
            and el != elevation and elevation == PLAYER_ELEVATION)


def wadeable(m, cell, elevation):
    mid, col, el = cell
    return not col and (el in (0, 15) or el == elevation) and m.behavior(mid) not in NEVER_STAND


def audit_map(repo, name, looks_cache):
    m = repo.map(name)
    lay = repo.layouts[m.json["layout"]]
    looks = looks_cache.water_like(m, lay["primary_tileset"], lay["secondary_tileset"])
    walker = Walker(m, surf=False, relics=True)
    starts = walker.starts([c for _, cells in entries(m) for c in cells])
    if not starts:  # nothing leads in (a cutscene stage): every standable cell counts
        starts = walker.starts([(x, y) for y in range(m.h) for x in range(m.w)])
    states = walker.reach(starts)
    ids, _ = DECORATIVE.get(name, (set(), ""))
    bad, fishable = {}, 0
    for x, y, e in states:
        if m.behavior_at(x, y) in WATER:  # wading in shallows: cast from the land around them
            continue
        elevation = PLAYER_ELEVATION if e in (0, 15) else e
        for dx, dy, d in DIRS:
            c = m.cell(x + dx, y + dy)
            if c is None or not is_water(m, c[0], c[1], looks):
                continue
            if can_cast(m, c, elevation):
                fishable += 1
            elif ids is None or c[0] in ids:
                continue
            elif not wadeable(m, c, elevation):
                bad.setdefault((x + dx, y + dy), (x, y, d, c))
    problems = []
    for (wx, wy), (x, y, d, (mid, col, el)) in sorted(bad.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        problems.append(f"CAST   ({wx},{wy}) metatile 0x{mid:03X} {m.behavior(mid)} collision {col} "
                        f"elevation {el}: no cast from ({x},{y}) facing {d}")
    if fishable and not any("fishing_mons" in t for t in repo.wild().get(m.json["id"], {}).values()):
        problems.append(f"TABLE  {fishable} shore cells face fishable water, but the map has no fishing table")
    return problems, fishable


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("maps", nargs="*", help="map names or prefixes (default: every Ichor map)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    repo = Repo()
    names = [n for n in repo.names if not n.startswith(UPSTREAM_PREFIXES)]
    if args.maps:
        names = [n for n in names if any(n == a or n.startswith(a) for a in args.maps)]
    looks, failed = Looks(), 0
    for name in names:
        problems, fishable = audit_map(repo, name, looks)
        if problems:
            failed += 1
            print(f"{name}: {len(problems)} problem(s)")
            for p in problems[:12]:
                print("  " + p)
            if len(problems) > 12:
                print(f"  ... and {len(problems) - 12} more")
        elif args.verbose and fishable:
            print(f"{name}: ok ({fishable} shore cells face fishable water)")
    print(f"fishing_audit: {len(names)} maps, {failed} with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
