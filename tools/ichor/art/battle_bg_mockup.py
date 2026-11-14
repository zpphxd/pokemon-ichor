#!/usr/bin/env python3
"""Battle background mock-ups, rendered from the *built* files.

Reads graphics/battle_environment/<dir>/{tiles.png,map.bin,<pal>} exactly as
the GBA draws them (lib.render_map), then composes a 240x160 battle view: the
BG3 scene, an opponent front pic on the far platform, a back pic on the near
platform and the real battle text box (graphics/battle_interface). It also
renders an intro-slide frame (top half from the right, bottom half from the
left, as the scanline effect does) and the whole 512x256 map with the screen
marked, to check that the strip wraps.

Usage: python3 tools/ichor/art/battle_bg_mockup.py [name ...]
Writes design/phase1/img/battle_bg_<name>.png at 3x.
"""
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle_bg_lib import ENV, ROOT, read_jasc, render_map  # noqa: E402

IMG = ROOT / "design/phase1/img"
SCALE = 3

# name -> (tiles dir, palette file, anim dir, front pic, back pic)
VIEWS = {
    "grass":    ("tall_grass", "tall_grass/palette.pal", "pokemon/piplup", "pokemon/cyndaquil"),
    "plain":    ("building", "plain/palette.pal", "trainers/kleon", "pokemon/snivy"),
    "sand":     ("sand", "sand/palette.pal", "pokemon/cyndaquil", "pokemon/piplup"),
    "water":    ("water", "water/palette.pal", "pokemon/piplup", "pokemon/snivy"),
    "building": ("building", "building/palette.pal", "trainers/hierophant_ione", "pokemon/cyndaquil"),
    "gym":      ("building", "building/gym.pal", "pokemon/snivy", "pokemon/piplup"),
    "leader":   ("building", "building/leader.pal", "trainers/hierophant_ione", "pokemon/snivy"),
    "frontier": ("building", "stadium/battle_frontier.pal", "pokemon/cyndaquil", "pokemon/piplup"),
}


def gbapal(path, n):
    data = Path(path).read_bytes()
    out = []
    for i in range(n):
        v = struct.unpack_from("<H", data, i * 2)[0]
        out.append(((v & 31) << 3, (v >> 5 & 31) << 3, (v >> 10 & 31) << 3))
    return out


def textbox():
    d = ROOT / "graphics/battle_interface"
    pal = gbapal(d / "textbox.gbapal", 32)
    im = render_map(d / "textbox.png", d / "textbox_map.bin", pal, 32, 20, palbase=0)
    return im


def pic(png, pal=None):
    """First 64x64 frame of an indexed pic as RGBA; index 0 is transparent.
    pal: a JASC file (Pokemon) or None to use the PNG's own palette (trainers)."""
    src = Image.open(png)
    p = read_jasc(pal) if pal else [tuple(src.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    px = src.load()
    im = Image.new("RGBA", (64, 64))
    o = im.load()
    for y in range(64):
        for x in range(64):
            i = px[x, y] % 16
            if i:
                o[x, y] = tuple(p[i]) + (255,)
    return im


def front(name):
    if name.startswith("trainers/"):
        return pic(ROOT / f"graphics/trainers/front_pics/{name.split('/')[1]}.png")
    return pic(ROOT / f"graphics/{name}/anim_front.png", ROOT / f"graphics/{name}/normal.pal")


def back(name):
    return pic(ROOT / f"graphics/{name}/back.png", ROOT / f"graphics/{name}/normal.pal")


def bottom(im):
    a = im.getchannel("A").load()
    for y in range(63, -1, -1):
        if any(a[x, y] for x in range(64)):
            return y
    return 63


def view(bg, fpic, bpic, shift=0):
    """240x160: BG3 scrolled for the intro slide by `shift` (0 = settled)."""
    v = Image.new("RGBA", (240, 160))
    top = bg.crop((0, 0, 512, 80))
    bot = bg.crop((0, 80, 512, 160))
    for half, y, s in ((top, 0, shift), (bot, 80, -shift)):
        s %= 512
        strip = Image.new("RGBA", (1024, 80))
        strip.paste(half, (0, 0))
        strip.paste(half, (512, 0))
        v.paste(strip.crop((s, 0, s + 240, 80)), (0, y))
    if shift == 0:
        f = fpic
        v.alpha_composite(f, (144, 72 - bottom(f)))
        v.alpha_composite(bpic, (40, 48))
    v.alpha_composite(textbox().crop((0, 0, 240, 160)), (0, 0))
    return v


def mockup(name):
    tdir, palfile, fname, bname = VIEWS[name]
    pal = read_jasc(ENV / palfile)
    d = ENV / tdir
    bg = render_map(d / "tiles.png", d / "map.bin", pal, 64, 32)
    fpic, bpic = front(fname), back(bname)
    settled = view(bg, fpic, bpic)
    slide = view(bg, fpic, bpic, shift=96)
    pad = 8
    W = 240 * 2 + pad * 3
    fw = W - pad * 2
    H = pad + 160 + pad + fw // 2 + pad
    sheet = Image.new("RGBA", (W, H), (32, 24, 24, 255))
    sheet.alpha_composite(settled, (pad, pad))
    sheet.alpha_composite(slide, (240 + pad * 2, pad))
    # the whole map, screen marked (left block, above the text box)
    full = bg.resize((fw, fw // 2), Image.NEAREST)
    dr = ImageDraw.Draw(full)
    k = fw / 512
    dr.rectangle((0, 0, round(240 * k) - 1, round(112 * k) - 1), outline=(255, 0, 255, 255))
    sheet.alpha_composite(full, (pad, 160 + pad * 2))
    out = sheet.resize((sheet.width * SCALE, sheet.height * SCALE), Image.NEAREST).convert("RGB")
    path = IMG / f"battle_bg_{name}.png"
    out.save(path)
    print(f"wrote {path.relative_to(ROOT)}")
    return path


if __name__ == "__main__":
    for n in sys.argv[1:] or list(VIEWS):
        mockup(n)
