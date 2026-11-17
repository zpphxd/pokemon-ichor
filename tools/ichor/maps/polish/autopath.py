"""Autotile a dirt path from a set of cells, learning the edge pieces from maps.

learn(ids, layouts) reads every cell whose metatile is in `ids` in the given
layouts and records which piece is used for each neighbour mask (N, E, S, W
are path, plus the four diagonals when all sides are path). lay(m, cells,
table) then draws the path.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapedit import Layout  # noqa: E402


def mask(is_path, x, y):
    n, e, s, w = is_path(x, y - 1), is_path(x + 1, y), is_path(x, y + 1), is_path(x - 1, y)
    k = (n, e, s, w)
    diag = ()
    if all(k):
        diag = (is_path(x + 1, y - 1), is_path(x + 1, y + 1), is_path(x - 1, y + 1), is_path(x - 1, y - 1))
    return k + diag


def learn(ids, names):
    seen = defaultdict(Counter)
    for name in names:
        m = Layout(name)
        inmap = lambda x, y: 0 <= x < m.w and 0 <= y < m.h  # noqa: E731
        is_path = lambda x, y: (not inmap(x, y)) or m.id(x, y) in ids  # noqa: E731
        for y in range(m.h):
            for x in range(m.w):
                if m.id(x, y) in ids:
                    seen[mask(is_path, x, y)][m.id(x, y)] += 1
    return {k: c.most_common(1)[0][0] for k, c in seen.items()}


def lay(m, cells, table, fallback):
    cells = set(cells)
    inmap = lambda x, y: 0 <= x < m.w and 0 <= y < m.h  # noqa: E731
    is_path = lambda x, y: (not inmap(x, y)) or (x, y) in cells  # noqa: E731
    missing = set()
    for x, y in cells:
        k = mask(is_path, x, y)
        mid = table.get(k)
        if mid is None and len(k) == 8:
            mid = table.get(k[:4] + (True, True, True, True))
        if mid is None:
            missing.add(k)
            mid = fallback
        m.put(x, y, mid, solid=False)
    return missing
