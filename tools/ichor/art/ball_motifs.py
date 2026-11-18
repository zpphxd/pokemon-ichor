"""The mark on each ball's cap, at both sizes, for balls.py.

Each mark is drawn by hand as ASCII blocks at absolute pixel positions:
`m` is the mark's dark, `M` its light, `x` a third color, `K` ink and
`1`-`4` the cap's own ramp. The battle cap is rows 3-7 of a 16x16 frame
(its highlight sits at x 5-6); the icon cap is rows 4-10 of 24x24 (its
highlight at x 5-8, the boss at x 9-14 from row 9). balls.py only lets a
mark land on cap pixels. A few marks (the web, the ripples, the crescent,
the ring) are geometric and computed instead.
"""
from __future__ import annotations

import math


def blocks(*parts):
    """blocks((x0, y0, rows), ...) -> {(x, y): role}; '.' and ' ' skip."""
    out = {}
    for x0, y0, rows in parts:
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in ". ":
                    out[(x0 + i, y0 + j)] = ch
    return out


def ring(cx, cy, r, w=0.55, size=24, rows=(3, 11), lit="M", dark="m", only_top=False):
    out = {}
    for y in range(*rows):
        for x in range(size):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if abs(d - r) <= w and (not only_top or y + 0.5 <= cy):
                out[(x, y)] = lit if (x + 0.5 - cx) + (y + 0.5 - cy) < 0 else dark
    return out


MOTIFS = {}

# Theseus: the horns of the bull of Marathon, in terracotta, where the Great
# Ball had its two red marks.
MOTIFS["great"] = (
    blocks((5, 4, ["M....M",
                   "m....m",
                   ".mmmm."])),
    blocks((7, 5, ["M........M",
                   "mM......Mm",
                   ".mm....mm.",
                   "..mmmmmm.."])),
)

# Herakles: the lion's pelt, and his olive-wood club across it.
MOTIFS["ultra"] = (
    blocks((7, 4, ["..Mm",
                   ".Mm.",
                   "Mm.."])),
    blocks((8, 4, [".....MMm",
                   "....Mmmm",
                   "...Mmm..",
                   "..Mmm...",
                   ".Mm....."])),
)

# Daedalus: the labyrinth, as a meander key.
MOTIFS["master"] = (
    blocks((7, 4, ["mmmm",
                   "m..m",
                   "mm.m"])),
    blocks((9, 4, ["mmmmmmm",
                   "m.....m",
                   "m.mmm.m",
                   "m.m...m",
                   "m.mmmmm"])),
)

# Xenia: the red fillet tied round a guest-gift.
MOTIFS["premier"] = (
    blocks((7, 4, ["m..m",
                   "mMMm",
                   "m..m"])),
    blocks((9, 5, ["mm..mm",
                   "mMmmMm",
                   ".mMMm.",
                   "m.mm.m"])),
)

# Asclepius: the rod and its serpent.
MOTIFS["heal"] = (
    blocks((7, 3, ["..",
                   "xm",
                   ".mx",
                   "xm"])),
    blocks((10, 4, ["..m..",
                    ".xmM.",
                    "..mMx",
                    ".xMm.",
                    "..mM."])),
)

# Alcyone: the kingfisher, wings spread over her nest.
MOTIFS["nest"] = (
    blocks((5, 4, ["m....m",
                   ".M..M.",
                   "..mm.."])),
    blocks((8, 5, ["Mm....mM",
                   ".Mm..mM.",
                   "..mMMm..",
                   "...mm..."])),
)

# Poseidon: the trident, in gold.
MOTIFS["dive"] = (
    blocks((6, 4, ["M.M.M",
                   "mmmmm",
                   "..m.."])),
    blocks((10, 4, ["M.M.M",
                    "m.m.m",
                    "MMMmm",
                    "..m..",
                    "..m.."])),
)

