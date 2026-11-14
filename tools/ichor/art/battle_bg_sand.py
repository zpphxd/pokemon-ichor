#!/usr/bin/env python3
"""Battle background: Akti's shore (sand).

A pale beach runs down to the Aegean. Surf breaks in a lace of foam along a
gently curving shoreline, the sea deepens to the horizon, and on a distant
islet stands a small whitewashed shrine with a blue dome. A fishing boat with
a square sail works the horizon. On the sand: an old amphora, half buried,
shells and pebbles. The platforms are low mounds of sand with rippled tops.

Writes, in graphics/battle_environment/sand/:
  tiles.png, map.bin, palette.pal   BATTLE_ENVIRONMENT_SAND
  anim_tiles.png, anim_map.bin      the surf that washes across at the start

Usage: python3 tools/ichor/art/battle_bg_sand.py [--preview DIR]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle_bg_lib import (ENV, OPP_PLATFORM, PLR_PLATFORM, STRIP, Canvas, Pal,  # noqa: E402
                           build_anim, build_bg, check_grid, compose, gradient,
                           hash2, platform, preview_canvas)

OUT = ENV / "sand"

# --- Palette ----------------------------------------------------------------
#   0: sky, clouds, the far sea, the islet and its shrine, the boat
#   1: the near sea, surf, wet and dry sand, the sand mounds
#   2: the beach and what lies on it
COLORS = {
    "sky1": (112, 168, 224), "sky2": (144, 192, 232), "sky3": (176, 216, 240),
    "sky4": (208, 232, 248), "cloud": (248, 248, 240), "cloud_sh": (192, 208, 232),
    "sea_dk": (24, 56, 120), "sea": (48, 104, 176), "sea_md": (80, 136, 200),
    "sea_lt": (112, 168, 224), "shallow": (152, 200, 232), "foam": (248, 248, 240),
    "rock_dk": (120, 112, 104), "rock_lt": (184, 176, 160), "scrub": (96, 112, 48),
    "wall_sh": (192, 200, 208),
    "wet_dk": (144, 112, 72), "wet": (176, 144, 96),
    "sand_dk": (192, 168, 120), "sand_md": (208, 184, 136), "sand": (224, 208, 168),
    "sand_lt": (232, 224, 192), "sand_hi": (248, 240, 216),
    "shell": (224, 136, 88), "clay_dk": (120, 48, 24), "clay": (184, 88, 48),
    "ink": (32, 24, 24),
}
SUBS = [
    ["sky1", "sky2", "sky3", "sky4", "cloud", "cloud_sh", "sea_dk", "sea", "sea_md",
     "sea_lt", "rock_dk", "rock_lt", "scrub", "wall_sh", "clay"],
    ["sea", "sea_md", "sea_lt", "shallow", "foam", "wet_dk", "wet", "sand_dk",
     "sand_md", "sand", "sand_lt", "sand_hi", "rock_lt", "sea_dk"],
    ["wet_dk", "wet", "sand_dk", "sand_md", "sand", "sand_lt", "sand_hi", "rock_dk",
     "rock_lt", "shell", "foam", "clay_dk", "clay", "ink"],
]
PAL = Pal(COLORS, SUBS)

HORIZON = 40


def shore_y(x):
    """The waterline: a gentle curve that repeats every 256 px."""
    return 57 + round(2.4 * math.sin(2 * math.pi * x / 128) + 1.4 * math.sin(2 * math.pi * x / 64 + 1.0))


# --- Motifs -----------------------------------------------------------------
CLOUD = check_grid([
    "          oooo        ",
    "      oooooooooo ooo  ",
    "  oooooooooooooooooooo",
    "ooooooooooooooooooooos",
    "sssoooooossssooosssss ",
    "   sssssss   ssss     ",
])
LONG_CLOUD = check_grid([
    "        oooooo                ",
    "   ooooooooooooooo  oooooo    ",
    "oooooooooooooooooooooooooooooo",
    "ssssssooooooosssssssssssssssss",
    "    ssssssss                  ",
])
CLOUD_KEY = {"o": "cloud", "s": "cloud_sh"}

# The islet: grey limestone with a little scrub, and a whitewashed shrine with
# a blue dome and a dark door.
ISLET = check_grid([
    "                 BBB                  ",
    "               BBBBBBB                ",
    "              BBBBBBBBB               ",
    "              WWWWWWWWw               ",
    "              WWWWdWWWw               ",
    "              WWWWdWWWw   g           ",
    "          gg rrrrrrrrrrr ggg          ",
    "        ggrrrrrRRRRRRRrrrrrgg         ",
    "     ggrrrrRRRRRRRRRRRRRRrrrrrgg      ",
    " ~~rrrrRRRRRRRRRRRRRRRRRRRRRRRrrrrr~~ ",
])
ISLET_KEY = {"B": "sea_dk", "W": "cloud", "w": "wall_sh", "d": "rock_dk", "r": "rock_dk",
             "R": "rock_lt", "g": "scrub", "~": "sea_lt"}

# A fishing boat with a square sail on the horizon.
BOAT = check_grid([
    "    m     ",
    "  SSSSS   ",
    "  SSSSS   ",
    "  SCSSS   ",
    "  SSSSS   ",
    "    m     ",
    "kkkkkkkkk ",
    " kkkkkkk  ",
])
BOAT_KEY = {"m": "rock_dk", "S": "cloud", "C": "clay", "k": "sea_dk"}

def amphora(c, x0, cy):
    """A wine amphora lying on its side, half buried: mouth to the left, a
    narrow neck with two handles, a full body painted with a black-figure band,
    tapering to the toe on the right. Lit from the top left."""
    # radius of the jar along its length: flared mouth, neck, round shoulder,
    # full belly, long taper to the toe
    prof = [3, 3, 2, 2, 2, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1]
    bury = cy + 5                       # sand line: the lowest rows are buried
    body = {}
    for i, r in enumerate(prof):
        for y in range(cy - r, cy + r + 1):
            body[(x0 + i, y)] = (i, (y - cy) / max(r, 1), r)
    for (x, y), (i, t, r) in body.items():
        if y >= bury:
            continue
        edge = (x - 1, y) not in body or (x + 1, y) not in body or \
            (x, y - 1) not in body or (x, y + 1) not in body
        if edge:
            n = "clay_dk"
        elif i in (8, 18):
            n = "ink"                                           # rings round the jar
        elif 11 <= i <= 15:
            # the black-figure panel; a clay figure (a leaping dolphin) in it
            fig = {(12, -2), (13, -3), (14, -2), (13, -1), (12, 0), (11, 1), (14, 0)}
            n = "clay" if (i, y - cy) in fig else "ink"
        elif t < -0.5:
            n = "shell"                                         # highlight
        elif t > 0.45:
            n = "clay_dk"
        else:
            n = "clay"
        c.set(x, y, n)
    c.set(x0 + 1, cy - 2, "shell")                             # lit rim of the mouth
    # handles: loops from the neck up and over to the shoulder
    for (hx, hy) in ((x0 + 4, cy - 3), (x0 + 4, cy - 4), (x0 + 5, cy - 5), (x0 + 6, cy - 6),
                     (x0 + 7, cy - 6), (x0 + 8, cy - 6)):
        c.set(hx, hy, "clay_dk")
    # half buried: sand piled along the bottom, a shadow line where it meets
    for x in range(x0 - 3, x0 + len(prof) + 3):
        c.set(x, bury, "sand_dk")
        c.set(x, bury + 1, "sand_md" if x % 2 else "sand")


SHELL = check_grid([" ff ", "fsff", " ss "])
SHELL_KEY = {"f": "foam", "s": "shell"}
PEBBLES = check_grid([" pp  ", "pPPp q", " pp qQ"])
PEBBLE_KEY = {"p": "rock_dk", "P": "rock_lt", "q": "rock_dk", "Q": "rock_lt"}


def sea_and_shore(c):
    gradient(c, HORIZON, [("sea_dk", 2), ("sea", 6), ("sea_md", 6), ("sea_lt", 30)])
    # wave lines on the sea, longer and lighter toward the shore
    for x0 in range(0, STRIP, 32):
        for (dx, y, n, w) in ((5, HORIZON + 4, "sea_md", 4), (21, HORIZON + 6, "sea_md", 3),
                              (12, HORIZON + 10, "sea_lt", 5), (27, HORIZON + 12, "sea_lt", 4),
                              (2, HORIZON + 15, "shallow", 6), (18, HORIZON + 17, "shallow", 5)):
            c.hline(x0 + dx, x0 + dx + w, y, n)
    for x in range(STRIP):
        s = shore_y(x)
        # shallows, then the foam: a lacy upper edge, a solid line, then the
        # wet sand the last wave left
        for y in range(s - 5, s - 2):
            if (x + y) % 2 == 0 or y == s - 3:
                c.set(x, y, "shallow")
        lace = hash2(x, 7) % 4
        for y in range(s - 2 - (1 if lace == 0 else 0), s + 1):
            c.set(x, y, "foam")
        if lace == 1:
            c.set(x, s - 3, "foam")
        c.set(x, s + 1, "wet_dk" if x % 9 == 0 else "wet")
        c.set(x, s + 2, "wet")
        c.set(x, s + 3, "wet" if (x + s) % 2 else "sand_dk")


def beach(c):
    """Dry sand from the wet line down. Ripples (long shallow arcs) and specks
    in bands that repeat every 32 px."""
    for x in range(STRIP):
        for y in range(shore_y(x) + 4, 240):
            c.set(x, y, "sand")
        for y in range(shore_y(x) + 4, shore_y(x) + 7):
            c.set(x, y, "sand_md" if (x + y) % 2 else "sand")
    for y0 in range(64, 240, 8):
        k = (y0 // 8) % 4
        for x0 in range(0, STRIP, 32):
            if k % 2 == 0:
                # a wind ripple: a shallow arc, lit on top
                ax = x0 + (5, 0, 19, 0)[k]
                w = 9
                for i in range(w):
                    dy = 0 if 2 <= i < w - 2 else 1
                    c.set(ax + i, y0 + 4 + dy, "sand_md")
                    if 2 <= i < w - 2:
                        c.set(ax + i, y0 + 3, "sand_lt")
            else:
                sx = x0 + (0, 26, 0, 11)[k]
                c.set(sx, y0 + 5, "sand_dk")
                c.set(sx + 1, y0 + 5, "sand_hi")


def strip():
    c = Canvas(STRIP, 256)
    gradient(c, 0, [("sky1", 12), ("sky2", 10), ("sky3", 9), ("sky4", HORIZON - 31)])
    c.rect(0, 240, STRIP, 256, "sky1")
    c.stamp(LONG_CLOUD, CLOUD_KEY, 70, 3)
    c.stamp(CLOUD, CLOUD_KEY, 126, 18)
    c.stamp(CLOUD, CLOUD_KEY, 212, 8)
    sea_and_shore(c)
    c.stamp(ISLET, ISLET_KEY, 104, HORIZON - len(ISLET) + 1)
    c.stamp(BOAT, BOAT_KEY, 216, HORIZON - 5)
    beach(c)
    # what the sea left on the sand
    amphora(c, 5, 89)
    c.stamp(SHELL, SHELL_KEY, 112, 92)
    c.stamp(SHELL, SHELL_KEY, 33, 101)
    c.stamp(PEBBLES, PEBBLE_KEY, 120, 98)
    c.stamp(PEBBLES, PEBBLE_KEY, 220, 64)
    return c


# --- Platforms ----------------------------------------------------------------
def mound_top(x, y, u, v):
    """A low sand mound: lit from the top left, ripple arcs across it. The
    pattern follows the platform so both mounds share tiles."""
    r = u * u + v * v
    lx, ly = int(round(u * 62)), int(round(v * 13))
    if r > 0.9:
        return "sand_dk" if v > 0.1 else "sand_md"
    # a smooth dome, lit from the top left, with 1 px checker steps between
    # the shades
    lit = -(0.45 * u + 0.9 * v) - 0.55 * r + 0.25
    step = 0.06 if (lx + ly) % 2 else -0.06
    lit += step
    # two faint wind ripples across the top
    s = v + 0.45 * u * u
    if abs(s + 0.3) < 0.05 or abs(s - 0.25) < 0.05:
        if -0.75 < u < 0.7 and lx % 7 != 0:
            return "sand_md"
    if lit > 0.45:
        return "sand_hi"
    if lit > 0.05:
        return "sand_lt"
    if lit > -0.45:
        return "sand"
    return "sand_md"


def mound_side(x, y, t, u):
    if t == 0:
        return "sand_md"
    if t >= 3:
        return "wet_dk" if u > 0.3 else "wet"
    return "sand_dk" if u < 0.5 else "wet"


def platforms():
    p = Canvas(STRIP, 256, wrap=False)
    for (cx, cy) in (OPP_PLATFORM, PLR_PLATFORM):
        platform(p, cx, cy, 62, 13, 4, mound_top, mound_side, shadow="sand_md",
                 under=("sand", "sand_lt", "sand_md"))
    return p


# --- The surf that washes across at the start ---------------------------------
def surf():
    """BG1 overlay (blended and fading while it scrolls right): a long wave
    breaking in foam, with spray."""
    c = Canvas(256, 256, wrap=True)
    base = 108
    for x in range(256):
        # crest height: a few big rollers and small chop between
        h = 10 + round(7 * max(0, math.sin(2 * math.pi * x / 64)) ** 3
                       + 2 * math.sin(2 * math.pi * x / 16 + 0.5))
        top = base - h
        for y in range(top, base + 1):
            d = y - top
            if d == 0:
                n = "foam"
            elif d < 3:
                n = "foam" if (x + y) % 3 else "shallow"
            elif d < 6:
                n = "shallow"
            elif d < 9:
                n = "sea_lt"
            else:
                n = "sea_md" if (x + y) % 4 else "sea_lt"
            c.set(x, y, n)
    for k in range(48):                       # spray
        r = hash2(k * 37, 11)
        x = (k * 16 + r % 11) % 256
        y = base - 14 - (r >> 4) % 20
        c.set(x, y, "foam")
        if (r >> 9) % 3 == 0:
            c.set(x + 1, y - 1, "shallow")
    return c


def main():
    full = compose(strip(), platforms())
    if "--preview" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--preview") + 1])
        preview_canvas(full, PAL, out / "sand_canvas.png")
        preview_canvas(surf(), PAL, out / "sand_surf.png")
    build_bg(full, PAL, OUT)
    PAL.write_jasc(OUT / "palette.pal")
    build_anim(surf(), PAL, OUT)


if __name__ == "__main__":
    main()
