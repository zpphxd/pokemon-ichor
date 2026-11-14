#!/usr/bin/env python3
"""Draw the ICHOR wordmark into graphics/title_screen/emerald_version.png.

Phase 0 placeholder. It replaces the "EMERALD VERSION" banner on the title
screen, reusing the original 16-color grayscale palette and 128x32 size so no
code changes are needed. The Phase 1 art pass replaces the full title screen.

Usage: python3 tools/ichor/make_title_banner.py
"""
import struct
import zlib
from pathlib import Path

PNG = Path(__file__).resolve().parents[2] / "graphics/title_screen/emerald_version.png"
W, H = 128, 32
T = 6           # stroke thickness
LH = 24         # letter height
TOP = 4         # top row of letters
SHEAR = 4       # 1 px of italic slant per SHEAR rows

# Palette indices in the original grayscale palette.
TRANSPARENT, OUTLINE, DEEP = 0, 4, 14
FILL_TOP, FILL_HI, FILL_MID, FILL_LO, FILL_BOTTOM = 15, 6, 12, 10, 8


def cut_corners(cells, w, h, r=3):
    """Round a letter's outer corners by removing small triangles."""
    out = set()
    for x, y in cells:
        if x + y < r or (w - 1 - x) + y < r or x + (h - 1 - y) < r or (w - 1 - x) + (h - 1 - y) < r:
            continue
        out.add((x, y))
    return out


def rect(x0, y0, x1, y1):
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def letter_I():
    return 9, rect(0, 0, 8, LH - 1)


def letter_C():
    w = 21
    outer = cut_corners(rect(0, 0, w - 1, LH - 1), w, LH)
    hole = rect(T, T, w - 1, LH - 1 - T)
    return w, outer - hole


def letter_H():
    w = 21
    return w, rect(0, 0, T - 1, LH - 1) | rect(w - T, 0, w - 1, LH - 1) | rect(0, 9, w - 1, 14)


def letter_O():
    w = 22
    outer = cut_corners(rect(0, 0, w - 1, LH - 1), w, LH)
    return w, outer - rect(T, T, w - 1 - T, LH - 1 - T)


def letter_R():
    w = 21
    bowl = cut_corners(rect(0, 0, w - 2, 14), w - 1, 15) - rect(T, T - 1, w - 2 - T, 14 - T + 1)
    stem = rect(0, 0, T - 1, LH - 1)
    leg = set()
    for y in range(13, LH):
        x0 = 8 + (y - 13)
        leg |= rect(x0, y, min(x0 + T - 1, w - 1), y)
    return w, bowl | stem | leg


def draw():
    letters = [letter_I(), letter_C(), letter_H(), letter_O(), letter_R()]
    gap = 3
    total = sum(w for w, _ in letters) + gap * (len(letters) - 1) + LH // SHEAR
    x = (W - total) // 2
    fill = set()
    for w, cells in letters:
        for cx, cy in cells:
            y = TOP + cy
            fill.add((x + cx + (TOP + LH - 1 - y) // SHEAR, y))
        x += w + gap

    grid = [[TRANSPARENT] * W for _ in range(H)]
    for px, py in fill:
        band = (py - TOP) / (LH - 1)
        if band < 0.30:
            c = FILL_TOP
        elif band < 0.50:
            c = FILL_HI
        elif band < 0.70:
            c = FILL_MID
        elif band < 0.88:
            c = FILL_LO
        else:
            c = FILL_BOTTOM
        grid[py][px] = c
    # Two-pixel outline: dark ring, then a deep shadow ring below/right.
    for ring, color in ((1, OUTLINE), (2, DEEP)):
        add = []
        for py in range(H):
            for px in range(W):
                if grid[py][px] != TRANSPARENT:
                    continue
                for dx in range(-ring, ring + 1):
                    for dy in range(-ring, ring + 1):
                        nx, ny = px + dx, py + dy
                        if 0 <= nx < W and 0 <= ny < H and (nx, ny) in fill:
                            if ring == 2 and not (dx <= 0 and dy <= 0 and (dx or dy)):
                                continue
                            add.append((px, py))
                            break
                    else:
                        continue
                    break
        for px, py in add:
            grid[py][px] = color
    return grid


def write_png(grid):
    data = PNG.read_bytes()
    pos, kept = 8, []
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if ctype not in (b"IDAT", b"IEND"):
            kept.append((ctype, data[pos + 8:pos + 8 + n]))
        pos += 12 + n
    raw = b"".join(b"\x00" + bytes(row) for row in grid)

    def chunk(t, c):
        return struct.pack(">I", len(c)) + t + c + struct.pack(">I", zlib.crc32(t + c) & 0xFFFFFFFF)

    out = b"\x89PNG\r\n\x1a\n" + b"".join(chunk(t, c) for t, c in kept)
    out += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    PNG.write_bytes(out)


if __name__ == "__main__":
    write_png(draw())
    print(f"wrote {PNG}")