# Nyx: the stars of her mantle.
MOTIFS["dusk"] = (
    blocks((9, 4, ["M"]), (6, 6, ["m"]), (10, 6, ["M"]), (7, 3, ["m"])),
    blocks((13, 4, [".M.",
                    "MMM",
                    ".M."]),
           (9, 5, ["M"]), (16, 8, ["M"]), (7, 8, ["m"]), (11, 7, ["m"]), (15, 4, ["m"]),
           (17, 6, ["m"])),
)

# Chronos: a sundial, the hours fanning out from the gnomon, and the sun.
MOTIFS["timer"] = (
    blocks((5, 4, ["m.MM.m",
                   ".m..m.",
                   "..mm.."])),
    blocks((6, 4, ["..m..MM..m..",
                   "m..m.MM.m..m",
                   ".m..m..m..m.",
                   "..m.m..m.m..",
                   "....mmmm...."])),
)

# Hermes: a wing from his hat.
MOTIFS["quick"] = (
    blocks((7, 3, ["..MM",
                   ".MMm",
                   "MMm.",
                   "mm.."])),
    blocks((8, 4, ["....MMM",
                   "...MMMm",
                   "..MMMm.",
                   ".MMmm..",
                   "Mmm...."])),
)

# Mnemosyne: ripples on the pool of memory.
MOTIFS["repeat"] = (
    {**ring(7.5, 7.5, 2.4, w=0.5, size=16, rows=(3, 7), only_top=True)},
    {**ring(11.5, 10.0, 2.9, w=0.5, rows=(4, 9), only_top=True),
     **ring(11.5, 10.0, 5.4, w=0.5, rows=(4, 9), only_top=True)},
)

# Plutus: his coins.
MOTIFS["luxury"] = (
    blocks((8, 4, ["Mm"]), (8, 5, ["mm"]), (10, 6, ["Mm"])),
    blocks((12, 4, ["MMm",
                    "Mmm",
                    ".m."]),
           (8, 6, ["MMm",
                   "Mmm",
                   ".m."]),
           (15, 7, ["Mm",
                    "mm"])),
)

# Arete: the rising steps of excellence, in gold.
MOTIFS["level"] = (
    blocks((6, 4, ["....M",
                   "..M.M",
                   "M.M.M"])),
    blocks((8, 4, ["......Mm",
                   "......Mm",
                   "...Mm.Mm",
                   "...Mm.Mm",
                   "Mm.Mm.Mm"])),
)

# Glaucus: the fisherman's catch, a silver fish.
MOTIFS["lure"] = (
    blocks((6, 4, [".MMm.m",
                   "MKmmmm",
                   ".mmm.m"])),
    blocks((8, 5, ["..MMMm.m",
                   ".MKMmmmm",
                   "MMmmmm.m",
                   "..mmm..."])),
)

# Selene: the crescent moon.
MOTIFS["moon"] = (
    blocks((7, 3, [".MM",
                   "M..",
                   "M..",
                   ".mm"])),
    {k: v for k, v in ring(11.0, 6.5, 2.7, w=0.75, rows=(3, 11)).items()
     if math.hypot(k[0] + 0.5 - 13.0, k[1] + 0.5 - 5.8) > 2.6},
)

# Philia: two rings linked, friendship.
MOTIFS["friend"] = (
    blocks((6, 4, [".M.m.",
                   "M.M.m",
                   ".M.m."])),
    blocks((8, 5, [".MM.mm.",
                   "M..M..m",
                   "M..m..m",
                   ".mm.mm."])),
)

# Eros: a red heart, the ivy-leaf of the painted cups.
MOTIFS["love"] = (
    blocks((6, 4, ["MM.mm",
                   "Mmmmm",
                   ".mmm."])),
    blocks((9, 4, [".MM.mm.",
                   "MMmmmmm",
                   "Mmmmmmm",
                   ".mmmmm.",
                   "..mmm.."])),
)

# Atalanta: the golden apple she stopped to pick up.
MOTIFS["fast"] = (
    blocks((8, 3, ["Kx"]), (7, 4, ["MMm", "Mmm", ".m."])),
    blocks((12, 3, ["Kxx"]), (12, 4, ["Kx"]),
           (10, 5, [".MMm.",
                    "MMmmm",
                    "Mmmmm",
                    ".mmm."])),
)

