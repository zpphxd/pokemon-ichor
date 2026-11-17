#!/usr/bin/env python3
"""Thyrsa polish: the land outside the walls, wall towers, flower beds.

Run once on the restored map; it repaints the country outside the walls
(groves, scrub, the necropolis on the south road, the vineyard past the
Proitid gate) and leaves the walled city's cells alone except where noted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapedit import Layout  # noqa: E402
from paint import paint, tufts  # noqa: E402

m = Layout("ThyrsaCity")

# West of the walls, x0-7: olive groves on the Kopais side, a cleared strip
# along the wall, the Kopais road (rows 23-24) kept as it is.
WEST = [
    "OOOOOOOO",  # 0
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOO,c",
    "OOOOOO,c",
    "OOOOOO;,",  # 5
    "OOOO,,,,",
    "OOOOr,c,",
    "OO,;,,c,",
    "OO,,OO,,",
    ",,r,OO,,",  # 10
    ",;,,OO;,",
    "OO,,,,,c",
    "OOOO,,,c",
    "OOOOOO,,",
    "OOOOOO,,",  # 15
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOOOO",
    ",,OO,;c,",
    ",;,,,,c,",  # 20
    ",,c,..ff",
    ",,c,...f",
    "========",
    "========",
    "OO,c....",  # 25
    "OO,c:..f",
    "OOOO,,c,",
    "OOOO,,c,",
    "OOOOOO,,",
    "PPOOOO,,",  # 30
    "PPOOOO;,",
    "PPOOOOOO",
    "PPOOOOOO",
    "OO,,OOOO",
    "OO,r,,OO",  # 35
    "OO,,,,,c",
    "OOOO,;,c",
    "OOOOOO,,",
    "OOOOOO,,",
    "OOOOOOOO",  # 40
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOOOO",  # 45
    "OOOOOOOO",
    "OOOOOOOO",
]

# East of the walls, x48-55: groves, then the Proitid road (rows 30-31) runs
# out into the vineyard on the plain.
EAST = [
    "OOOOOOOO",  # 0
    "OOOOOOOO",
    "c,OOOOOO",
    "c,OOOOOO",
    ",,,,OOOO",
    ",r,,OOOO",  # 5
    "OO,,OOOO",
    "OO,,,;OO",
    "OOc,,,OO",
    "OOc,PPOO",
    "OOOOPPOO",  # 10
    "OOOOPPOO",
    "OOOOPPOO",
    "OOOOOOOO",
    ",,OOOOOO",
    ",;OOOOOO",  # 15
    "c,,,OOOO",
    "c,k,OOOO",
    ",,,,,,OO",
    "OO,;,,OO",
    "OOOO,,OO",  # 20
    "OOOO,,OO",
    "OOOOc,OO",
    "OO,,c,OO",
    ",,,,OOOO",
    "PP,,OOOO",  # 25
    "PP,,OOOO",
    ",,c,,,,c",
    "..c..,,c",
    ".:..f,,,",
    "========",  # 30
    "========",
    ".f..:...",
    "........",
    "VVVVVV..",
    "VVVVVV..",  # 35
    "......:.",
    "VVVVVV..",
    "VVVVVV.,",
    "......,,",
    "VVVV,,,c",  # 40
    "VVVV,,,c",
    "OOOOOO,,",
    "OOOOOO;,",
    "OOOOOOOO",
    "OOOOOOOO",  # 45
    "OOOOOOOO",
    "OOOOOOOO",
]

# South of the walls, x8-47, rows 41-47: the necropolis along the road out of
# the south gate (x26-29), meadow under the wall, groves beyond.
#            x8        x18       x28       x38
SOUTH = [a + b + "====" + c + d for a, b, c, d in [
    # x8-9  x10-25              x30-45              x46-47
    ("OO", "......c.:....f..", "..f.....c....:..", "OO"),  # 41
    ("OO", "..:...c.ff.cs...", "...sc...c...c...", "OO"),  # 42
    ("OO", "......f..:.cf...", "...fc.:.f...c...", "OO"),  # 43
    ("OO", "OOOO,,OO,;,,c,cs", "ch,;OOOO,,OOOO,,", "OO"),  # 44
    ("OO", "OOOO,cOOOO,,c,cF", "cs,,OOOO,cOOOOOO", "OO"),  # 45
    ("OO", "OOOO,cOOOOOO,;ns", "nF,;OOOO,cOOOOOO", "OO"),  # 46
    ("OO", "OOOO,;OOOOOO,FF,", "s,F,OOOO,;OOOOOO", "OO"),  # 47
]]

paint(m, 0, 0, WEST, seed=11)
paint(m, 48, 0, EAST, legend={"V": (0x001, True)}, seed=12)
paint(m, 8, 41, SOUTH, seed=13)

# Vineyard: vines on stakes (3C4/3C5 over 3CC/3CD), two to a unit.
for j, row in enumerate(EAST):
    for i, c in enumerate(row):
        if c != "V":
            continue
        k = j
        while k > 0 and EAST[k - 1][i] == "V":
            k -= 1
        upper, left = (j - k) % 2 == 0, i % 2 == 0
        mid = (0x3C4 if left else 0x3C5) if upper else (0x3CC if left else 0x3CD)
        m.put(48 + i, j, mid, solid=not upper)

# North wall: two towers break its 26-cell inner face (STYLE.md 4.5: towers
# along the wall), and a votive stele marks the corner of the temple precinct.
TOWER = ((0x278, 0x279), (0x280, 0x281), (0x288, 0x289), (0x290, 0x291), (0x298, 0x299))
for tx in (16, 21, 38):
    for dy, (a, b) in enumerate(TOWER):
        m.put(tx, dy, a, solid=True)
        m.put(tx + 1, dy, b, solid=True)
for sx in ():
    m.put(sx, 3, 0x228, solid=True)

# Flowers: clear the confetti inside the walls, then plant beds by doors,
# house walls and shrines.
for y in range(3, 38):
    for x in range(10, 46):
        if m.id(x, y) != 0x004:
            continue
        m.put(x, y, 0x001)
BEDS = [
    # Semele's chamber (the ruined bridal room, x14-16 rows 6-7): offerings
    (13, 6), (13, 7), (17, 7), (17, 6),
    # the Sown house door (19, 6)
    (18, 7), (20, 7),
    # the Vintner's house front
    (10, 17), (11, 17), (10, 18),
    # under the NE houses' walls
    (42, 9), (42, 10), (42, 11),
    (43, 6), (44, 6), (44, 7),
    # by the Dirke spring (23, 34) and the south-west lane
    (20, 36), (21, 36), (20, 37),
    (11, 36), (12, 36), (12, 37),
]
for x, y in BEDS:
    if m.id(x, y) == 0x001:
        m.put(x, y, 0x004)

# Worn ground and tufts in the yards inside the walls and under them outside.
tufts(m, (10, 3, 45, 37), share=0.10, seed=21)
tufts(m, (10, 41, 45, 43), share=0.10, seed=22)

m.save()
print("thyrsa: painted")
