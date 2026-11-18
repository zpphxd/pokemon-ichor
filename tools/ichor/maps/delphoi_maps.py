#!/usr/bin/env python3
"""Delphoi's chapter maps (design/phase4/SCRIPT.md III-6A to III-8, Part 2):
Route 28's Sacred Olives and Kastalian Gorge, and Delphoi.

Built on kythera_maps.Map (the same checks, renders and event writing) with
the delphoi and parnassos catalogs (tools/ichor/maps/catalogs/*.json, written
by tools/ichor/art/delphoi_build.py). Each map is an ASCII ground plan plus
structures placed by key and name, so a critique pass edits a plan, not ids.
Renders go to design/phase4/img/maps/.

  /usr/bin/python3 tools/ichor/maps/delphoi_maps.py [olives] [gorge] [delphoi]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kythera_maps as KM  # noqa: E402
import kythera_tiles as KT  # noqa: E402
from kythera_maps import A, Map, _hash  # noqa: E402

for _name in ("delphoi", "parnassos", "temple_apollo"):
    KT.TILESETS[_name] = json.loads((HERE / "catalogs" / f"{_name}.json").read_text())
    for _s in KT.TILESETS[_name]["structures"].values():
        _s["names"] = {k: tuple(v) for k, v in _s["names"].items()}

POND = 0x0A1          # aethos still water (MB_POND_WATER, surfable)
SURFB = KM.SURF


class DMap(Map):
    """kythera_maps.Map with the Parnassos painters."""

    def plan(self, rows):
        assert len(rows) == self.h, (len(rows), self.h)
        for y, r in enumerate(rows):
            assert len(r) == self.w, (y, len(r), r)
        self.rows = rows
        return {ch: {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == ch}
                for ch in set("".join(rows))}

    def pond(self, cells, solid=False):
        """Still water with aethos's pond rim: dark-blue lips where it meets the
        land, plain water inside, foam along its foot (aethos 0x0B0-0x0C2)."""
        cells = set(cells)
        kit = {"TL": 0x0B0, "T": 0x0B1, "TR": 0x0B2, "L": 0x0B8, "C": POND, "R": 0x0BA,
               "BL": 0x0C0, "B": 0x0C1, "BR": 0x0C2}
        for (x, y) in cells:
            n = (x, y - 1) in cells or not self.ok(x, y - 1)
            s_ = (x, y + 1) in cells or not self.ok(x, y + 1)
            w = (x - 1, y) in cells or not self.ok(x - 1, y)
            e = (x + 1, y) in cells or not self.ok(x + 1, y)
            v = "" if (n and s_) else ("T" if not n else "B")
            h = "" if (w and e) else ("L" if not w else "R")
            if v and h and not (n or s_):
                v = "T"
            self.set(x, y, kit[(v + h) or "C"], solid)

    def ledges(self, cells):
        """aethos's dry-stone terrace lips (jump south), ends rounded off."""
        cells = set(cells)
        for (x, y) in cells:
            w, e = (x - 1, y) in cells, (x + 1, y) in cells
            self.set(x, y, A.LEDGE["SL"] if not w else A.LEDGE["SR"] if not e else A.LEDGE["S"], False)

    def break_runs(self, keep=(), longest=9, props=None, allow=None):
        """MAP_DESIGN/STYLE §4.2: no straight edge longer than ~6-10 cells. Walk
        every run of open cells along a blocked line, and every `longest` cells
        stand a prop in it (a bush, a boulder, a stele): only where the cell
        behind it, away from the edge, stays open, and never on a cell in
        `keep` (roads, people, triggers, warps), so no way is ever shut."""
        keep = set(keep) | {(o["x"], o["y"]) for o in self.objects} | {(w["x"], w["y"]) for w in self.warps} \
            | {(t["x"], t["y"]) for t in self.coords} | {(b["x"], b["y"]) for b in self.bgs}
        props = props or [("bush", "mastic"), ("bush", "laurel")]

        def open_(x, y):
            b = self.behavior(int(self.mid[y, x])) if self.ok(x, y) else ""
            return self.ok(x, y) and not self.solid[y, x] and b not in SURFB and not b.startswith("MB_JUMP")

        def blocked(x, y):
            return self.ok(x, y) and not open_(x, y)
        placed = 0
        for horiz in (True, False):
            for d in (-1, 1):
                outer = self.h if horiz else self.w
                inner = self.w if horiz else self.h
                for a in range(outer):
                    run = 0
                    for b in range(inner):
                        x, y = (b, a) if horiz else (a, b)
                        ex, ey = (x, y + d) if horiz else (x + d, y)
                        bx, by = (x, y - d) if horiz else (x - d, y)
                        if open_(x, y) and blocked(ex, ey):
                            run += 1
                            if run > longest and (x, y) not in keep and open_(bx, by) \
                                    and int(self.mid[y, x]) in (allow or (A.GRASS, A.TALL, A.SHADE)) \
                                    and not self.in_seam(x, y):
                                k, n = props[(x * 3 + y) % len(props)]
                                if k is None:
                                    self.set(x, y, n, True)
                                else:
                                    self.piece(k, n, x, y, solid=True)
                                placed += 1
                                run = 0
                        else:
                            run = 0
        return placed

    def in_seam(self, x, y):
        for side, depth in self.seams:
            if ((side == "up" and y < depth) or (side == "down" and y >= self.h - depth)
                    or (side == "left" and x < depth) or (side == "right" and x >= self.w - depth)):
                return True
        return False

    def cliff(self, cells, edge_in=True):
        """The Phaedriades kit over a set of cells: crest, faces and foot by
        what's above and below, west/east edges by what's beside; off the map
        counts as cliff, so cliffs run on past the edge."""
        cells = set(cells)

        def inn(x, y):
            return (x, y) in cells or (edge_in and not self.ok(x, y))
        for (x, y) in cells:
            up, dn = inn(x, y - 1), inn(x, y + 1)
            w, e = inn(x - 1, y), inn(x + 1, y)
            row = "crest" if not up else "foot" if not dn else ("face" if y % 2 == 0 else "faceb")
            col = "_W" if not w else "_E" if not e else ("" if x % 2 == 0 else "2")
            name = row + col
            if name not in self.s("phaedriades")["names"]:
                name = row + ("" if col in ("", "2") else col)
            self.piece("phaedriades", name, x, y, solid=True)

    def ledge(self, cells, key="pezoula"):
        cells = set(cells)
        for (x, y) in cells:
            w, e = (x - 1, y) in cells, (x + 1, y) in cells
            name = "W" if not w else "E" if not e else ("M" if x % 3 else "M2")
            self.piece(key, name, x, y, solid=False)

    def grove(self, cells, salt=0, open_=False, leftover=A.TALL, cypress=40):
        """The god's olives: 2x2 olives placed top-down in a shuffled order so
        their rows never line up (nobody has replanted them in a thousand years),
        a cypress now and then. open_: an orchard you can walk through, the gaps
        tall grass; otherwise a mass you walk round, its gaps deep shade."""
        free = set(cells)
        if open_:
            # top-down in bands of 3 rows, shuffled within each band, so crowns
            # stack but no two rows line up
            order = sorted(free, key=lambda c: (c[1] // 3, _hash(c[0], c[1], salt + 21)))
        else:
            # a canopy wall: rows two deep, each row shifted by a cell or not,
            # trees packed side by side, so the mass reads solid
            order = sorted(free, key=lambda c: (c[1], (c[0] + _hash(0, c[1] // 2, salt + 23) % 2) % 2,
                                                c[0]))
        for (x, y) in order:
            quad = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if not all(c in free for c in quad):
                continue
            r = _hash(x, y, salt)
            if open_ and r < 520:
                continue
            if not open_ and r < 60:
                continue
            k = _hash(x, y, salt + 3)
            if k < cypress and (x, y + 1) in free:
                self.cypress(x, y)
                free -= {(x, y), (x, y + 1)}
                continue
            if not open_ and k < cypress + 130 and "laurel" in self.cat["structures"] \
                    and not any(self.in_seam(*c) for c in quad):
                self.put("laurel" if k % 2 else "laurel_b", x, y)
            elif not open_ and k < cypress + 200:
                self.pine(x, y)
            else:
                self.olive(x, y)
            free -= set(quad)
        for (x, y) in sorted(free, key=lambda c: (c[1], c[0])):
            if open_:
                self.set(x, y, leftover if _hash(x, y, salt + 9) < 800 else A.GRASS, False)
            elif (x, y + 1) in free and _hash(x, y, salt + 7) < 700:
                self.cypress(x, y)
                free.discard((x, y + 1))
            elif self.in_seam(x, y) or "bush" not in self.cat["structures"]:
                self.set(x, y, A.BOULDER_GRASS if _hash(x, y, salt + 8) < 300 else A.SHADE, True)
            else:
                self.piece("bush", "mastic" if _hash(x, y, salt + 8) % 3 else "laurel", x, y, solid=True)
        if not open_:
            for (x, y) in cells:
                self.solid[y, x] = True

    def scatter(self, cells, key, names, rate=120, salt=0):
        """Ground variety on plain grass: about rate/1000 of the cells take a
        variant, never two side by side."""
        took = set()
        for (x, y) in sorted(cells):
            if int(self.mid[y, x]) != A.GRASS or self.solid[y, x]:
                continue
            if any((x + dx, y + dy) in took for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                continue
            if _hash(x, y, salt + 11) < rate:
                n = names[_hash(x, y, salt + 13) % len(names)]
                self.piece(key, n, x, y, solid=False)
                took.add((x, y))


def trainer(m, gfx, x, y, script, face, sight, flag="0", local_id=None):
    move = {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP",
            "left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT"}[face]
    return m.obj(gfx, x, y, script, move=move, trainer=True, sight=sight, flag=flag, local_id=local_id)


def npc(m, gfx, x, y, script, face="down", flag="0", local_id=None, wander=False):
    move = ("MOVEMENT_TYPE_WANDER_AROUND" if wander else
            {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP",
             "left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT"}[face])
    e = m.obj(gfx, x, y, script, move=move, flag=flag, local_id=local_id)
    if wander:
        e["movement_range_x"], e["movement_range_y"] = 1, 1
    return e


class Plan:
    """A ground plan built from rectangles, printable for the critique notes.
    Codes: T a mass of trees (walk round), o an orchard (walk through: olives,
    tall grass between), . grass, G tall grass, p road, # cliff, = terrace
    ledge, w dry-stone wall, s dry stream bed, ~ water, ' ' kept for a structure."""

    def __init__(self, w, h, fill="T"):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def box(self, x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.g[y][x] = ch

    def cells(self, pts, ch):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.g[y][x] = ch

    def road(self, pts, width=2, ch="p", salt=0, bulge=True):
        """A road through waypoints, width cells wide (the extra cells fall to
        the right of travel, then below), widening by a cell at every bend and
        now and then along a straight, the way a worn road does."""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx = (x1 > x0) - (x1 < x0)
            dy = (y1 > y0) - (y1 < y0)
            x, y = x0, y0
            while True:
                for k in range(width):
                    self.cells([(x + (k if dy else 0), y + (k if dx else 0))], ch)
                if bulge and _hash(x, y, salt + 31) < 140:
                    side = width if _hash(x, y, salt + 33) % 2 else -1
                    self.cells([(x + (side if dy else 0), y + (side if dx else 0))], ch)
                if (x, y) == (x1, y1):
                    break
                x, y = x + dx, y + dy
            # the bend: a cell wider
            for ox in range(-1, width + 1):
                for oy in range(-1, width + 1):
                    if abs(ox) + abs(oy) <= width and _hash(x1 + ox, y1 + oy, salt + 35) < 600:
                        self.cells([(x1 + ox, y1 + oy)], ch)

    def rows(self):
        return ["".join(r) for r in self.g]


def paint(m, rows, salt=0):
    """Lay a plan's ground: grass, tall grass, road, groves, cliffs, ledges,
    walls, the dry stream bed and water. Returns get(ch) for its regions."""
    regions = m.plan(rows)

    def get(ch):
        return regions.get(ch, set())
    for (x, y) in get(".") | get(" "):
        m.set(x, y, A.GRASS, False)
    for (x, y) in get("G"):
        m.set(x, y, A.TALL, False)
    m.pond(get("~"))
    m.ledges(get("J"))
    m.path(get("p"))
    m.grove(get("T"), salt=salt + 1)
    m.grove(get("o"), salt=salt + 2, open_=True)
    m.cliff(get("#"))
    m.ledge(get("="))
    for (x, y) in get("w"):
        w, e = (x - 1, y) in get("w"), (x + 1, y) in get("w")
        m.set(x, y, A.WALL["L"] if not w else A.WALL["R"] if not e else A.WALL["M"], True)
    for (x, y) in get("s"):
        m.piece("ground", "stones", x, y, solid=False)
    return get


def run(build, stem_views):
    m, rows = build()
    print("\n".join(rows))
    return m.build(m.name.lower(), **stem_views)

