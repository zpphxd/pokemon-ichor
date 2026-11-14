#!/usr/bin/env python3
"""Paint the bands of Ichor's battle transitions: the screen becomes a vase.

Two transitions in src/battle_transition.c use these BG0 tiles (BG palette 15):
* B_TRANSITION_ICHOR_WILD: friezes of black glaze, meander and clay sweep in
  from alternate sides, band by band, like the rings of a turning pot.
* B_TRANSITION_ICHOR_TRAINER: a black glaze shoulder and foot frame a wide
  clay band between two meander friezes; the opponent and the player slide
  onto it as black-figure silhouettes and face off, as on an Attic amphora.

Writes graphics/battle_transitions/ichor_pottery.png (tiles and palette),
ichor_wild.bin and ichor_trainer.bin (32x20 BG0 maps; the code ORs in
palette 15).

Usage: python3 tools/ichor/art/ui_battle_transitions.py
"""
import struct

from ui_battle_lib import BT, CLAY, CLAY_DARK, CLAY_LIGHT, INK, MEANDER, ROOT, IdxCanvas

PAL = [(0, 0, 0), INK, CLAY_DARK, CLAY, CLAY_LIGHT] + [(0, 0, 0)] * 11
I_INK, I_LINE, I_CLAY, I_LIGHT = 1, 2, 3, 4

T_GLAZE, T_CLAY, T_FRIEZE, T_GROUND, T_GLAZE_LIP, T_RAYS = range(6)
VFLIP = 0x800

# Rays: black spikes rising from the glaze below, the band painters set
# above a vase's foot (flipped, they hang from the shoulder).
RAYS = [
    "...#....",
    "...#....",
    "..###...",
    "..###...",
    ".#####..",
    ".#####..",
    "#######.",
    "########",
]


def tiles():
    c = IdxCanvas(128, 8)
    c.rect(8 * T_GLAZE, 0, 8 * T_GLAZE + 7, 7, I_INK)
    c.rect(8 * T_CLAY, 0, 8 * T_CLAY + 7, 7, I_CLAY)
    # Meander frieze: a clay gap, the key, an incised line, clay.
    x = 8 * T_FRIEZE
    c.rect(x, 0, x + 7, 7, I_CLAY)
    for r, row in enumerate(MEANDER):
        for col, ch in enumerate(row):
            if ch == "#":
                c.set(x + col, 1 + r, I_INK)
    c.hline(x, x + 7, 6, I_LINE)
    # Ground line the figures stand on.
    x = 8 * T_GROUND
    c.rect(x, 0, x + 7, 7, I_CLAY)
    c.hline(x, x + 7, 5, I_INK)
    c.hline(x, x + 7, 6, I_LINE)
    # Glaze with a lighter lip where it meets the clay below.
    x = 8 * T_GLAZE_LIP
    c.rect(x, 0, x + 7, 7, I_INK)
    c.hline(x, x + 7, 7, I_LINE)
    x = 8 * T_RAYS
    c.rect(x, 0, x + 7, 7, I_CLAY)
    c.blit(x, 0, RAYS, {"#": I_INK})
    return c


def write_map(name, rows):
    entries = []
    for r in rows:
        entries += [r] * 32
    assert len(entries) == 32 * 20
    path = BT / name
    path.write_bytes(struct.pack("<640H", *entries))
    print(f"wrote {path.relative_to(ROOT)}")


def main():
    tiles().save(BT / "ichor_pottery.png", PAL)
    # Wild: a glaze band with its meander, then clay with rays rising from
    # the next glaze, five times; each 16 px pair of rows sweeps in as one.
    write_map("ichor_wild.bin",
              [T_GLAZE_LIP, T_FRIEZE, T_CLAY, T_RAYS] * 5)
    # Trainer: a glaze shoulder with hanging rays, a frieze, the figure band,
    # the ground line, a frieze, rays rising from the glaze foot.
    write_map("ichor_trainer.bin",
              [T_GLAZE] * 2 + [T_RAYS | VFLIP, T_FRIEZE] + [T_CLAY] * 10
              + [T_GROUND, T_FRIEZE | VFLIP, T_RAYS] + [T_GLAZE] * 3)


if __name__ == "__main__":
    main()
