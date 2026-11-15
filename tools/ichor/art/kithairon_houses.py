"""Eleutherai's houses: Eleusa's house kit, pixel for pixel (eleusa_house.py).

Eleutherai is Eleusis's border town: the same Attic country building, lime
plaster on a rubble socle under red Laconian tiles. Only the parts the town
uses are copied: the tiled roof, the wall rows, two windows and two doors.
Fronts are arrangements of these parts (the map builder composes them).
"""
from __future__ import annotations

import eleusa_house
import kithairon_lib as K

SEC = "houses"
KEEP = {
    "roof_tile": None,
    "wall": None,
    "windows": ("shutters", "lattice", "closed"),
    "doors": ("plank", "curtain"),
}


def _subset(src, names):
    """A copy of some named one-row cells of src, in the given order."""
    s = K.struct(src.key, src.title, len(names), 1, SEC, walk=["D" * len(names)] if src.key == "doors"
                 else ["X" * len(names)], notes=src.notes,
                 names={n: (i, 0) for i, n in enumerate(names)})
    for i, n in enumerate(names):
        cx, cy = src.names[n]
        for ln in ("bottom", "middle", "top"):
            s.layers[ln].a[:, i * 16:i * 16 + 16] = src.layers[ln].a[cy * 16:cy * 16 + 16,
                                                                     cx * 16:cx * 16 + 16]
    return s


def build():
    out = []
    for src in eleusa_house.build_parts():
        if src.key not in KEEP:
            continue
        names = KEEP[src.key]
        if names is None:
            s = K.struct(src.key, src.title, src.w, src.h, SEC, walk=list(src.walk),
                         notes=src.notes, names=dict(src.names))
            for ln in ("bottom", "middle", "top"):
                s.layers[ln].a[:] = src.layers[ln].a
            s.behaviors = dict(src.behaviors)
        else:
            s = _subset(src, names)
        out.append(s)
    return out
