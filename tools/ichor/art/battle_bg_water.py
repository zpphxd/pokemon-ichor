#!/usr/bin/env python3
"""Battle background: the open Aegean (water: fishing and surfing at sea).

Deep blue sea to the horizon under a high sun. The sun lays a road of glitter
across the water; wave crests grow toward the viewer. On the horizon a trireme
under a square sail pulls past, its oars out. The platforms are rings of
lighter water spreading round each battler, edged in foam.

Writes, in graphics/battle_environment/water/:
  tiles.png, map.bin, palette.pal   BATTLE_ENVIRONMENT_WATER
  anim_tiles.png, anim_map.bin      the wave that rolls across at the start,
                                    curling like the Greek wave scroll
  kyogre.pal                        BATTLE_ENVIRONMENT_KYOGRE (a Hoenn legend
                                    the slice never reaches): the same sea in
                                    a storm, so its colors still fit the tiles

Usage: python3 tools/ichor/art/battle_bg_water.py [--preview DIR]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle_bg_lib import (ENV, OPP_PLATFORM, PLR_PLATFORM, STRIP, Canvas, Pal,  # noqa: E402
                           build_anim, build_bg, check_grid, compose, gradient,
                           hash2, in_ellipse, platform, preview_canvas)

OUT = ENV / "water"

# --- Palette ----------------------------------------------------------------
#   0: sky, clouds, sun, the trireme, the far sea
#   1: the sea, its glitter and the water rings
#   2: (spare: the near sea again, so wave tiles can borrow it)
COLORS = {
    "sky1": (112, 168, 224), "sky2": (144, 192, 232), "sky3": (176, 216, 240),
    "sky4": (208, 232, 248), "cloud": (248, 248, 240), "cloud_sh": (192, 208, 232),
    "sun_halo": (240, 240, 216),
    "deep": (24, 56, 120), "sea": (48, 104, 176), "sea_md": (80, 136, 200),
    "sea_lt": (112, 168, 224), "shallow": (152, 200, 232), "foam": (248, 248, 240),
    "gold": (240, 192, 64), "gold_lt": (248, 232, 160),
    "hull": (56, 40, 32), "sail_sh": (216, 208, 192), "clay": (184, 88, 48),
    "deep_dk": (16, 40, 96),
}
SUBS = [
    ["sky1", "sky2", "sky3", "sky4", "cloud", "cloud_sh", "sun_halo", "deep", "sea",
     "sea_md", "hull", "sail_sh", "clay", "gold_lt"],
    ["deep_dk", "deep", "sea", "sea_md", "sea_lt", "shallow", "foam", "gold", "gold_lt", "hull"],
    ["deep_dk", "deep", "sea", "sea_md", "sea_lt", "shallow", "foam"],
]
PAL = Pal(COLORS, SUBS)

# BATTLE_ENVIRONMENT_KYOGRE uses these tiles: a storm over the same sea.
STORM = PAL.variant(
    sky1=(56, 64, 88), sky2=(72, 80, 104), sky3=(88, 96, 120), sky4=(104, 112, 136),
    cloud=(136, 144, 160), cloud_sh=(96, 104, 128), sun_halo=(120, 128, 144),
    deep=(16, 32, 64), sea=(32, 56, 104), sea_md=(48, 80, 128), sea_lt=(72, 104, 152),
    shallow=(104, 136, 176), foam=(200, 208, 216), gold=(136, 144, 168),
    gold_lt=(168, 176, 192), deep_dk=(8, 24, 48), sail_sh=(144, 144, 152),
)

HORIZON = 40

# --- Motifs -----------------------------------------------------------------
CLOUD = check_grid([
    "         ooooo          ",
    "    ooooooooooooo oooo  ",
    " ooooooooooooooooooooooo",
    "ooooooooooooooooooooooos",
    "ssssooooooosssssoosssss ",
    "   ssssssss    ss       ",
])
CLOUD_KEY = {"o": "cloud", "s": "cloud_sh"}

# A trireme on the horizon, sailing left: the stern post curls up behind,
# the ram juts at the bow (right), a square sail with a clay stripe on one
# mast, and the oar banks dip into the sea.
TRIREME = check_grid([
    "               :              ",
    "          SSSSSSSSSSS         ",
    "          SSSSSSSSSSS         ",
    " hh       CCCCCCCCCCC         ",
    "h  h      SSSSSSSSSSs         ",
    "h   h     SSSSSSSSSSs         ",
    " h  h     SSSSSSSSSSs     h   ",
    "    hh         :         hh   ",
    "     hhhhhhhhhhhhhhhhhhhhhhhh ",
    "      hhhhhhhhhhhhhhhhhhhhhhhhh",
    "       / / / / / / / / / /    ",
])
TRIREME_KEY = {"S": "cloud", "s": "sail_sh", "C": "clay", "h": "hull", ":": "hull", "/": "hull"}


def sun(c, cx, cy):
    """A high sun at the top of the screen: a white disc in a pale halo."""
    for y in range(0, cy + 16):
        for x in range(cx - 18, cx + 19):
            d = math.hypot(x + 0.5 - cx, (y + 0.5 - cy) * 1.1)
            if d < 7:
                c.set(x, y, "cloud")
            elif d < 10:
                c.set(x, y, "sun_halo")
            elif d < 14 and (x + y) % 2 == 0:
                c.set(x, y, "sun_halo")


def sea(c):
    """The sea from the horizon down: one blue, textured by wavelets in bands
    that repeat every 32 px and grow toward the viewer. A wavelet is a light
    crest dash; its trough is a shorter dark dash below and to the right, so
    the water reads as moving, not as rows of buttons."""
    for y in range(HORIZON, 240):
        c.hline(0, STRIP, y, "sea")
    c.hline(0, STRIP, HORIZON, "deep_dk")
    c.hline(0, STRIP, HORIZON + 1, "deep")
    for x in range(STRIP):
        if x % 2:
            c.set(x, HORIZON + 2, "deep")
    # (row, [(x, crest width)], crest color, highlight)
    bands = [
        (HORIZON + 4, [(3, 2), (13, 3), (24, 2)], "sea_md", None),
        (HORIZON + 8, [(8, 3), (19, 4), (29, 2)], "sea_md", None),
        (HORIZON + 12, [(1, 4), (15, 3), (24, 5)], "sea_lt", None),
        (HORIZON + 17, [(9, 5), (22, 4)], "sea_lt", None),
        (HORIZON + 23, [(2, 6), (16, 4), (27, 3)], "sea_lt", None),
        (HORIZON + 30, [(10, 7), (24, 5)], "sea_lt", "shallow"),
        (HORIZON + 38, [(3, 8), (19, 6)], "sea_lt", "shallow"),
        (HORIZON + 47, [(12, 9), (27, 4)], "sea_lt", "foam"),
        (HORIZON + 57, [(4, 10), (21, 6)], "sea_lt", "foam"),
        (HORIZON + 67, [(14, 10), (29, 5)], "sea_lt", "foam"),
    ]
    k = 0
    while bands[-1][0] + 10 < 236:
        last = bands[-2 if k % 2 == 0 else -1]
        bands.append((bands[-1][0] + 10, last[1], "sea_lt", "foam"))
        k += 1
    for (y0, crests, col, hi) in bands:
        for x0 in range(0, STRIP, 32):
            for (dx, w) in crests:
                x = x0 + dx
                c.hline(x, x + w, y0, col)
                if hi and w >= 6:
                    c.hline(x + 2, x + w - 2, y0 - 1, hi)
                if w >= 3:
                    tw = max(1, w // 2)
                    c.hline(x + w - tw + 1, x + w + 1, y0 + 1, "deep")


def glitter(c, cx):
    """The sun's road on the water: short bright streaks lying on the
    wavelets, thick under the sun, spreading and thinning toward the viewer."""
    for y in range(HORIZON + 2, 112):
        d = y - HORIZON
        half = 4 + d * 0.5
        for x in range(int(cx - half), int(cx + half) + 1):
            r = hash2(x, y)
            near = abs(x - cx) / half
            if r % (3 + d // 5 + int(near * 6)) == 0 and r % 5 < 3:
                w = 1 + (r >> 7) % (2 + d // 20)
                for i in range(w):
                    c.set(x + i, y, "gold_lt" if i == 0 or (r >> 11) % 3 else "foam")
                if d > 24 and (r >> 13) % 4 == 0:
                    c.set(x + w, y, "gold")


def strip():
    c = Canvas(STRIP, 256)
    gradient(c, 0, [("sky1", 12), ("sky2", 10), ("sky3", 9), ("sky4", HORIZON - 31)])
    c.rect(0, 240, STRIP, 256, "sky1")
    sun(c, 224, 2)
    c.stamp(CLOUD, CLOUD_KEY, 60, 4)
    c.stamp(CLOUD, CLOUD_KEY, 132, 20)
    sea(c)
    glitter(c, 224)
    c.stamp(TRIREME, TRIREME_KEY, 108, HORIZON - 9)
    return c


# --- Platforms ----------------------------------------------------------------
def ring_top(x, y, u, v):
    """Rings of lighter water spreading round the battler, foam at the edge.
    Rings follow the platform so both share tiles."""
    r = math.sqrt(u * u + v * v)
    lx, ly = int(round(u * 62)), int(round(v * 13))
    if r > 0.93:
        return "foam" if (lx + 2 * ly) % 5 else "shallow"
    if r > 0.86:
        return "sea_lt"
    ring = int(r * 7)
    if ring in (5,) and (lx * 3 + ly) % 4:
        return "shallow"
    if ring == 3 and (lx + ly) % 3:
        return "sea_lt"
    lit = -(0.4 * u + 0.8 * v)
    if r < 0.32:
        return "shallow" if (lit > 0.1 or (lx + ly) % 2) else "sea_lt"
    if lit > 0.5 and (lx + ly) % 2 == 0:
        return "shallow"
    return "sea_md" if ring in (4, 6) else "sea_lt"


def ring_side(x, y, t, u):
    return "foam" if t == 0 and (x % 3) else ("sea" if t < 2 else "deep")


def platforms():
    p = Canvas(STRIP, 256, wrap=False)
    for (cx, cy) in (OPP_PLATFORM, PLR_PLATFORM):
        platform(p, cx, cy, 62, 13, 2, ring_top, ring_side)
    return p


def clear_glitter(s, plat):
    """Keep the sea plain in tiles the platforms touch (left block), so the
    two water rings share their edge tiles."""
    for ty in range(32):
        for tx in range(32):
            if any(plat.px[ty * 8 + j][tx * 8 + i] is not None for j in range(8) for i in range(8)):
                for j in range(8):
                    for i in range(8):
                        y, x = ty * 8 + j, tx * 8 + i
                        if plat.px[y][x] is None and s.px[y][x] in ("gold", "gold_lt"):
                            plat.px[y][x] = "sea_md" if y < HORIZON + 36 else "sea"


# --- The wave that rolls across at the start ----------------------------------
def wave():
    """BG1 overlay (blended, bobbing, scrolling right): a running wave whose
    crests curl into spirals, the Greek wave scroll drawn in foam."""
    c = Canvas(256, 256, wrap=True)
    base = 110
    unit = 64
    for x0 in range(0, 256, unit):
        sx, sy, R = x0 + 40, base - 20, 13        # spiral center and radius
        body = set()
        for x in range(x0, x0 + unit):
            # the slope rises from the trough to the top of the curl
            t = (x - x0) / 40
            top = base - 6 - round(26 * (t ** 1.6)) if t <= 1 else None
            if top is not None:
                for y in range(top, base + 1):
                    body.add((x, y))
        for y in range(sy - R, base + 1):
            for x in range(sx - R, sx + R + 1):
                if math.hypot(x + 0.5 - sx, y + 0.5 - sy) <= R or y >= sy:
                    if x < x0 + unit:
                        body.add((x, y))
        for (x, y) in body:
            d = base - y
            n = "sea" if d < 6 else ("sea_md" if d < 14 else "sea_lt")
            c.set(x, y, n)
        # the curl: a foam spiral winding in from the crest
        for i in range(260):
            th = i / 260 * 2.6 * math.pi
            r = R - th * (R - 2) / (2.6 * math.pi)
            x = sx + r * math.cos(th - math.pi / 2)
            y = sy + r * math.sin(th - math.pi / 2)
            c.set(round(x), round(y), "foam")
        # foam along the front of the slope
        for x in range(x0, sx):
            ys = [y for (bx, y) in body if bx == x]
            if ys:
                c.set(x, min(ys), "foam")
                c.set(x, min(ys) + 1, "shallow")
    for k in range(40):                         # spray
        r = hash2(k * 29, 5)
        c.set((k * 13 + r % 7) % 256, base - 36 - (r >> 3) % 14, "foam")
    for y in range(base - 4, base + 1):
        for x in range(256):
            if c.get(x, y) is None:
                c.set(x, y, "sea")
    # the intro scrolls this layer leftward, so turn the waves to curl the
    # way they travel
    m = Canvas(256, 256, wrap=True)
    for y in range(256):
        for x in range(256):
            m.px[y][255 - x] = c.px[y][x]
    return m


def main():
    s = strip()
    plat = platforms()
    clear_glitter(s, plat)
    full = compose(s, plat)
    if "--preview" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--preview") + 1])
        preview_canvas(full, PAL, out / "water_canvas.png")
        preview_canvas(wave(), PAL, out / "water_wave.png")
    build_bg(full, PAL, OUT)
    PAL.write_jasc(OUT / "palette.pal")
    STORM.write_jasc(OUT / "kyogre.pal")
    build_anim(wave(), PAL, OUT)


if __name__ == "__main__":
    main()
