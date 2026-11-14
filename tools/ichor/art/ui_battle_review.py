#!/usr/bin/env python3
"""Review sheets for the pottery battle interface (design/phase1/UI_battle.md).

  parts      every redrawn piece at 4x, drawn from the built PNGs
  compare    before/after rows from two capture folders of 240x160 shots
  strip      a row of frames from one capture folder (the transitions)

Usage:
  python3 tools/ichor/art/ui_battle_review.py parts
  python3 tools/ichor/art/ui_battle_review.py compare BEFORE AFTER OUT label=path ...
  python3 tools/ichor/art/ui_battle_review.py strip DIR OUT f1 f2 ...

The captures come from a headless run of a battle test patch (see the doc).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from ui_battle import STATUS_COLORS, STATUS_ORDER
from ui_battle_lib import BI, BT, IMG, ROOT

BG = (60, 52, 48)
LABEL = (240, 216, 160)


def png_rgba(path, recolor=None):
    im = Image.open(path)
    pal = im.getpalette()[:48]
    pal = [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]
    if recolor:
        for i, c in recolor.items():
            pal[i] = c
    out = Image.new("RGBA", im.size)
    src = im.load()
    dst = out.load()
    for y in range(im.height):
        for x in range(im.width):
            v = src[x, y]
            dst[x, y] = (0, 0, 0, 0) if v == 0 else pal[v] + (255,)
    return out


def scaled(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def parts():
    k = 4
    items = []

    def add(label, im):
        items.append((label, scaled(im, k)))

    for n in ("healthbox_singles_player", "healthbox_singles_opponent",
              "healthbox_doubles_player", "healthbox_doubles_opponent"):
        im = png_rgba(BI / f"{n}.png")
        add(n, im.crop(im.getbbox()))
    # The bar sprite as the game assembles it: label, then six 8 px slices.
    bar = png_rgba(BI / "hpbar.png")
    anim = png_rgba(BI / "hpbar_anim.png")
    slices = {"green": (bar, 24), "yellow": (anim, 0), "red": (anim, 72)}
    row = Image.new("RGBA", (3 * 72, 8))
    for i, (color, pixels) in enumerate((("green", 48), ("yellow", 18), ("red", 7))):
        src, x0 = slices[color]
        row.paste(bar.crop((8, 0, 24, 8)), (i * 72, 0))
        for t in range(6):
            n = max(0, min(8, pixels - 8 * t))
            row.paste(src.crop((x0 + 8 * n, 0, x0 + 8 * n + 8, 8)), (i * 72 + 16 + 8 * t, 0))
    add("hp bar: healthy, caution, danger", row)
    add("expbar (0..8 px)", png_rgba(BI / "expbar.png"))
    badges = Image.new("RGBA", (24 * 6 + 10, 8))
    for i, name in enumerate(STATUS_ORDER):
        color = STATUS_COLORS.get(name, STATUS_COLORS["FRZ"])
        im = png_rgba(BI / "status.png", {12: color})
        badges.paste(im.crop((0, i * 8, 24, i * 8 + 8)), (i * 26, 0))
    add("status badges", badges)
    add("party tokens: full, empty, fainted, statused", png_rgba(BI / "ball_display.png"))
    add("ground line", png_rgba(BI / "ball_status_bar.png"))
    add("enemy shadows", png_rgba(BI / "enemy_mon_shadows_sized.png"))
    pop = png_rgba(BI / "ability_pop_up.png")
    add("ability pop-up", pop.crop(pop.getbbox()))
    win = Image.new("RGBA", (32 * 3 + 8, 64))
    win.paste(png_rgba(BI / "last_used_ball_r_cycle.png"), (0, 0))
    win.paste(png_rgba(BI / "move_info_window_l.png"), (36, 16))
    add("R and L windows", win)
    trig = png_rgba(BI / "mega_trigger.png")
    both = Image.new("RGBA", (64, 18))
    both.paste(trig.crop((0, 0, 32, 18)), (0, 0))
    both.paste(trig.crop((0, 32, 32, 50)), (32, 0))
    add("Omphalos trigger, dim and lit", both)
    add("textbox tiles: cursor, corner, band, side, field", png_rgba(BI / "textbox.png").crop((0, 0, 56, 8)))
    arrow = png_rgba(ROOT / "graphics/fonts/down_arrow.png").crop((0, 0, 8, 16))
    add("continue arrow", arrow)
    add("transition tiles", png_rgba(BT / "ichor_pottery.png").crop((0, 0, 48, 8)))

    w = max(im.width for _, im in items) + 20
    h = sum(im.height + 26 for _, im in items) + 10
    sheet = Image.new("RGBA", (w, h), BG + (255,))
    dr = ImageDraw.Draw(sheet)
    y = 8
    for label, im in items:
        dr.text((10, y), label, fill=LABEL)
        sheet.alpha_composite(im, (10, y + 14))
        y += im.height + 26
    out = IMG / "ui_battle_parts.png"
    sheet.convert("RGB").save(out)
    print(f"wrote {out.relative_to(ROOT)}")


def compare(before, after, out, pairs, k=2):
    rows = []
    for spec in pairs:
        # label=shot, or label=before_shot:after_shot when the frames differ
        label, rel = spec.split("=", 1)
        rel_b, rel_a = rel.split(":") if ":" in rel else (rel, rel)
        rows.append((label, Image.open(Path(before) / rel_b).convert("RGB"),
                     Image.open(Path(after) / rel_a).convert("RGB")))
    w, h = 240 * k, 160 * k
    sheet = Image.new("RGB", (w * 2 + 30, len(rows) * (h + 22) + 22), BG)
    dr = ImageDraw.Draw(sheet)
    dr.text((10, 4), "before", fill=LABEL)
    dr.text((w + 20, 4), "after", fill=LABEL)
    for i, (label, b, a) in enumerate(rows):
        y = 22 + i * (h + 22)
        dr.text((10, y), label, fill=LABEL)
        sheet.paste(b.resize((w, h), Image.NEAREST), (10, y + 14))
        sheet.paste(a.resize((w, h), Image.NEAREST), (w + 20, y + 14))
    sheet.save(out)
    print(f"wrote {out}")


def strip(folder, out, frames, k=2):
    ims = [Image.open(Path(folder) / f"f{int(f):05d}.png").convert("RGB") for f in frames]
    w, h = 240 * k, 160 * k
    cols = 2
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 10) + 10, rows * (h + 24) + 6), BG)
    dr = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(zip(frames, ims)):
        x, y = 10 + (i % cols) * (w + 10), 6 + (i // cols) * (h + 24)
        dr.text((x, y), f"frame {f}", fill=LABEL)
        sheet.paste(im.resize((w, h), Image.NEAREST), (x, y + 14))
    sheet.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "parts":
        parts()
    elif cmd == "compare":
        compare(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    elif cmd == "strip":
        strip(sys.argv[2], sys.argv[3], sys.argv[4:])
