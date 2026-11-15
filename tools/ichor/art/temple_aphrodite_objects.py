#!/usr/bin/env python3
"""The Temple of Aphrodite's mirror objects (Galatea's Gallery, SCRIPT.md Part 5).

  graphics/object_events/pics/misc/ichor/mirror_stand.png  (144 x 32, 9 frames)
      A bronze mirror on a stand, for the rose court's P1-P3 (OBJ_EVENT_GFX_ICHOR_MIRROR).
      Its facing is its angle, so the frames show it: 0 facing south (the polished
      face toward you), 1 north (the bronze back), 2 west (edge-on, the face to
      the left; east is the same flipped); 3-8 repeat them (a mirror never walks).
  graphics/object_events/pics/misc/ichor/mirror_mark.png   (16 x 16, blank)
      The invisible marker that stands on a wall mirror's tile (M0, W1, W2): the
      metatile draws the mirror, the object only turns the line of sight.

Both use the cast palette (OBJ_EVENT_PAL_TAG_ICHOR_CAST), copied from tablet.png.
TODO(art): the statues are still the Trick House statue; Galatea's are owed.

  /usr/bin/python3 tools/ichor/art/temple_aphrodite_objects.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "graphics/object_events/pics/misc/ichor"
# cast palette indices
T, OUT, BRN, RED, BRZ, RRED, LBRZ, PALE, GOLD, LGOLD, TAN, HI, DBLUE, BLUE, SLATE, OLIVE = range(16)


def frame_front():
    g = [[T] * 16 for _ in range(32)]
    # the disc: an oval, x 3..12, y 2..17
    cx, cy, rx, ry = 7.5, 9.5, 5.2, 7.6
    for y in range(32):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1.0:
                if d > 0.80:
                    g[y][x] = GOLD
                elif d > 0.62:
                    g[y][x] = BRZ
                else:
                    g[y][x] = LGOLD
            elif d <= 1.28 and g[y][x] == T:
                g[y][x] = OUT
    # the polish: a highlight streak and a blue gleam of sky
    for i in range(6):
        x, y = 5 + i // 2, 5 + i
        if g[y][x] == LGOLD:
            g[y][x] = HI
    for (x, y) in ((6, 4), (5, 6), (9, 12), (10, 11), (6, 13), (7, 14)):
        if g[y][x] == LGOLD:
            g[y][x] = BLUE if y > 10 else HI
    for (x, y) in ((8, 13), (9, 13), (8, 14)):
        if g[y][x] == LGOLD:
            g[y][x] = PALE
    stand(g)
    return g


def frame_back():
    g = [[T] * 16 for _ in range(32)]
    cx, cy, rx, ry = 7.5, 9.5, 5.2, 7.6
    for y in range(32):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1.0:
                g[y][x] = GOLD if d > 0.80 else (BRN if d > 0.55 else BRZ)
            elif d <= 1.28:
                g[y][x] = OUT
    for (x, y) in ((7, 9), (8, 9), (7, 10), (8, 10)):
        g[y][x] = GOLD                      # the boss
    g[8][7] = LGOLD
    stand(g)
    return g


def frame_side():
    """Edge-on, the polished face to the west (left)."""
    g = [[T] * 16 for _ in range(32)]
    for y in range(2, 18):
        h = abs(y - 9.5) / 8.0
        w = 2 if h > 0.8 else 3
        x0 = 7 - (w // 2)
        for x in range(x0, x0 + w):
            g[y][x] = LGOLD if x == x0 else (BRZ if x < x0 + w - 1 else BRN)
        g[y][x0 - 1] = OUT
        g[y][x0 + w] = OUT
    g[1][7] = OUT
    g[18][7] = OUT
    for y in (5, 6, 7):
        g[y][6] = HI
    stand(g)
    return g


def stand(g):
    """The neck, the slender stand and its three feet, under the disc."""
    for y in range(18, 28):
        g[y][7], g[y][8] = BRZ, BRN
        g[y][6], g[y][9] = OUT, OUT
    g[18][7], g[18][8] = GOLD, BRZ
    g[23][7] = GOLD
    for x in range(3, 13):
        g[28][x] = BRN if 4 <= x <= 11 else OUT
        g[29][x] = OUT if x in (3, 12) or not (4 <= x <= 11) else BRZ
        g[30][x] = OUT
    g[28][7], g[28][8] = BRZ, BRZ
    for x in (4, 11):
        g[29][x] = GOLD


def main():
    pal = Image.open(DIR / "tablet.png").getpalette()[:48]
    frames = [frame_front(), frame_back(), frame_side()]
    frames += [frames[0], frames[0], frames[1], frames[1], frames[2], frames[2]]
    sheet = Image.new("P", (16 * 9, 32), 0)
    sheet.putpalette(pal + [0] * (768 - len(pal)))
    for i, f in enumerate(frames):
        for y in range(32):
            for x in range(16):
                sheet.putpixel((i * 16 + x, y), f[y][x])
    sheet.save(DIR / "mirror_stand.png", bits=4)
    mark = Image.new("P", (16, 16), 0)
    mark.putpalette(pal + [0] * (768 - len(pal)))
    mark.save(DIR / "mirror_mark.png", bits=4)
    big = sheet.convert("RGB").resize((16 * 9 * 4, 32 * 4), Image.NEAREST)
    out = ROOT / "build/kythera_maps/mirror_stand_4x.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    big.save(out)
    print(out)


if __name__ == "__main__":
    main()
