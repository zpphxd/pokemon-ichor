#!/usr/bin/env python3
"""Small helpers for hand-editing a layout's map.bin from Python.

A cell is a u16: metatile id in bits 0-9, collision in bits 10-11, elevation
in bits 12-15 (see tools/ichor/mapdata.py).

  from mapedit import Layout
  m = Layout("ThyrsaCity")
  m.dump(0, 0, 20, 12)            # print ids (* = solid)
  m.put(4, 5, 0x1CE, solid=True)  # elevation kept from the old cell
  m.stamp(10, 10, m.grab(2, 2, 3, 3))
  m.save()
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class Layout:
    def __init__(self, name, layout_id=None):
        lays = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
        lay = next(l for l in lays if l.get("id") == layout_id or l.get("name") == name + "_Layout"
                   or l.get("blockdata_filepath", "").endswith(f"/{name}/map.bin"))
        self.w, self.h = lay["width"], lay["height"]
        self.path = ROOT / lay["blockdata_filepath"]
        data = self.path.read_bytes()
        self.cells = [int.from_bytes(data[i:i + 2], "little") for i in range(0, len(data), 2)]

    def raw(self, x, y):
        return self.cells[y * self.w + x]

    def id(self, x, y):
        return self.raw(x, y) & 0x3FF

    def solid(self, x, y):
        return bool(self.raw(x, y) & 0xC00)

    def elev(self, x, y):
        return self.raw(x, y) >> 12

    def put(self, x, y, mid, solid=None, elev=None):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        old = self.raw(x, y)
        s = (old >> 10) & 3 if solid is None else (1 if solid else 0)
        e = old >> 12 if elev is None else elev
        self.cells[y * self.w + x] = (e << 12) | (s << 10) | (mid & 0x3FF)

    def setraw(self, x, y, raw):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.cells[y * self.w + x] = raw

    def grab(self, x, y, w, h):
        return [[self.raw(x + i, y + j) for i in range(w)] for j in range(h)]

    def stamp(self, x, y, block, skip=None):
        """Paste raw cells; cells whose id equals `skip` are left alone."""
        for j, row in enumerate(block):
            for i, raw in enumerate(row):
                if skip is not None and (raw & 0x3FF) == skip:
                    continue
                self.setraw(x + i, y + j, raw)

    def fill(self, x0, y0, x1, y1, mid, solid=None, elev=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, mid, solid, elev)

    def dump(self, x0=0, y0=0, x1=None, y1=None, out=sys.stdout):
        x1 = self.w - 1 if x1 is None else x1
        y1 = self.h - 1 if y1 is None else y1
        out.write("     " + "".join(f"{x:>6}" for x in range(x0, x1 + 1)) + "\n")
        for y in range(y0, y1 + 1):
            row = []
            for x in range(x0, x1 + 1):
                r = self.raw(x, y)
                e = r >> 12
                row.append(f"{r & 0x3FF:03X}{'*' if r & 0xC00 else ' '}{e:X}".rjust(6))
            out.write(f"{y:>4} " + "".join(row) + "\n")

    def ascii(self, legend=None, out=sys.stdout):
        """One char per cell: legend[id] if given, else '#' solid / '.' open."""
        legend = legend or {}
        out.write("   " + "".join(str(x // 10) for x in range(self.w)) + "\n")
        out.write("   " + "".join(str(x % 10) for x in range(self.w)) + "\n")
        for y in range(self.h):
            s = "".join(legend.get(self.id(x, y)) or ("#" if self.solid(x, y) else ".")
                        for x in range(self.w))
            out.write(f"{y:2} {s}\n")

    def save(self):
        self.path.write_bytes(b"".join(c.to_bytes(2, "little") for c in self.cells))


TREES = {0x1CE: "o", 0x1CF: "o", 0x1D4: "O", 0x1D5: "O", 0x1E4: "t", 0x1E5: "t", 0x1DC: "T",
         0x1DD: "T", 0x00E: "c", 0x016: "C", 0x01E: "p", 0x01F: "p", 0x026: "P", 0x027: "P",
         0x0E0: "r", 0x004: "f"}

if __name__ == "__main__":
    m = Layout(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "ascii":
        m.ascii(TREES)
    else:
        a = [int(v) for v in sys.argv[2:6]] if len(sys.argv) >= 6 else []
        m.dump(*a)
