"""A character-grid canvas for drawing tileset pieces in code.

The interior sets (oikia, ergasteria, limen) draw every piece as a grid of
palette characters, '.' for clear. Small pieces are typed out by hand; bigger
ones (a forge hood, a kiln, a mosaic) are easier to build from shapes and then
touch up pixel by pixel. Canvas holds such a grid and draws into it:

    c = Canvas(32, 16)
    c.rect(2, 4, 29, 9, "l")            # inclusive corners
    c.box(2, 4, 29, 9, "l", edge="k")   # filled, outlined
    c.put(5, 5, "h")
    c.paste(["kk", "kk"], 10, 2)
    rows = c.text()                     # for ergasteria_art.grid()

Coordinates are pixels, x right and y down; anything off the canvas is
clipped, so shapes can run past an edge.
"""
import math


class Canvas:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    # -- single pixels and lines ------------------------------------------
    def put(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h and ch is not None:
            self.g[y][x] = ch

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return "."

    def hline(self, x0, x1, y, ch):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.put(x, y, ch)

    def vline(self, x, y0, y1, ch):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.put(x, y, ch)

    def line(self, x0, y0, x1, y1, ch):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), ch)

    # -- areas ------------------------------------------------------------
    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            self.hline(x0, x1, y, ch)

    def box(self, x0, y0, x1, y1, fill, edge="k"):
        self.rect(x0, y0, x1, y1, edge)
        if x1 - x0 >= 2 and y1 - y0 >= 2:
            self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)

    def ellipse(self, cx, cy, rx, ry, ch):
        """Filled; pixel centres within the ellipse centred on (cx, cy)."""
        for y in range(self.h):
            for x in range(self.w):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                    self.put(x, y, ch)

    def fill_where(self, pred, ch):
        for y in range(self.h):
            for x in range(self.w):
                if pred(x, y):
                    self.put(x, y, ch)

    def recolor(self, mapping, x0=0, y0=0, x1=None, y1=None):
        x1 = self.w - 1 if x1 is None else x1
        y1 = self.h - 1 if y1 is None else y1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = self.get(x, y)
                if c in mapping:
                    self.put(x, y, mapping[c])

    def outline(self, ink="k", solid=None):
        """Ink every clear pixel next to a drawn one (4-neighbours)."""
        solid = solid or (lambda c: c != ".")
        hit = []
        for y in range(self.h):
            for x in range(self.w):
                if solid(self.g[y][x]):
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < self.w and 0 <= y + dy < self.h and solid(self.g[y + dy][x + dx]):
                        hit.append((x, y))
                        break
        for x, y in hit:
            self.g[y][x] = ink

    # -- composition ------------------------------------------------------
    def paste(self, rows, x, y, clear="."):
        if isinstance(rows, str):
            rows = [r for r in rows.strip("\n").split("\n")]
        for j, line in enumerate(rows):
            for i, ch in enumerate(line):
                if ch not in (clear, " "):
                    self.put(x + i, y + j, ch)

    def mirror_x(self):
        """Copy the left half onto the right, mirrored."""
        for y in range(self.h):
            for x in range(self.w // 2):
                self.g[y][self.w - 1 - x] = self.g[y][x]

    def flipped(self):
        c = Canvas(self.w, self.h)
        c.g = [row[::-1] for row in self.g]
        return c

    def text(self):
        return "\n".join("".join(r) for r in self.g)


def dist(x0, y0, x1, y1):
    return math.hypot(x1 - x0, y1 - y0)
