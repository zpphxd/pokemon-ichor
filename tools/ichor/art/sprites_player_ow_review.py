"""Review images for Theo's and Ianthe's overworld sprites.

Usage:
    python3 tools/ichor/art/sprites_player_ow_review.py shots SHOTS_DIR OUT.png [--title TEXT]
    python3 tools/ichor/art/sprites_player_ow_review.py rom OUT.png [--rom pokeemerald.gba]

shots: crops tools/ichor/tests/player_ow_walk.lua's screenshots into a 3x
    filmstrip. Each row is one move from the walk test (walk up, down, left,
    right, then run the same way holding B); each cell is the player 4 frames
    apart while the key is held, so every walk and run frame appears mid-step.
    The first cell is the player standing before the test moves.

rom: decodes the player's sheets and palettes straight out of the built ROM,
    at the symbols the engine loads (gObjectEventPic_Brendan*, ..._May*,
    gObjectEventPal_Brendan, gObjectEventPal_May), and draws every frame at 3x
    with the east-facing (mirrored) frames the animations use. This checks the
    fishing and field-move sheets, which the walk test cannot reach from the
    bedroom.
"""
import argparse
import glob
import os
import re

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# The player's 16x32 frame sits at (112, 56) on the 240x160 screen; the crop
# adds a margin for the shadow.
BOX = (104, 52, 136, 92)
SCALE = 3
BG = (40, 40, 48)


def filmstrip(args):
    rows = {}
    for path in sorted(glob.glob(os.path.join(args.shots, "*.png"))):
        m = re.match(r"(\d\d)_(\w+?)_(\d{3})\.png$", os.path.basename(path))
        if m:
            rows.setdefault((m.group(1), m.group(2)), []).append(path)
    stand = os.path.join(args.shots, "00_stand.png")

    cw, ch = (BOX[2] - BOX[0]) * SCALE, (BOX[3] - BOX[1]) * SCALE
    label_w, pad, top = 90, 2, 18 if args.title else 0
    ncol = max(len(v[::2]) for v in rows.values()) + 1
    out = Image.new("RGB", (label_w + ncol * (cw + pad), top + len(rows) * (ch + pad)), BG)
    d = ImageDraw.Draw(out)
    if args.title:
        d.text((4, 3), args.title, fill=(255, 255, 255))

    def cell(path, x, y):
        im = Image.open(path).convert("RGB").crop(BOX)
        out.paste(im.resize((cw, ch), Image.NEAREST), (x, y))

    for r, ((num, name), paths) in enumerate(sorted(rows.items())):
        y = top + r * (ch + pad)
        d.text((4, y + ch // 2 - 5), name.replace("_", " "), fill=(255, 255, 255))
        x = label_w
        if r == 0 and os.path.exists(stand):
            cell(stand, x, y)
        x += cw + pad
        for p in paths[::2]:
            cell(p, x, y)
            x += cw + pad
    out.save(args.out)


# (symbol suffix, frames, frame w, frame h, label, frames to also show mirrored)
SHEETS = [
    ("NormalRunning", 18, 16, 32, "walking 0-8, running 9-17", [2, 7, 8, 11, 16, 17]),
    ("Fishing", 12, 32, 32, "fishing: west 0-3, north 4-7, south 8-11", [0, 1, 2, 3]),
    ("FieldMove", 5, 32, 32, "field move", []),
]


def symbols(path):
    out = {}
    with open(path) as fh:
        for line in fh:
            m = re.match(r"^\s+0x([0-9a-f]+)\s+(gObjectEvent(?:Pic|Pal)_(?:Brendan|May)\w*)\s*$", line)
            if m:
                out[m.group(2)] = int(m.group(1), 16)
    return out


def decode_frames(rom, addr, n, fw, fh):
    tw, th = fw // 8, fh // 8
    off = addr - 0x08000000
    frames = []
    for f in range(n):
        im = Image.new("P", (fw, fh))
        for t in range(tw * th):
            base = off + (f * tw * th + t) * 32
            tx, ty = (t % tw) * 8, (t // tw) * 8
            for i in range(32):
                b = rom[base + i]
                x, y = (i % 4) * 2, i // 4
                im.putpixel((tx + x, ty + y), b & 15)
                im.putpixel((tx + x + 1, ty + y), b >> 4)
        frames.append(im)
    return frames


def decode_pal(rom, addr):
    off = addr - 0x08000000
    flat = []
    for i in range(16):
        c = rom[off + 2 * i] | rom[off + 2 * i + 1] << 8
        flat += [(c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3]
    return flat


def rom_check(args):
    rom = open(args.rom, "rb").read()
    syms = symbols(os.path.splitext(args.rom)[0] + ".map")
    rows = []
    for who, name in (("Brendan", "Theo"), ("May", "Ianthe")):
        pal = decode_pal(rom, syms["gObjectEventPal_" + who])
        for suffix, n, fw, fh, label, mirror in SHEETS:
            frames = decode_frames(rom, syms["gObjectEventPic_" + who + suffix], n, fw, fh)
            cells = []
            for im in frames:
                im.putpalette(pal)
                im.info["transparency"] = 0
                cells.append(im.convert("RGBA"))
            cells += [c.transpose(Image.FLIP_LEFT_RIGHT) for c in (cells[i] for i in mirror)]
            label = f"{name}: {label}" + (", then mirrored for east" if mirror else "")
            rows.append((label, cells, len(frames)))

    pad, lab = 4, 14
    bg = (168, 200, 120, 255)
    width = max(sum(c.width * SCALE + pad for c in cells) + 6 for _, cells, _ in rows)
    height = sum(lab + 32 * SCALE + pad for _ in rows)
    out = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(out)
    y = 0
    for label, cells, nreal in rows:
        d.text((4, y + 1), label, fill=(255, 255, 255))
        y += lab
        x = 4
        for i, c in enumerate(cells):
            if i == nreal:
                x += 6
            tile = Image.new("RGBA", c.size, bg)
            tile.alpha_composite(c)
            out.paste(tile.resize((c.width * SCALE, c.height * SCALE), Image.NEAREST), (x, y))
            x += c.width * SCALE + pad
        y += 32 * SCALE + pad
    out.save(args.out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("shots")
    s.add_argument("shots")
    s.add_argument("out")
    s.add_argument("--title", default="")
    r = sub.add_parser("rom")
    r.add_argument("out")
    r.add_argument("--rom", default=os.path.join(ROOT, "pokeemerald.gba"))
    args = ap.parse_args()
    (filmstrip if args.cmd == "shots" else rom_check)(args)


if __name__ == "__main__":
    main()
