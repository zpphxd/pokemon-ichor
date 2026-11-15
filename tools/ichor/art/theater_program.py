#!/usr/bin/env python3
"""The Dionysia's program (design/phase3/SCRIPT.md beat 32, Part 10): a papyrus
sheet reading THE UNWOVEN. A TRAGEDY IN FOUR SCENES. BY: and then nothing but a
little hook where the name should be (the same hook as under Emporion's owl).

Writes graphics/ichor/act2/program.png: 64 x 64, 16 colors, color 0
transparent, which src/ichor_act2_scene.c shows in a picture box
(Ichor_ShowProgram). Also a 4x preview in design/phase3/img/theater_program.png.

Usage: /usr/bin/python3 tools/ichor/art/theater_program.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/ichor/act2/program.png"
PREVIEW = ROOT / "design/phase3/img/theater_program.png"

PAL = [
    (255, 0, 255),     # 0 transparent
    (240, 224, 184),   # 1 papyrus, light
    (216, 192, 136),   # 2 papyrus
    (176, 144, 96),    # 3 papyrus, the fibres and the rolled ends' shade
    (120, 88, 56),     # 4 the rolled ends' edge
    (40, 32, 24),      # 5 ink
    (152, 40, 32),     # 6 red ink, the title
    (64, 48, 40),      # 7 ink, faded
]

# A 3 x 5 capital font (the play's program is lettered by hand)
FONT = {
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"], "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"], "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"], "N": ["101", "111", "111", "111", "101"],
    "O": ["010", "101", "101", "101", "010"], "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "111", "111", "101"], "Y": ["101", "101", "010", "010", "010"],
    ":": ["0", "1", "0", "1", "0"], ".": ["0", "0", "0", "0", "1"], " ": ["00", "00", "00", "00", "00"],
}

HOOK = [
    "..55.",
    ".5..5",
    "....5",
    "...5.",
    "..5..",
    "..5..",
    ".5..5",
    "..55.",
]


def text_width(s):
    return sum(len(FONT[c][0]) + 1 for c in s) - 1


def draw_text(px, x, y, s, color):
    for c in s:
        g = FONT[c]
        for j, row in enumerate(g):
            for i, b in enumerate(row):
                if b == "1":
                    px[x + i, y + j] = color
        x += len(g[0]) + 1


def main():
    img = Image.new("P", (64, 64), 0)
    flat = []
    for c in PAL:
        flat += list(c)
    flat += [0] * (768 - len(flat))
    img.putpalette(flat)
    px = img.load()
    # the sheet, a little skewed at its edges, with rolled ends top and bottom
    for y in range(4, 60):
        x0 = 6 + (1 if y % 11 == 3 else 0)
        x1 = 57 - (1 if y % 13 == 5 else 0)
        for x in range(x0, x1 + 1):
            fib = (y * 3 + (x // 9)) % 7 == 0
            px[x, y] = 3 if fib and (x + y) % 3 else (2 if (x * 7 + y * 5) % 17 == 0 else 1)
        px[x0, y] = 3
        px[x1, y] = 3
    for (y0, y1) in ((2, 6), (57, 61)):
        for y in range(y0, y1 + 1):
            for x in range(4, 60):
                edge = y in (y0, y1) or x in (4, 59)
                px[x, y] = 4 if edge else (2 if y == (y0 + y1) // 2 else 3)
    # the title in red, the rest in ink
    def centered(y, s, color):
        draw_text(px, 32 - text_width(s) // 2, y, s, color)
    centered(10, "THE", 6)
    centered(17, "UNWOVEN", 6)
    for x in range(14, 50):
        if x % 3 != 2:
            px[x, 24] = 7
    centered(28, "A TRAGEDY", 5)
    centered(35, "IN FOUR SCENES", 5)
    draw_text(px, 12, 45, "BY:", 5)
    # where the name should be: nothing, except a little hook
    for j, row in enumerate(HOOK):
        for i, ch in enumerate(row):
            if ch == "5":
                px[30 + i, 42 + j] = 5
    for x in range(26, 50, 2):
        px[x, 51] = 3
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").resize((256, 256), Image.NEAREST).save(PREVIEW)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
