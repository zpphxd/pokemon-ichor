"""Pan's Crook's climbable face (WORLD_EXPLORATION §2): the one look every
cliff family shares.

A climbable face is a vertical strip of cliff, one metatile wide, with worn
**handholds cut in pairs** up it, **ivy hanging over its top edge**, and a
small **goat-hoof votive** scratched at its foot. Plain cliff never has
handholds; ivy alone is decoration.

This module only says where the marks go, as role codes per pixel of a 16x16
cell, so each tileset's painter maps them onto its own ramp:

  H  the hold's dark cut           h  its shadowed back wall
  L  the hold's lit lower lip      (light from the top left)
  W  the worn rock round a hold
  I  ivy, dark    i  ivy, mid      v  ivy, lit
  V  the votive's scratched lines  S  the votive's lit edge

The holds sit in the cell's left half (x 1-6) on an 8 px period, so a face of
any height lines up cell to cell, and the right half of every face cell keeps
its tileset's own tiles (two new 8x8 tiles a cell, not four). The pairs are
staggered, left then right, the way a climber reaches.
"""
from __future__ import annotations

# One pair of holds per 8 rows: the left hold at rows 0-3, the right at 4-7.
# Each is a worn rim (W) round a dark cut, its lower lip catching the light.
HOLD = [".WW.", "WHHW", "WhhL", ".LL."]
HOLDS = [(0, 0), (3, 4)]          # (x, y) of each hold's top-left in an 8-row period

# Ivy over the top edge: hung from the lip, ragged at the bottom, a tendril
# reaching down the face. Row 0 is `lip - 2` (the ivy creeps over the edge).
IVY = [
    " vi   iv  ",
    "viIi ivIi ",
    "iIviIiIvi ",
    " IiIvIiIi ",
    "  IiI iIv ",
    "  I i  I  ",
    "  i    i  ",
    "       I  ",
]

# The votive: a cloven hoof print scratched into the rock, two lobes.
HOOF = [
    "V.V",
    "VSV",
    "VSV",
    ".V.",
]
HOOF_X = 4


def holds(rows=range(16), x0=0):
    """{(x, y): role} for the handholds in the given cell rows."""
    out = {}
    for base in (0, 8):
        for (hx, hy) in HOLDS:
            for j, line in enumerate(HOLD):
                y = base + hy + j
                if y not in rows:
                    continue
                for i, ch in enumerate(line):
                    if ch != ".":
                        out[(x0 + hx + i, y)] = ch
    return out


def ivy(lip):
    """{(x, y): role} for the ivy over a top edge whose lit lip is at row `lip`."""
    out = {}
    for j, line in enumerate(IVY):
        for i, ch in enumerate(line):
            if ch != " " and 0 <= lip - 2 + j < 16:
                out[(i, lip - 2 + j)] = ch
    return out


def hoof(y0):
    out = {}
    for j, line in enumerate(HOOF):
        for i, ch in enumerate(line):
            if ch != ".":
                out[(HOOF_X + i, y0 + j)] = ch
    return out


def marks(kind, lip=5, face_top=None, foot_base=12):
    """The marks for one cell of a face.

    kind   "top" (the brink: ivy over the lip, holds below it), "face" (holds
           all the way), or "foot" (holds, then the hoof votive near the base)
    lip    the top cell's lit-lip row
    face_top  first row of rock on a "top" cell (default lip + 2)
    foot_base the row where a "foot" cell's rock ends
    """
    if kind == "top":
        top = (lip + 2) if face_top is None else face_top
        m = holds(range(top + 2, 16))
        m.update(ivy(lip))
        return m
    if kind == "face":
        return holds()
    if kind == "foot":
        hy = max(1, foot_base - 5)
        m = holds(range(0, hy))
        m.update(hoof(hy))
        return m
    raise ValueError(kind)


def paint(px, cell_marks, roles, ox=0, oy=0):
    """Paint marks with a painter's px(x, y, color) and its {role: color} map."""
    for (x, y), r in cell_marks.items():
        if r in roles and roles[r] is not None:
            px(ox + x, oy + y, roles[r])
