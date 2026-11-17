"""Paint a region of a layout from an ASCII sketch, with Aethos trees.

Trees come out as interlocking Gen 3 masses: an olive or pine 'O'/'P' run is
read down each even column pair, so one sketch letter block becomes stacked,
overlapping crowns (olive tip 1CE/1CF, crown 1D4/1D5, trunk-under-crown
1DC/1DD, last trunk 1E4/1E5). Cypress 'c' runs are read down single columns.

Single-cell legend entries are (metatile, solid); '=' keeps the old cell.
"""
import random

# Aethos olive / stone pine / cypress
OL_TIP, OL_CROWN, OL_MID, OL_TRUNK = (0x1CE, 0x1CF), (0x1D4, 0x1D5), (0x1DC, 0x1DD), (0x1E4, 0x1E5)
PI_CROWN, PI_TRUNK = (0x01E, 0x01F), (0x026, 0x027)
CY_TOP, CY_BOT = 0x00E, 0x016

BASE = {
    ".": (0x001, False), ",": (0x001, True),
    ":": ("var", False), ";": ("var", True),
    "f": (0x004, False), "F": (0x004, True),
    "r": (0x0E0, True), "k": (0x0D7, True),
    "s": (0x003, True), "h": (0x01B, True), "n": (0x1C5, True),
}
GRASS_VARIANTS = (0x0D3, 0x0D4, 0x002)


def paint(m, x0, y0, rows, legend=None, parity=0, seed=1, ground=0x001):
    """Paint `rows` (list of equal-length strings) with its top-left at (x0, y0).

    parity: x (absolute) of the left column of a tree pair, mod 2.
    """
    rnd = random.Random(seed)
    lg = dict(BASE)
    lg.update(legend or {})
    h, w = len(rows), len(rows[0])
    assert all(len(r) == w for r in rows), [len(r) for r in rows]
    ch = lambda i, j: rows[j][i] if 0 <= i < w and 0 <= j < h else None  # noqa: E731

    # singles and ground first
    for j in range(h):
        for i in range(w):
            c = rows[j][i]
            x, y = x0 + i, y0 + j
            if c == "=":
                continue
            if c in "OPc":
                m.put(x, y, ground, solid=True)
                continue
            mid, solid = lg[c]
            if mid == "var":
                mid = rnd.choice(GRASS_VARIANTS)
            if callable(mid):
                mid = mid(x, y)
            m.put(x, y, mid, solid=solid)

    # tree pairs
    for i in range(w - 1):
        if (x0 + i) % 2 != parity:
            continue
        for letter in "OP":
            j = 0
            while j < h:
                if ch(i, j) == letter and ch(i + 1, j) == letter:
                    k = j
                    while ch(i, k + 1) == letter and ch(i + 1, k + 1) == letter:
                        k += 1
                    _column(m, x0 + i, y0 + j, y0 + k, letter, ground)
                    j = k + 1
                else:
                    j += 1
    # cypress columns
    for i in range(w):
        j = 0
        while j < h:
            if ch(i, j) == "c":
                k = j
                while ch(i, k + 1) == "c":
                    k += 1
                n = k - j + 1
                for t in range(n - n % 2):
                    m.put(x0 + i, y0 + j + t, CY_TOP if t % 2 == 0 else CY_BOT, solid=True)
                j = k + 1
            else:
                j += 1


def tufts(m, box, base=0x001, variants=GRASS_VARIANTS, share=0.12, seed=1, avoid=()):
    """Turn ~share of the plain `base` cells in box=(x0, y0, x1, y1) into
    clustered ground variants (2-4 cells a clump), keeping solidity."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    cells = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
             if m.id(x, y) == base and (x, y) not in avoid]
    want = int(len(cells) * share)
    done = 0
    while done < want and cells:
        x, y = rnd.choice(cells)
        v = rnd.choice(variants)
        for dx, dy in [(0, 0)] + rnd.sample([(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1)], rnd.randint(1, 3)):
            if (x + dx, y + dy) in cells and m.id(x + dx, y + dy) == base:
                m.put(x + dx, y + dy, v)
                done += 1


def _column(m, x, ya, yb, letter, ground):
    n = yb - ya + 1
    rows = []
    if letter == "O":
        if ya == 0:
            # the map's top edge: the canopy carries on off the map
            if n % 2:
                rows.append(OL_MID)
        else:
            rows.append(OL_TIP)
        trees = (n - len(rows)) // 2
        for t in range(trees):
            rows.append(OL_CROWN)
            rows.append(OL_MID if t < trees - 1 else OL_TRUNK)
        if len(rows) < n and yb == m.h - 1:
            # the map's bottom edge: end on a crown whose trunk is off the map
            if rows and rows[-1] == OL_TRUNK:
                rows[-1] = OL_MID
            rows.append(OL_CROWN)
    else:
        for t in range(n // 2):
            rows += [PI_CROWN, PI_TRUNK]
    for t, pair in enumerate(rows):
        if pair is None:
            continue
        m.put(x, ya + t, pair[0], solid=True)
        m.put(x + 1, ya + t, pair[1], solid=True)
    for t in range(len(rows), n):        # leftover row: rough ground under the canopy
        m.put(x, ya + t, ground, solid=True)
        m.put(x + 1, ya + t, ground, solid=True)
