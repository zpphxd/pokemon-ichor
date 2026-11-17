"""Interlocking woods for aethos maps (STYLE.md §4.2 "Forests", §4.3 canopy walls).

An olive is 2x2 (crown 1D4/1D5 over trunk 1E4/1E5). Olives stacked one row
apart overlap: the lower tree's crown hides the upper tree's trunk (1D6/1D7),
so a column of olives reads as one canopy wall with trunks only along its foot.
`interlock` fills a set of cells that way, column pair by column pair, and
bites a ragged foot and crown out of each pair where the wood faces open
ground, with a cypress or a stone pine standing in front in some of the bites.

The map builders (kythera_outdoor.py, kythera_maps.py) call it from their
woods(); it touches the grid only through the callbacks it is given.
"""
from __future__ import annotations

CROWN = (0x1D4, 0x1D5)          # crown row: canopy over open ground
CROWN_OVER = (0x1D6, 0x1D7)     # canopy over the trunk of the tree behind
TRUNK = (0x1E4, 0x1E5)          # foot row: trunk on grass
TIP_GRASS, TIP_TALL, TIP_SEA = (0x1CE, 0x1CF), (0x1C6, 0x1C7), (0x1F6, 0x1F7)
CYPRESS = ((0x00E, 0x016), (0x00F, 0x017))   # two silhouettes: top, bottom
PINE = ((0x01E, 0x01F), (0x026, 0x027))
GRASS, GRASS2, SHADE, TALL, FLOWERS, SEA = 0x001, 0x002, 0x01C, 0x00D, 0x004, 0x170


def interlock(cells, get, setc, is_open, rnd, single=None, salt=0):
    """Fill `cells` with an interlocking olive mass.

    get(x, y) -> metatile id or None off the map; setc(x, y, mid, solid);
    is_open(x, y) -> True for walkable ground outside `cells`; rnd(x, y, salt)
    -> a stable number in [0, 1); single(x, y) dresses a lone leftover cell
    (a myrtle, a briar) and returns True, else the cell becomes closed shade.
    Returns the cells left open (bitten out of the edge)."""
    cells = set(cells)
    if not cells:
        return set()
    # each separate wood pairs its columns from its own west edge, so an odd
    # column falls at its far side rather than down its middle
    comps, seen = [], set()
    for c in sorted(cells):
        if c in seen:
            continue
        comp, todo = set(), [c]
        seen.add(c)
        while todo:
            x, y = todo.pop()
            comp.add((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in cells and n not in seen:
                    seen.add(n)
                    todo.append(n)
        comps.append(comp)
    if len(comps) > 1:
        opened = set()
        for comp in comps:
            opened |= interlock(comp, get, setc, lambda x, y: is_open(x, y) and (x, y) not in cells,
                                rnd, single=single, salt=salt)
        return opened
    x0 = min(x for x, _ in cells)
    done, opened = set(), set()

    def bite(x, y, k, side):
        # how many rows to bite from a pair's foot ("s") or crown ("n")
        r = rnd(x, y, salt + (17 if side == "s" else 29))
        if side == "s":
            return 0 if r < 0.42 else 1 if r < 0.74 else 2 if k >= 2 else 1
        return 0 if r < 0.62 else 1

    for x in range(x0, max(cx for cx, _ in cells) + 1, 2):
        col = sorted(y for (cx, y) in cells if cx == x and (x + 1, y) in cells)
        runs, run = [], []
        for y in col:
            if run and y != run[-1] + 1:
                runs.append(run)
                run = []
            run.append(y)
        if run:
            runs.append(run)
        for run in runs:
            a, b = run[0], run[-1]
            # never bite at the map's side edges: a cell opened there would face a
            # neighbour's solid seam (MAP_DESIGN §5)
            on_side = get(x - 1, a) is None or get(x + 2, a) is None
            foot_open = is_open(x, b + 1) and is_open(x + 1, b + 1) and not on_side
            crown_open = is_open(x, a - 1) and is_open(x + 1, a - 1) and not on_side
            bs = bite(x, b, len(run) - 2, "s") if foot_open else 0
            bn = bite(x, a, len(run) - 2, "n") if crown_open else 0
            while (b - bs) - (a + bn) + 1 < 2 and (bs or bn):
                if bs:
                    bs -= 1
                else:
                    bn -= 1
            top, bot = a + bn, b - bs
            if bot - top + 1 >= 2:
                for y in range(top, bot + 1):
                    pair = CROWN if y == top else TRUNK if y == bot else CROWN_OVER
                    setc(x, y, pair[0], True)
                    setc(x + 1, y, pair[1], True)
                    done |= {(x, y), (x + 1, y)}
            else:
                bot = top - 1
            # the bitten foot: open grass, sometimes a tree standing in front
            for y in range(bot + 1, b + 1):
                for dx in (0, 1):
                    setc(x + dx, y, GRASS, False)
                    done.add((x + dx, y))
                    opened.add((x + dx, y))
            if bs == 2:
                r = rnd(x, b, salt + 41)
                if r < 0.22:
                    for j, row in enumerate(PINE):
                        setc(x, b - 1 + j, row[0], True)
                        setc(x + 1, b - 1 + j, row[1], True)
                    opened -= {(x, b - 1), (x + 1, b - 1), (x, b), (x + 1, b)}
                elif r < 0.55:
                    dx = 0 if rnd(x, b, salt + 43) < 0.5 else 1
                    t, u = CYPRESS[int(rnd(x, b, salt + 47) * 2)]
                    setc(x + dx, b - 1, t, True)
                    setc(x + dx, b, u, True)
                    opened -= {(x + dx, b - 1), (x + dx, b)}
            for y in range(a, top):
                for dx in (0, 1):
                    setc(x + dx, y, GRASS, False)
                    done.add((x + dx, y))
                    opened.add((x + dx, y))
            # the crown's rim pokes into the row above
            if top <= bot:
                for dx in (0, 1):
                    m = get(x + dx, top - 1)
                    if (x + dx, top - 1) in cells and (x + dx, top - 1) not in opened:
                        continue
                    if m in (GRASS, GRASS2, FLOWERS, SHADE):
                        setc(x + dx, top - 1, TIP_GRASS[dx], None)
                    elif m == TALL:
                        setc(x + dx, top - 1, TIP_TALL[dx], None)
                    elif m == SEA:
                        setc(x + dx, top - 1, TIP_SEA[dx], None)

    # columns left over (an odd width): cypresses two by two, then singles
    for (x, y) in sorted(cells - done, key=lambda c: (c[0], c[1])):
        if (x, y) in done:
            continue
        if (x, y + 1) in cells and (x, y + 1) not in done:
            t, u = CYPRESS[int(rnd(x, y, salt + 53) * 2)]
            setc(x, y, t, True)
            setc(x, y + 1, u, True)
            done |= {(x, y), (x, y + 1)}
        elif single and single(x, y):
            done.add((x, y))
        else:
            setc(x, y, SHADE, True)
            done.add((x, y))
    return opened