# Atlas: the sky's sphere he bears, a meridian and the slanted ecliptic.
MOTIFS["heavy"] = (
    blocks((8, 3, ["M", "M", "M", "M"]), (3, 6, ["mm"]), (5, 5, [".mm"]), (9, 4, ["mm"]),
           (11, 3, ["m"])),
    blocks((12, 4, ["M", "M", "M", "M", "M"]),
           (5, 8, ["mm"]), (7, 7, ["mmm"]), (10, 6, ["mm"]), (13, 6, ["m"]), (14, 5, ["mmm"]),
           (17, 4, ["m"])),
)

# Hypnos: the poppy of sleep.
MOTIFS["dream"] = (
    blocks((7, 4, ["MM", "MKm", ".mm"])),
    blocks((10, 4, [".Mm.",
                    "MMmmm",
                    "MmKmm",
                    ".mmm.",
                    "..x.."])),
)

# Pan: his pipes, bound with a cord.
MOTIFS["safari"] = (
    blocks((6, 4, ["MmMmMm",
                   "MmMm..",
                   "Mm...."])),
    blocks((8, 4, ["MmMmMmMm",
                   "KKKKKKKK",
                   "MmMmMm..",
                   "MmMm....",
                   "Mm......"])),
)

# Agon: the games, black-figure stripes either side of a discus.
MOTIFS["sport"] = (
    blocks((5, 4, ["m.MM.m",
                   "m.MM.m",
                   "m....m"])),
    blocks((6, 4, [".m.......m.",
                   ".m..MM...m.",
                   "m..MMMM...m",
                   "m...MM....m",
                   "m.........m"])),
)

# Elysium: asphodel, the white flowers of the blessed meadow.
MOTIFS["park"] = (
    blocks((6, 4, [".M..M",
                   "MmM..",
                   ".M..."])),
    blocks((8, 5, [".M.",
                    "MmM",
                    ".M."]),
           (13, 4, [".M.",
                    "MmM",
                    ".M."]),
           (16, 7, ["M"]), (11, 8, ["M"])),
)

# Typhon: the storm-serpent, fire down his back.
MOTIFS["beast"] = (
    blocks((4, 4, ["..M..M.",
                   ".M.mM.m",
                   "M..m..."])),
    blocks((5, 5, ["...M....M...M",
                   "..M.m..M.m.Mm",
                   ".M...mM...mK.",
                   "M.....m......"])),
)

# Charis: a rosette, the gift of grace.
MOTIFS["cherish"] = (
    blocks((7, 4, ["M.m", ".M.", "m.m"])),
    blocks((10, 4, ["M.M.m",
                    ".MMm.",
                    "MMxmm",
                    ".mmm.",
                    "m.m.m"])),
)

# Aion: the serpent ring of eternity, swallowing its tail.
MOTIFS["strange"] = (
    blocks((7, 4, ["MMm", "M.m", "mmK"])),
    {**ring(12.0, 6.5, 2.4, w=0.6, rows=(3, 10)), (14, 8): "K"},
)


def lattice(size_cap, step):
    """Arachne's web: a diamond lattice over the whole cap."""
    out = {}
    y0, y1, x0, x1 = size_cap
    for y in range(y0, y1):
        for x in range(x0, x1):
            a, b = (x + y) % step == 0, (x - y) % step == 0
            if a and b:
                out[(x, y)] = "M"
            elif a or b:
                out[(x, y)] = "m"
    return out


MOTIFS["net"] = (lattice((3, 8, 2, 14), 3), lattice((4, 11, 3, 21), 4))

# The Poke Ball carries no mark: its look is the red over white itself.
MOTIFS["poke"] = ({}, {})


def apply(balls):
    for b in balls:
        m16, m24 = MOTIFS[b["key"]]
        b["motif16"] = dict(m16)
        b["motif24"] = dict(m24)
