#!/usr/bin/env python3
"""Thyrsa's Agora interior: a wine-and-mask market hall behind a stoa front.

12x10, Aethos + Civic. The merchant (5, 3) serves from a striped-awning wine
stall over its counter (row 4); the exit mat stays at (6, 9).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapedit import Layout  # noqa: E402

m = Layout("ThyrsaCity_Agora")

F, f1, f2, f3 = 0x280, 0x281, 0x282, 0x283     # sandstone flags (walkable)
WALK = {F, f1, f2, f3, 0x26B, 0x242, 0x27F}

A, C, K, B1, B2, M = 0x2C0, 0x2BD, 0x2AE, 0x2D0, 0x2D1, 0x2BE   # amphora, crate, krater, grain, mask bust
G = [
    # 0      1      2      3      4      5      6      7      8      9      10     11
    [0x260, 0x287, 0x287, 0x287, 0x287, 0x287, 0x287, 0x287, 0x287, 0x287, 0x287, 0x260],  # 0
    [0x261, 0x284, 0x285, 0x285, 0x263, 0x264, 0x265, 0x285, 0x285, 0x285, 0x286, 0x261],  # 1
    [0x262, 0x288, 0x289, 0x289, 0x266, 0x267, 0x268, 0x288, 0x289, 0x289, 0x289, 0x262],  # 2
    [A,     F,     B1,    B2,    0x269, 0x26B, 0x26C, K,     A,     F,     C,     A],      # 3
    [A,     F,     F,     F,     0x26D, 0x26E, 0x26F, A,     F,     F,     F,     C],      # 4
    [F,     0x270, F,     f1,    F,     F,     F,     F,     F,     f2,    0x270, M],      # 5
    [F,     0x271, F,     F,     F,     F,     F,     f3,    F,     F,     0x271, M],      # 6
    [f2,    0x272, F,     0x2B9, 0x2BA, F,     F,     F,     0x2BB, 0x2BC, 0x272, F],      # 7
    [A,     F,     A,     0x2B8, F,     F,     F,     F,     F,     0x2B8, C,     A],      # 8
    [A,     C,     F,     F,     f1,    F,     0x242, F,     F,     F,     C,     A],      # 9
]
for y, row in enumerate(G):
    for x, mid in enumerate(row):
        m.put(x, y, mid, solid=mid not in WALK, elev=3 if mid in WALK else 0)
m.save()
print("thyrsa agora: laid out")
