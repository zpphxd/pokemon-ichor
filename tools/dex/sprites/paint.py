"""Hand-finishing helpers for the dex's battle-sprite art files.

An art file (tools/dex/sprites/art/<name>_<view><phase>.txt) is the --dump
format: two column-header lines, then one line per row, 'yy ' followed by
64 characters, '.' for clear and hex palette indices ('1'-'f') for colors.
Edit them with these helpers from a short Python snippet:

    import sys; sys.path.insert(0, "tools/dex/sprites")
    from paint import paint, retone, shift, clear

    P = "tools/dex/sprites/art/nebrel_front0.txt"
    paint(P, {24: [(18, "1511771554443321")]})   # row 24, starting at x 18
    clear(P, range(22, 34), 12, 34)               # rows 22-33, x 12-34
    retone(P, "2345", range(45, 64), 4, 47, lambda t, v, top: 0.1 + 0.5 * t + 0.4 * v)
    shift("..._front0.txt", "..._front1.txt", (8, 10, 45, 33), dy=-1)

paint: a space in a run leaves that pixel alone.
retone: repaints the pixels of one ramp (dark to light, e.g. "2345") inside a
    region with fn(t, v, top) -> 0..1 (0 lightest); t is the position along
    the row's run, v down the region, top is True right under an outline.
shift: copies a file and moves a rectangle (x0, y0, x1, y1) by dx, dy; rows
    left behind are filled from below (good for raising a head for frame 2).
    Pass mask=lambda x, y: ... to move only some pixels of the box (a head
    without the cape behind it), or only="45ab" to move only those colors.
paint_under: like paint, but only writes into clear pixels, for adding
    parts behind what is already drawn.
"""
from __future__ import annotations


def _read(path):
    lines = open(path).read().rstrip("\n").split("\n")
    head, rows = [], {}
    for i, line in enumerate(lines):
        if not line or line.lstrip().startswith("#"):
            continue
        if len(head) < 2:
            head.append(i)
            continue
        rows[int(line[:3])] = i
    x0 = int(lines[head[0]][4]) * 10 + int(lines[head[1]][4])
    if x0 != 0:
        raise SystemExit(f"{path}: art files start at column 0")
    grid = {y: list(lines[i][4:].ljust(64, ".")[:64]) for y, i in rows.items()}
    return lines, rows, grid


def _write(path, lines, rows, grid):
    for y, i in rows.items():
        lines[i] = lines[i][:4] + "".join(grid[y])
    open(path, "w").write("\n".join(lines) + "\n")


def paint(path, edits):
    """edits: {y: [(x, "chars"), ...]}"""
    lines, rows, grid = _read(path)
    for y, runs in edits.items():
        for x, chars in runs:
            for k, ch in enumerate(chars):
                if ch != " ":
                    grid[y][x + k] = ch
    _write(path, lines, rows, grid)


def clear(path, ys, x0, x1):
    lines, rows, grid = _read(path)
    for y in ys:
        for x in range(x0, x1 + 1):
            grid[y][x] = "."
    _write(path, lines, rows, grid)


def retone(path, ramp, ys, xmin, xmax, fn, skip=lambda x, y: False):
    lines, rows, grid = _read(path)
    ys = list(ys)
    y0, y1 = min(ys), max(ys)
    for y in ys:
        row = grid[y]
        xs = [x for x in range(xmin, xmax + 1) if row[x] in ramp and not skip(x, y)]
        if not xs:
            continue
        a, b = min(xs), max(xs)
        for x in xs:
            t = (x - a) / max(b - a, 1)
            v = (y - y0) / max(y1 - y0, 1)
            top = y > 0 and grid[y - 1][x] == "1"
            k = min(len(ramp) - 1, max(0, int(fn(t, v, top) * len(ramp))))
            row[x] = ramp[len(ramp) - 1 - k]
    _write(path, lines, rows, grid)


def paint_under(path, edits):
    """paint, but only into clear pixels."""
    lines, rows, grid = _read(path)
    for y, runs in edits.items():
        for x, chars in runs:
            for k, ch in enumerate(chars):
                if ch != " " and grid[y][x + k] == ".":
                    grid[y][x + k] = ch
    _write(path, lines, rows, grid)


def shift(src, dst, box, dx=0, dy=-1, mask=None, only=None):
    """Copy src to dst, moving the rectangle box=(x0, y0, x1, y1) by (dx, dy).
    mask(x, y) or only (a string of colors) limits which pixels move; the
    pixels they leave behind become clear unless something lands there."""
    lines, rows, grid = _read(src)
    x0, y0, x1, y1 = box
    old = {y: r[:] for y, r in grid.items()}

    def moves(x, y):
        ch = old[y][x]
        return ch != "." and (mask is None or mask(x, y)) and (only is None or ch in only)
    moving = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if moves(x, y)]
    for x, y in moving:
        grid[y][x] = "."
    for x, y in moving:
        if 0 <= y + dy < 64 and 0 <= x + dx < 64:
            grid[y + dy][x + dx] = old[y][x]
    # fill the strip the move uncovered from the row just outside the box
    if dy < 0 and mask is None and only is None:
        for y in range(y1 + dy + 1, y1 + 1):
            for x in range(x0, x1 + 1):
                if grid[y][x] == "." and old[y1 + 1][x] != ".":
                    grid[y][x] = old[y1 + 1][x]
    lines = [ln.replace(" phase 0", " phase 1") if ln.startswith("#") else ln for ln in lines]
    _write(dst, lines, rows, grid)
