#!/usr/bin/env python3
"""Review images for the post-game's first sprites (design/postgame/SPRITES.md).

Usage:
    python3 tools/ichor/art/sprites_pg_previews.py [--shots DIR]

Writes into design/postgame/img/:

    sprites_contact.png     the contact sheet: the Euploia's 18 frames (and the
                            east headings the engine flips) over the aethos sea,
                            every walker in all four directions, the portraits
    sprites_euploia_sea.png the ship at 1x and 3x over the sea, as on the GBA
    sprites_ingame.png      four frames from tools/ichor/tests/pg_sprites.sh's
                            run (--shots, default build/test_pg_sprites/shots)

The sea is rendered from the aethos primary's animated sea metatile (0x170)
by tools/ichor/render_map.py, so the ship is judged on the real water.
"""
import glob
import os
import struct
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, to_rgba, upscale  # noqa: E402
from sprites_npc import checker_bg, ref_rgba  # noqa: E402
import sprites_pg_ship as SHIP  # noqa: E402
import sprites_pg_walkers as WALK  # noqa: E402
import sprites_pg_portraits as PORT  # noqa: E402

IMG = os.path.join(ROOT, "design/postgame/img")
BG = (232, 224, 200, 255)
INK = (40, 24, 24, 255)


def sea(w, h):
    """A w x h field of aethos's sea, rendered by render_map.py."""
    tmp = os.path.join(ROOT, "build/render")
    os.makedirs(tmp, exist_ok=True)
    cols, rows = -(-w // 16), -(-h // 16)
    bin_path = os.path.join(tmp, "pg_sea.bin")
    with open(bin_path, "wb") as f:
        f.write(b"".join(struct.pack("<H", 0x170) for _ in range(cols * rows)))
    out = os.path.join(tmp, "pg_sea.png")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools/ichor/render_map.py"), "--blockdata", bin_path,
                    "--width", str(cols), "--primary", "aethos", "--secondary", "kalliste", "--scale", "1",
                    "-o", out], check=True, capture_output=True)
    return Image.open(out).convert("RGBA").crop((0, 0, w, h))


def ship_rows():
    """Both sheets' nine frames plus the three east frames, as RGBA rows."""
    rows = []
    for name, full in SHIP.SHEETS.items():
        a = SHIP.sheet(full)
        fr = [a[:, i * 64:(i + 1) * 64] for i in range(9)]
        rows.append((name, np.hstack(fr + [fr[2][:, ::-1], fr[7][:, ::-1], fr[8][:, ::-1]])))
    return rows


def label(d, xy, text):
    d.text(xy, text, fill=INK)


def ship_block(k=2):
    rows = ship_rows()
    w, h = 64 * 12, 64 * len(rows)
    water = sea(w, h)
    for i, (_, a) in enumerate(rows):
        water.alpha_composite(to_rgba(a, SHIP.PAL), (0, 64 * i))
    return upscale(water, k)


def walker_block(k=4):
    sh = WALK.sheets()
    pad, lw = 4, 24
    names = list(sh)
    cw = 16 * 12 + pad * 11
    out = Image.new("RGBA", (lw + cw, (32 + pad) * (len(names) + 1)), BG)
    items = [("prof_birch", ref_rgba())] + [(n, to_rgba(a, WALK.pal_of(n))) for n, a in sh.items()]
    for i, (n, im) in enumerate(items):
        frames = [im.crop((f * 16, 0, (f + 1) * 16, 32)) for f in range(9)]
        frames += [frames[2].transpose(Image.FLIP_LEFT_RIGHT), frames[7].transpose(Image.FLIP_LEFT_RIGHT),
                   frames[8].transpose(Image.FLIP_LEFT_RIGHT)]
        for f, fr in enumerate(frames):
            tile = checker_bg(16, 32)
            tile.alpha_composite(fr)
            out.alpha_composite(tile, (lw + f * (16 + pad), i * (32 + pad)))
    big = upscale(out, k)
    d = ImageDraw.Draw(big)
    for i, (n, _) in enumerate(items):
        label(d, (4, i * (32 + pad) * k + 4), n.replace("_", " "))
    return big


def portrait_block(k=4):
    names = list(PORT.PORTRAITS)
    out = Image.new("RGBA", (64 * len(names) + 4 * (len(names) - 1), 64), BG)
    for i, n in enumerate(names):
        a, pal = PORT.render(n, 3)
        tile = Image.new("RGBA", (64, 64), (200, 200, 200, 255))
        tile.alpha_composite(to_rgba(a, pal))
        out.alpha_composite(tile, (i * 68, 0))
    return upscale(out, k)


def stack(blocks, titles, gap=16):
    w = max(b.width for b in blocks)
    h = sum(b.height + 20 for b in blocks) + gap * (len(blocks) - 1)
    out = Image.new("RGBA", (w, h), BG)
    d = ImageDraw.Draw(out)
    y = 0
    for b, t in zip(blocks, titles):
        label(d, (4, y + 4), t)
        out.alpha_composite(b, (0, y + 20))
        y += b.height + 20 + gap
    return out


def euploia_sea():
    """The four headings at GBA size and at 3x, on a wide stretch of sea."""
    rows = ship_rows()
    a = rows[0][1]
    frames = [a[:, i * 64:(i + 1) * 64] for i in (0, 1, 2, 9)]
    slack = rows[1][1]
    frames += [slack[:, i * 64:(i + 1) * 64] for i in (3, 7)]
    water = sea(240, 160)
    spots = [(8, 8), (88, 8), (168, 8), (8, 88), (88, 88), (168, 88)]
    for (x, y), fr in zip(spots, frames):
        water.alpha_composite(to_rgba(fr, SHIP.PAL), (x, y))
    both = Image.new("RGBA", (240 + 8 + 720, 480), BG)
    both.alpha_composite(water, (0, 0))
    both.alpha_composite(upscale(water, 3), (248, 0))
    return both


def ingame(shots):
    files = sorted(glob.glob(os.path.join(shots, "*.png")))
    pick = [f for key in ("ships_down", "ships_left", "crew_down", "olympia_down")
            for f in files if key in f][:4]
    if not pick:
        return None
    out = Image.new("RGBA", (240 * 2 + 4, 160 * 2 + 4), BG)
    for i, f in enumerate(pick):
        out.alpha_composite(Image.open(f).convert("RGBA"), ((i % 2) * 244, (i // 2) * 164))
    return upscale(out, 2)


def main(argv):
    os.makedirs(IMG, exist_ok=True)
    shots = argv[argv.index("--shots") + 1] if "--shots" in argv else os.path.join(ROOT, "build/test_pg_sprites/shots")
    walkers = walker_block()
    contact = stack([ship_block(), walkers, portrait_block()],
                    ["The Euploia over the aethos sea, 2x: sail full, then slack. Frames 0-8, then east (7, 2, 8 flipped)",
                     "Walkers, 4x: face S, N, W; walk S, S, N, N, W, W; then east (flipped). Vanilla Birch first",
                     "Trainer pics, 4x: Achilles, Odysseus, Hippolyta, Atalanta, Ariadne, Olympias"])
    contact.save(os.path.join(IMG, "sprites_contact.png"))
    euploia_sea().save(os.path.join(IMG, "sprites_euploia_sea.png"))
    g = ingame(shots)
    if g is not None:
        g.save(os.path.join(IMG, "sprites_ingame.png"))
    print("wrote", ", ".join(n for n in ("sprites_contact.png", "sprites_euploia_sea.png",
                                         "sprites_ingame.png" if g is not None else "") if n))


if __name__ == "__main__":
    main(sys.argv[1:])
