"""Shared builder for Act III's Lakonia maps (design/phase4/SCRIPT.md Part 2).

Gytheion, Route 25 up the Eurotas and Lakonia itself are composed here on
kythera_maps.Map, with pieces placed by key and name from the Lakonia-family
catalogs (lakonia_tiles.py, design/phase4/TILES_{gytheion,eurotas,lakonia}.md)
and the aethos primary. Each map's own module (lakonia_gytheion.py,
lakonia_route25.py, lakonia_town.py) lays its land from a character plan, then
places its structures and events, and calls build(), which writes the layout
and map.json, checks it and renders it into design/phase4/img/maps/.

    /usr/bin/python3 tools/ichor/maps/lakonia_maps.py            # build all three
    /usr/bin/python3 tools/ichor/maps/lakonia_maps.py gytheion   # just one

The plan characters every module shares:
    .  grass            ,  shaded grass        "  ledge grass (under a lip)
    p  worn path        s  sand                ~  sea
    w  river water      r  reeds in the river (tall grass)
    G  tall grass       T  wood (filled by Map.woods)
    M  mountain mass    o  olive (2x2, top-left)   c  cypress (1x2, top)
    other letters are left as grass for the module to place structures on.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kythera_tiles as KT  # noqa: E402
import lakonia_tiles as LT  # noqa: E402

KT.TILESETS.update(LT.TILESETS)

from kythera_maps import A, Map, AETHOS_SOLID, _hash  # noqa: E402,F401

SOLID_AETHOS = AETHOS_SOLID


class LMap(Map):
    """A Map whose secondary is one of the Lakonia family."""

    def __init__(self, name, tileset, plan, fill=A.GRASS):
        rows = [r for r in plan.strip("\n").split("\n")]
        w, h = max(len(r) for r in rows), len(rows)
        super().__init__(name, tileset, w, h, fill=fill)
        self.plan = [r.ljust(w, ".") for r in rows]

    # --- plan --------------------------------------------------------------------------
    def cells(self, chars):
        return {(x, y) for y, r in enumerate(self.plan) for x, c in enumerate(r) if c in chars}

    def at(self, x, y):
        if not self.ok(x, y):
            return None
        return self.plan[y][x]

    def lay_plan(self, salt=0):
        """Lay the ground from the plan (structures come after)."""
        for (x, y) in self.cells(","):
            self.set(x, y, A.SHADE, False)
        for (x, y) in self.cells('"'):
            self.set(x, y, A.GRASS_LEDGE, False)
        for (x, y) in self.cells("s"):
            self.set(x, y, A.SAND, False)
        for (x, y) in self.cells("~"):
            self.set(x, y, A.SEA, False)
        for (x, y) in self.cells("G"):
            self.set(x, y, A.TALL, False)
        self.path(self.cells("p"))
        water = self.cells("wr")
        if water:
            self.soft("river", self.cells("w"), water)
            if self.cells("r"):
                self.soft("reeds", self.cells("r"), self.cells("r"))
        for (x, y) in sorted(self.cells("o")):
            self.olive(x, y)
        for (x, y) in sorted(self.cells("c")):
            self.cypress(x, y)
        m = self.cells("M")
        for (x, y) in m:
            self.piece("taygetos", f"mass_{x % 2}{y % 2}", x, y)

    def soft(self, key, cells, region, edge_in=True):
        """Soft-edged autotile pieces over `cells`, shaped against `region`;
        cells off the map count as in the region when edge_in."""
        region = set(region)

        def inside(x, y):
            if not self.ok(x, y):
                return edge_in
            return (x, y) in region
        names = self.s(key)["names"]
        walk = self.s(key)["walk"][0][0]
        for (x, y) in cells:
            k = self.shape_key(inside, x, y)
            cx, cy = names[k]
            self.set(x, y, self.s(key)["ids"][cy][cx], walk == "X")

    def woods(self, free, salt=0, aethos_only=lambda x, y: False, singles=None, **kw):
        """kythera_maps' wood, with the family's own single shrubs (oleander where
        the tileset has it, else shaded grass) instead of Kythera's myrtle."""
        if singles is None:
            singles = [("oleander", "bush")] if "oleander" in self.cat["structures"] else []
        return super().woods(free, salt=salt, aethos_only=aethos_only, singles=singles, **kw)

    # --- land pieces -------------------------------------------------------------------
    def rock_wall(self, x0, x1, y, faces=1, key="taygetos", ends=True):
        """A south-facing rock wall: lip at row y, `faces` rows of face, the foot."""
        names = self.s(key)["names"]
        for x in range(x0, x1 + 1):
            b = "_b" if x % 2 and "lip_b" in names else ""
            end = ""
            if ends and x == x0 and "lip_L" in names:
                end = "_L"
            elif ends and x == x1 and "lip_R" in names:
                end = "_R"
            self.piece(key, "lip" + (end or b), x, y)
            for f in range(faces):
                self.piece(key, "face" + (end or b), x, y + 1 + f)
            self.piece(key, "foot" + (end or b), x, y + 1 + faces)

    def ledge_run(self, x0, x1, y, kit=A.LEDGE):
        """A dry-stone terrace lip (jump south) from x0 to x1 on row y."""
        for x in range(x0, x1 + 1):
            name = "SL" if x == x0 else ("SR" if x == x1 else "S")
            self.set(x, y, kit[name], False)

    def wall_run(self, x0, x1, y):
        for x in range(x0, x1 + 1):
            self.set(x, y, A.WALL["L"] if x == x0 else (A.WALL["R"] if x == x1 else A.WALL["M"]), True)

    def plane(self, x, y, key="plane"):
        self.put(key, x, y)

    def front(self, key, x, y):
        """A house front from the tileset's fronts (rows of house piece names)."""
        f = self.cat["fronts"][key]
        house = self.s("house")
        for j, row in enumerate(f["rows"]):
            for i, n in enumerate(row):
                cx, cy = house["names"][n]
                self.set(x + i, y + j, house["ids"][cy][cx], house["walk"][cy][cx] == "X")
        return len(f["rows"][0]), len(f["rows"])

    def house(self, rows, x, y):
        """A house built from rows of house piece names (None leaves a cell)."""
        hs = self.s("house")
        for j, row in enumerate(rows):
            for i, n in enumerate(row):
                if n is None:
                    continue
                cx, cy = hs["names"][n]
                self.set(x + i, y + j, hs["ids"][cy][cx], hs["walk"][cy][cx] == "X")

    def aethos_building(self, rows, x, y):
        for j, r in enumerate(rows):
            for i, m in enumerate(r):
                self.set(x + i, y + j, m, m in AETHOS_SOLID)

    def scatter(self, cells, salt, rate, fn):
        for (x, y) in sorted(cells):
            if _hash(x, y, salt) < rate:
                fn(x, y)


def main(which):
    import importlib
    mods = {"gytheion": "lakonia_gytheion", "route25": "lakonia_route25", "lakonia": "lakonia_town"}
    errs = 0
    for k in (which or list(mods)):
        mod = importlib.import_module(mods[k])
        errs += len(mod.build() or [])
    return errs


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
