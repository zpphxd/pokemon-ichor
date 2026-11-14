"""Greek door animations for the aethos tileset (graphics/door_anims/ichor_*).

Usage:
    /usr/bin/python3 tools/ichor/art/doors.py [--write] [--preview DIR]

--write    rewrites graphics/door_anims/ichor_*.png
--preview  writes DIR/doors.png: each door closed, then its three opening
           frames, as the game plays them, at 4x and 1x

aethos keeps General's five animated door ids (design/phase1/TILES_aethos.md).
Every one of them is drawn on the bottom layer in palette 0, so each frame is
built straight from the door's own tiles, in palette indices: the closed door
is exactly the tileset's, and only the doorway changes.

  021  farmhouse    an Aegean-blue wooden door, swinging in on its left hinge
  041  Agora        the striped stall curtain, drawn aside to the right
  061  Asclepeion   the gold-studded Aegean door in its marble frame, swinging in
  1CD  palaestra    the same studded door, between the porch columns
  1DB  theater      blue double doors under the gold mask, both leaves swinging in

The doorway opens on a dark room, with daylight falling on the first floor
tiles inside. Each turning leaf darkens a shade per frame as it turns away
from the light.

Engine layout (src/field_door.c): a 1x2 door animates the door cell and the
cell above it, 8 tiles a frame (16x32); a 1x1 door only the door cell, 4
tiles a frame (16x16). Three frames, stacked vertically. The engine copies 8
tiles per frame either way, so the 1x1 sheets end with 4 blank tiles.
They are registered in sIchorDoorAnimGraphicsTable in src/field_door.c.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from items_lib import ROOT, upscale  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "tools/ichor"))
import render_map as R  # noqa: E402

OUT = os.path.join(ROOT, "graphics/door_anims")

# name -> (metatiles bottom to top, door kind, opening box (x0, y0, x1, y1) in
#          the frame, inclusive)
DOORS = {
    "ichor_farmhouse": dict(mt=[0x021], kind="leaf", box=(4, 3, 11, 14), sound="normal",
                            what="farmhouse door (aethos 021)"),
    "ichor_agora": dict(mt=[0x041, 0x039], kind="curtain", box=(4, 12, 11, 22), sound="sliding",
                        what="Agora curtain (aethos 041)"),
    "ichor_asclepeion": dict(mt=[0x061, 0x059], kind="leaf", box=(5, 13, 11, 23), sound="normal",
                             what="Asclepeion door (aethos 061)"),
    "ichor_palaestra": dict(mt=[0x1CD], kind="leaf", box=(5, 1, 10, 11), sound="normal",
                            what="palaestra door (aethos 1CD)"),
    "ichor_theater": dict(mt=[0x1DB], kind="double", box=(3, 8, 12, 15), sound="normal",
                          what="theater doors (aethos 1DB)"),
}


def load_aethos():
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R.Tileset(R.resolve_tileset("aethos", syms))


def metatile_indices(ts, mid):
    """16x16 palette-index map of a single-layer, palette-0 metatile."""
    e = [int(v) for v in ts.metatiles[mid]]
    assert all(v >> 12 == 0 for v in e[:4]), f"{mid:03X}: door art must be palette 0"
    assert all(v & 0x3FF == 0 for v in e[4:]), f"{mid:03X}: door art must be one layer"
    out = np.zeros((16, 16), np.int32)
    for k in range(4):
        v = e[k]
        t = ts.tiles[v & 0x3FF].copy()
        if v >> 10 & 1:
            t = t[:, ::-1]
        if v >> 11 & 1:
            t = t[::-1, :]
        y, x = (k // 2) * 8, (k % 2) * 8
        out[y:y + 8, x:x + 8] = t
    return out


def closed_frame(ts, mts):
    """The door cell (and the cell above, for 1x2) stacked top to bottom."""
    return np.vstack([metatile_indices(ts, m) for m in reversed(mts)])


class Pal:
    def __init__(self, colors):
        self.colors = colors
        self.by = {tuple(c): i for i, c in enumerate(colors) if i}

    def __getitem__(self, rgb):
        return self.by[tuple(rgb)]


INK = (32, 24, 24)
AE_D, AE_M, AE_L = (24, 56, 120), (48, 104, 176), (112, 168, 224)
SG_D, SG_L = (200, 144, 40), (240, 192, 64)
TC_D, TC_M = (120, 48, 24), (184, 88, 48)
MB_D, MB_5 = (168, 160, 152), (128, 120, 112)


def darken_map(p):
    """One shade darker, within palette 0, for a leaf turning from the light."""
    return {p[AE_L]: p[AE_M], p[AE_M]: p[AE_D], p[AE_D]: p[INK], p[SG_L]: p[SG_D], p[SG_D]: p[TC_D],
            p[TC_M]: p[TC_D], p[MB_D]: p[MB_5]}


def room(frame, box, p):
    """Fill the doorway with the dark room: ink, and daylight on the floor
    just inside the threshold."""
    x0, y0, x1, y1 = box
    frame[y0:y1 + 1, x0:x1 + 1] = p[INK]
    frame[y1, x0:x1 + 1] = p[TC_D]
    frame[y1 - 1, x0 + 1:x1 + 1] = p[TC_D]
    frame[y1, x0 + 2:x1] = p[TC_M]


def swing(frame, closed, box, frac, shades, p, hinge="left", edge=True):
    """Draw the leaf, closed in box, turned in on its hinge so that its face
    shows frac of its width. The free edge recedes, so the leaf's top drops
    and its bottom rises toward that edge."""
    x0, y0, x1, y1 = box
    W = x1 - x0 + 1
    w = max(1, int(round(W * frac)))
    leaf = closed[y0:y1 + 1, x0:x1 + 1]
    dm = darken_map(p)
    for i in range(w):
        # column i of the visible face, counted from the hinge
        src = int(i * W / w)
        if hinge == "right":
            sx, dx = W - 1 - src, x1 - i
        else:
            sx, dx = src, x0 + i
        drop = int(round((i / max(w - 1, 1)) * (1 - frac) * 2.2))
        col = leaf[:, sx].copy()
        for _ in range(shades):
            col = np.array([dm.get(int(c), int(c)) for c in col])
        h = len(col)
        top, bot = y0 + drop, y1 - (drop // 2)
        # resample the column into its shortened height
        n = bot - top + 1
        idx = (np.arange(n) * h / n).astype(int)
        frame[top:bot + 1, dx] = col[idx]
        frame[top, dx] = p[INK]
    if edge and w < W:
        # the leaf's thickness at its free edge
        ex = x0 + w if hinge == "left" else x1 - w
        frame[y0 + 1:y1, ex] = p[AE_D] if shades < 2 else p[INK]


def leaf_frames(closed, box, p, double=False):
    frames = []
    for frac, shades in ((0.7, 0), (0.4, 1), (0.14, 2)):
        f = closed.copy()
        room(f, box, p)
        if double:
            x0, y0, x1, y1 = box
            mid = (x0 + x1) // 2
            swing(f, closed, (x0, y0, mid, y1), frac, shades, p, "left")
            swing(f, closed, (mid + 1, y0, x1, y1), frac, shades, p, "right")
        else:
            swing(f, closed, box, frac, shades, p, "left")
        frames.append(f)
    return frames


def curtain_frames(closed, box, p):
    """The curtain gathers to the right: its stripes bunch up, and its hem is
    lifted toward the tie, so less of it hangs at the bottom."""
    x0, y0, x1, y1 = box
    W = x1 - x0 + 1
    cur = closed[y0:y1 + 1, x0:x1 + 1]
    frames = []
    for top_w, bot_w in ((6, 4), (4, 2), (2, 1)):
        f = closed.copy()
        room(f, box, p)
        H = y1 - y0 + 1
        for j in range(H):
            w = int(round(top_w + (bot_w - top_w) * j / (H - 1)))
            for i in range(w):
                src = W - w + int(i * w / w) if w == W else int(i * W / w)
                f[y0 + j, x1 - w + 1 + i] = cur[j, min(src, W - 1)]
            # a dark fold where the cloth turns at the gather
            f[y0 + j, x1 - w + 1] = p[AE_D] if f[y0 + j, x1 - w + 1] != p[INK] else p[INK]
        frames.append(f)
    return frames


def build(ts):
    p = Pal([tuple(int(v) & 0xF8 for v in c) for c in ts.pals[0]])
    out = {}
    for name, d in DOORS.items():
        closed = closed_frame(ts, d["mt"])
        if d["kind"] == "curtain":
            frames = curtain_frames(closed, d["box"], p)
        else:
            frames = leaf_frames(closed, d["box"], p, double=d["kind"] == "double")
        out[name] = (closed, frames)
    return p, out


def write(ts):
    p, out = build(ts)
    colors = [tuple(c) for c in p.colors]
    flat = [v for c in colors for v in c]
    for name, (closed, frames) in out.items():
        sheet = np.vstack(frames).astype(np.uint8)
        if sheet.shape[0] == 48:
            # The engine copies 8 tiles a frame whatever the door's size, so a
            # 1x1 sheet gets 4 blank tiles after its last frame to copy from.
            sheet = np.vstack([sheet, np.zeros((16, 16), np.uint8)])
        im = Image.fromarray(sheet, "P")
        im.putpalette(flat)
        im.save(os.path.join(OUT, name + ".png"), bits=4)
        print(f"doors.py: wrote graphics/door_anims/{name}.png {sheet.shape[1]}x{sheet.shape[0]}")


def preview(ts, outdir):
    os.makedirs(outdir, exist_ok=True)
    p, out = build(ts)
    cols = np.array(p.colors, np.uint8)
    k = 4
    names = list(out)
    cell_h = 32 * k + 40
    sheet = Image.new("RGB", (5 * (16 * k + 10) + 16 * 6 + 30, len(names) * cell_h + 10), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    for r, name in enumerate(names):
        closed, frames = out[name]
        y = 10 + r * cell_h
        d.text((10, y), DOORS[name]["what"] + "  closed | open 1 | open 2 | open (the close plays back)",
               fill=(248, 240, 216))
        seq = [closed] + frames
        for i, f in enumerate(seq):
            img = cols[f]
            pad = np.zeros((32, 16, 3), np.uint8) + np.array((64, 40, 32), np.uint8)
            pad[32 - img.shape[0]:] = img
            sheet.paste(Image.fromarray(upscale(pad, k)), (10 + i * (16 * k + 10), y + 14))
            sheet.paste(Image.fromarray(pad), (10 + 5 * (16 * k + 10) + i * 20, y + 14))
    sheet.save(os.path.join(outdir, "doors.png"))
    print(f"doors.py: preview in {outdir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--preview")
    args = ap.parse_args()
    ts = load_aethos()
    if args.write:
        write(ts)
    if args.preview:
        preview(ts, args.preview)


if __name__ == "__main__":
    main()
