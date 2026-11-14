#!/usr/bin/env python3
"""Battle background: olive grove and meadow (tall grass).

An old olive tree frames the screen: its gnarled silver trunk stands at the
left edge and its crown spills over both top corners (the strip wraps, so one
tree does both). Past the meadow, young olives line the coast, the Aegean
shows between them, and a far island carries a small Doric temple. Bright
Aegean sky with fair-weather clouds. The platforms are raised rings of turf on
an earth bank.

Writes, in graphics/battle_environment/:
  tall_grass/tiles.png, map.bin, palette.pal   BATTLE_ENVIRONMENT_GRASS
  tall_grass/anim_tiles.png, anim_map.bin      the grass that sweeps past at
                                               the start of a wild battle

Plains (BATTLE_ENVIRONMENT_PLAIN) draw the *building* tiles in the engine's
table, so their palette comes from battle_bg_building.py. If the director
points PLAIN at the TallGrass background (one line in
src/data/battle_environment.h, see design/phase1/BATTLE_BG.md), run this with
--plain-grove to write plain/palette.pal for this scene instead: the same
grove with trodden-earth platforms.

Usage: python3 tools/ichor/art/battle_bg_grass.py [--preview DIR] [--plain-grove]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle_bg_lib import (ENV, OPP_PLATFORM, PLR_PLATFORM, STRIP, Canvas, Pal,  # noqa: E402
                           build_anim, build_bg, check_grid, compose, gradient,
                           hash2, in_ellipse, platform, preview_canvas)

# --- Palette ----------------------------------------------------------------
# Master palette families (design/phase1/PLAN.md) plus in-between shades that
# stay inside them. Tile rows are laid out so that each 8x8 tile needs one
# sub-palette: the horizon sits at y = 48 and the shore at y = 56.
#   0: sky, clouds, sea, the far island
#   1: olive trees over sky and sea
#   2: the meadow, the trunk's foot and the platforms
COLORS = {
    "sky1": (112, 168, 224), "sky2": (144, 192, 232), "sky3": (176, 216, 240),
    "sky4": (208, 232, 248), "cloud": (248, 248, 240), "cloud_sh": (192, 208, 232),
    "sea": (48, 104, 176), "sea_lt": (112, 168, 224), "sea_dk": (32, 72, 136),
    "far": (136, 168, 184), "far_lt": (168, 192, 208), "far_dk": (112, 144, 168),
    "marble": (248, 248, 240), "marble_sh": (168, 176, 184),
    # olive trees
    "lf_dk": (56, 72, 32), "lf": (96, 112, 48), "lf_lt": (144, 160, 72),
    "lf_si": (168, 184, 136), "lf_hi": (208, 216, 184),
    "bk_dk": (80, 72, 56), "bk": (128, 120, 96), "bk_lt": (176, 168, 144),
    # meadow
    "mw": (200, 200, 128), "mw_lt": (216, 216, 152), "mw_dk": (168, 168, 96),
    "flower": (184, 88, 48), "bloom": (248, 248, 240),
    # platform turf (recolored for plains)
    "pg_dk": (96, 112, 48), "pg": (144, 160, 72), "pg_lt": (176, 184, 104),
    "pg_hi": (200, 208, 144),
    "ea_hi": (224, 200, 152),
}
SUBS = [
    ["sky1", "sky2", "sky3", "sky4", "cloud", "cloud_sh", "sea", "sea_lt", "sea_dk",
     "far", "far_lt", "far_dk", "marble", "marble_sh"],
    ["sky1", "sky2", "sky3", "sky4", "sea_lt", "sea", "sea_dk",
     "lf_dk", "lf", "lf_lt", "lf_si", "lf_hi", "bk_dk", "bk", "bk_lt"],
    ["mw", "mw_lt", "mw_dk", "flower", "bloom", "lf_dk", "lf_lt",
     "bk_dk", "bk", "bk_lt", "ea_hi", "pg_dk", "pg", "pg_lt", "pg_hi"],
]
PAL = Pal(COLORS, SUBS)

# For plains, if they are ever pointed at this scene (--plain-grove): the
# platforms' turf becomes trodden limestone earth.
PLAIN = PAL.variant(
    pg_dk=(136, 104, 64), pg=(176, 144, 96), pg_lt=(208, 184, 136), pg_hi=(232, 216, 176),
)

HORIZON = 48   # first row of sea
SHORE = 56     # first row of meadow

# --- Motifs -----------------------------------------------------------------
CLOUD = check_grid([
    "             oooo               ",
    "        ooo oooooooo  ooo       ",
    "     oooooooooooooooooooooo     ",
    "   ooooooooooooooooooooooooooo  ",
    " oooooooooooooooooooooooooooooo ",
    "osoooooooooooooooooooooooooooooo",
    "ssssooooooossssssoooooosssssssss",
    "  ssssssssss    sssssssss       ",
])
SMALL_CLOUD = check_grid([
    "      oooo       ",
    "  ooooooooooo    ",
    "ooooooooooooooo  ",
    "sssooooosssssssss",
    "  sssssss        ",
])
CLOUD_KEY = {"o": "cloud", "s": "cloud_sh"}

# The far island, with a small Doric temple on its crest: pediment, entablature,
# four columns, steps. Drawn in the cool haze of distance.
ISLAND = check_grid([
    "                    mmm                              ",
    "                  mmmmmmm                            ",
    "                mmmmmmmmmmm                          ",
    "                sssssssssss                          ",
    "                m.mm.mm.mm.                          ",
    "                m.mm.mm.mm.                          ",
    "                m.mm.mm.mm.                          ",
    "               sssssssssssss                         ",
    "         llllllllllllllllllllllll                    ",
    "    lllllllll::::::::lllllllllllllllll               ",
    " lllll:::::::::::::::::::::lllllllllllllllll         ",
    "::::::::::::::::::::::::::::::::::::::::::::lllllll  ",
])
ISLAND_KEY = {"m": "marble", "s": "marble_sh", ".": "far_dk", "l": "far_lt", ":": "far"}

# A young olive of the coastal grove: silver crown on a dark trunk.
GROVE_TREE = check_grid([
    "    s ss       ",
    "  sssssss s    ",
    " ssllsssssss   ",
    "sslllllssllls  ",
    "slllolllllllo  ",
    " lloooollloooo ",
    "  ooddoooooodd ",
    "    d tbd  d   ",
    "      bd       ",
])
GROVE_KEY = {"s": "lf_si", "l": "lf_lt", "o": "lf", "d": "lf_dk", "t": "bk", "b": "bk_dk"}

# The old olive's trunk: two twisted stems from a broad foot, the left one lit.
TRUNK = check_grid([
    "   db              db    ",
    "   dbd            dbd    ",
    "    dbd          dbd     ",
    "    dBbd        dbbd     ",
    "     dBbd      dbBd      ",
    "     dBbbd    dbBd       ",
    "      dBbbd  dbBbd       ",
    "      dBBbbddbBbd        ",
    "       dBBbbbBbbd        ",
    "       dBBbbBbbd         ",
    "       dBBbbBbbd         ",
    "      dBBbbbBbbd         ",
    "      dBBbbdbBbbd        ",
    "      dBBbd dBbbd        ",
    "     dBBbd  dBbbd        ",
    "     dBBbd  dBBbbd       ",
    "     dBBbbd dBBbbd       ",
    "     dBBbbdddBbbbd       ",
    "     dBBbbbbBBbbbd       ",
    "     dBBbbbbBbbbd        ",
    "     dBBBbbbBbbbd        ",
    "     dBBBbbbbBbbd        ",
    "    dBBBbbbbbBbbd        ",
    "    dBBBbbdbbBbbd        ",
    "    dBBBbbd dBbbbd       ",
    "    dBBBbd  dBbbbd       ",
    "    dBBBbd  dBBbbd       ",
    "   dBBBbbd  dBBbbbd      ",
    "   dBBBbbdd dBBbbbd      ",
    "   dBBBbbbbddBBbbbbd     ",
    "  dBBBbbbbbbbBBbbbbd     ",
    "  dBBBbbbbbbbBBbbbbbd    ",
    "  dBBbbbbbbbbbBBbbbbd    ",
    " dBBBbbbbbbbbbBbbbbbbd   ",
    " dBBbbbbbdbbbbbBbbbbbd   ",
    "dBBbbbbbd dbbbbbBbbbbbd  ",
    "ddddddddd  dddddddddddd  ",
])
TRUNK_KEY = {"d": "bk_dk", "b": "bk", "B": "bk_lt"}
TRUNK_X, TRUNK_TOP = -2, 44   # the foot rests at y = TRUNK_TOP + len(TRUNK)


def crown(c, clusters):
    """An olive crown built from round leaf clusters, drawn in list order (back
    first). Each cluster has a lobed edge and is lit from the top left: silver
    on top, olive in the middle, dark underneath. Leaf dabs break up the bands,
    and a cluster's lower edge gets a dark line wherever it is not over sky."""
    owner = {}
    for k, (ex, ey, r, ph) in enumerate(clusters):
        rx, ry = r, r * 0.8
        pts = {}
        for y in range(int(ey - ry * 1.25) - 1, int(ey + ry * 1.25) + 2):
            for x in range(int(ex - rx * 1.25) - 1, int(ex + rx * 1.25) + 2):
                dx, dy = (x + 0.5 - ex) / rx, (y + 0.5 - ey) / ry
                a = math.atan2(dy, dx)
                edge = 1 + 0.11 * math.sin(7 * a + ph) + 0.06 * math.sin(13 * a + 3 * ph)
                rr = math.hypot(dx, dy) / edge
                if rr <= 1:
                    pts[(x, y)] = (dx, dy, rr)
        for (x, y), (dx, dy, rr) in pts.items():
            lit = -(0.6 * dx + 0.8 * dy) - 0.35 * rr * rr + 0.1
            # leaf dabs: short slanted marks, lighter in the shade, darker in
            # the light, so the crown reads as many leaves
            dab = hash2(x, y) % 9 == 0
            if dab:
                lit += 0.38 if lit < 0 else -0.38
            if lit > 0.55:
                n = "lf_hi"
            elif lit > 0.18:
                n = "lf_si"
            elif lit > -0.25:
                n = "lf_lt"
            elif lit > -0.7:
                n = "lf"
            else:
                n = "lf_dk"
            c.set(x, y, n)
            owner[(x % c.w, y)] = k
        for (x, y), (dx, dy, rr) in pts.items():
            if dy > 0.15 and (x, y + 1) not in pts and owner.get((x % c.w, y + 1)) is not None:
                c.set(x, y + 1, "lf_dk")     # over a cluster behind: shade line
            elif dy > 0.35 and (x, y + 1) not in pts:
                c.set(x, y, "lf_dk")         # underside against the sky
    return owner


FAR_TUFT = ["d.d", ".d."]
MID_TUFT = ["d...d", ".d.d.", "..d.."]
NEAR_TUFT = ["d..l..d", ".d.l.d.", ".ddldd.", "..ddd.."]
ANEMONE = [".f.", "fLf", ".f.", ".g."]
CHAMOMILE = ["b", "g"]
MARK_KEY = {"d": "mw_dk", "l": "lf_lt", "f": "flower", "L": "mw_lt", "g": "lf_lt", "b": "bloom"}

# Meadow bands from the shore down: (first row, height, marks). Each band's
# marks repeat every 32 px; bands shift so the pattern does not form columns.
# Below the screen (y >= 112) the last two bands repeat, which keeps the tile
# count down; they only show when the screen shakes.
BAND_FAR = [(FAR_TUFT, 6, 4), (FAR_TUFT, 23, 2)]
BAND_MID_A = [(MID_TUFT, 2, 2), (MID_TUFT, 19, 4)]
BAND_MID_B = [(MID_TUFT, 12, 3), (FAR_TUFT, 28, 1)]
BAND_NEAR_A = [(NEAR_TUFT, 4, 3), (MID_TUFT, 22, 1)]
BAND_NEAR_B = [(NEAR_TUFT, 17, 2), (CHAMOMILE, 7, 2)]


def meadow(c):
    """The meadow, in 8-row bands of marks that repeat every 32 px. The near
    bands alternate all the way down (below y = 112 they only show when the
    screen shakes), which keeps the tile count down."""
    c.rect(0, SHORE, STRIP, 240, "mw")
    c.hline(0, STRIP, SHORE, "mw_lt")            # the sunlit lip of the shore
    for y in range(SHORE + 1, SHORE + 4):        # haze over the far meadow
        for x in range(STRIP):
            if y < SHORE + 3 or (x + y) % 2:
                c.set(x, y, "mw_lt")
    bands = [(SHORE, BAND_FAR), (64, BAND_MID_A), (72, BAND_MID_B)]
    for i, y in enumerate(range(80, 240, 8)):
        bands.append((y, BAND_NEAR_A if i % 2 == 0 else BAND_NEAR_B))
    for y0, marks in bands:
        for grid, mx, my in marks:
            for x0 in range(0, STRIP, 32):
                c.stamp(grid, MARK_KEY, x0 + mx, y0 + my)


def strip():
    c = Canvas(STRIP, 256)
    gradient(c, 0, [("sky1", 14), ("sky2", 12), ("sky3", 11), ("sky4", HORIZON - 37)])
    c.rect(0, 240, STRIP, 256, "sky1")          # seen above row 0 when the screen shakes
    # the sea, darkest at the horizon, shallows by the shore
    gradient(c, HORIZON, [("sea_dk", 1), ("sea", 4), ("sea_lt", SHORE - HORIZON - 5)])
    for x in range(0, STRIP, 16):               # glints
        c.hline(x + 3, x + 6, HORIZON + 2, "sea_lt")
        c.hline(x + 11, x + 13, HORIZON + 4, "sea_lt")
        c.hline(x + 7, x + 9, HORIZON + 6, "sea")
    c.stamp(ISLAND, ISLAND_KEY, 96, HORIZON - len(ISLAND))
    c.stamp(CLOUD, CLOUD_KEY, 74, 2)
    c.stamp(SMALL_CLOUD, CLOUD_KEY, 120, 22)
    c.stamp(SMALL_CLOUD, CLOUD_KEY, 166, 6)
    meadow(c)
    # anemones in the open spots between the battlers
    for fx, fy in ((104, 89), (111, 93), (118, 88), (24, 93), (31, 97), (214, 62)):
        c.stamp(ANEMONE, MARK_KEY, fx, fy)
    c.stamp(CHAMOMILE, MARK_KEY, 12, 99)
    c.stamp(CHAMOMILE, MARK_KEY, 108, 99)
    # the coastal grove, its crowns over the sea, trunks on the shore line
    for gx, fl in ((24, 0), (40, 1), (152, 0), (168, 1), (200, 0), (232, 1)):
        c.stamp(GROVE_TREE, GROVE_KEY, gx, SHORE - len(GROVE_TREE), hflip=fl)
    # the old olive: trunk, then crown over it (wraps to both screen edges)
    c.stamp(TRUNK, TRUNK_KEY, TRUNK_X, TRUNK_TOP)
    foot = TRUNK_TOP + len(TRUNK)
    for x in range(-14, 30):                      # dappled shade at its foot
        for y in range(foot - 3, foot + 3):
            if c.get(x, y) == "mw" and (x + y) % 2 == 0 and abs(x - 8) < 22 - 3 * abs(y - foot):
                c.set(x, y, "mw_dk")
    crown(c, [
        # back row, under the sky
        (-56, 20, 10, 0.3), (-38, 8, 14, 1.1), (-14, 0, 16, 2.0), (12, -2, 17, 0.6),
        (38, 4, 15, 2.6), (58, 16, 11, 1.7),
        # middle
        (-46, 30, 10, 2.2), (-26, 20, 14, 0.9), (-2, 14, 16, 1.5), (24, 18, 15, 0.2),
        (46, 28, 11, 2.9),
        # low and in front
        (-30, 38, 9, 1.3), (-12, 32, 12, 2.4), (10, 32, 13, 0.8), (30, 38, 9, 1.9),
        (-2, 44, 8, 0.4),
    ])
    return c


# --- Platforms ----------------------------------------------------------------
def turf_top(x, y, u, v):
    """Top of the turf ring: a darker ring of tufts round a lit center. The
    texture follows the platform, not the screen, so both platforms share
    their tiles."""
    r = u * u + v * v
    lx, ly = int(round(u * 62)), int(round(v * 13))
    if r > 0.86:                                 # the outer ring of tufts
        if v > 0.1:
            return "pg_dk"
        return "pg_dk" if (lx + ly) % 4 == 0 else "pg"
    if r > 0.66:
        if v > 0.3:
            return "pg" if (lx + ly) % 3 else "pg_dk"
        return "pg_lt" if (lx * 2 + ly) % 5 else "pg"
    # the lit center: a soft highlight toward the top left
    h = (u + 0.25) ** 2 / 0.25 + (v + 0.35) ** 2 / 0.16
    if h < 1.0:
        return "pg_hi" if h < 0.55 or (lx + ly) % 2 == 0 else "pg_lt"
    # small tufts on a staggered grid
    if ly % 4 == 0 and (lx + 5 * (ly // 4)) % 11 in (0, 2):
        return "pg"
    if ly % 4 == 1 and (lx + 5 * (ly // 4)) % 11 == 1:
        return "pg"
    return "pg_lt"


def earth_side(x, y, t, u):
    if t == 0:
        return "ea_hi" if u < 0.3 else "bk_lt"
    if t >= 4:
        return "bk_dk"
    lx = int(round(u * 62))
    if (lx + 3 * t) % 9 == 0:
        return "bk_lt"                           # stones in the bank
    if t == 3 or u > 0.6:
        return "bk_dk" if (lx + t) % 2 else "bk"
    return "bk"


def platforms():
    p = Canvas(STRIP, 256, wrap=False)
    for (cx, cy) in (OPP_PLATFORM, PLR_PLATFORM):
        platform(p, cx, cy, 62, 13, 5, turf_top, earth_side, rim="pg_dk",
                 shadow="mw_dk")
    return p


def clear_marks(strip_c, plat):
    """Wipe the meadow's marks from every tile a platform touches (left block
    only), so the two platforms' edge tiles come out the same."""
    for ty in range(SHORE // 8 + 1, 32):
        for tx in range(32):
            if any(plat.px[ty * 8 + j][tx * 8 + i] is not None for j in range(8) for i in range(8)):
                for j in range(8):
                    for i in range(8):
                        y, x = ty * 8 + j, tx * 8 + i
                        if plat.px[y][x] is None and y >= SHORE + 4:
                            plat.px[y][x] = "mw"


# --- The grass that sweeps past at the start of a wild battle ----------------
def sweep():
    """32x32-tile BG1 overlay. A band of tall meadow grass with red anemones
    (rows 8-13); the intro scrolls it sideways and down out of view."""
    c = Canvas(256, 256, wrap=True)
    base = 111

    def blade(x0, h, w, lean, body, shade, edge):
        # a tapered blade: lit left edge, shaded right half
        for t in range(h):
            f = t / h
            half = (w / 2) * (1 - f) ** 0.8
            cx = x0 + lean * f ** 1.6
            xa, xb = round(cx - half), round(cx + half)
            for x in range(xa, max(xa, xb) + 1):
                n = shade if x > cx else body
                if x == xa and edge and t > 2:
                    n = edge
                c.set(x, base - t, n)

    # back layer: tall, dark
    for i, x0 in enumerate(range(0, 256, 6)):
        r = hash2(x0, 1)
        blade(x0 + r % 3, 26 + r % 18, 5 + r % 2, (r >> 5) % 11 - 5, "pg_dk", "lf_dk", None)
    # front layer: shorter, sunlit
    for i, x0 in enumerate(range(3, 256, 8)):
        r = hash2(x0, 2)
        blade(x0 + r % 3, 14 + r % 16, 6 + r % 3, (r >> 5) % 9 - 4, "pg_lt", "pg", "pg_hi")
    for y in range(base - 5, base + 1):              # dense roots
        for x in range(256):
            c.set(x, y, "lf_dk" if (x + y) % 3 == 0 else "pg_dk")
    # red anemones on thin stems, in front of the blades
    for k, fx in enumerate((14, 61, 103, 150, 197, 236)):
        fy = base - 20 - (k * 5) % 9
        c.stamp(check_grid([" f ", "fFf", " f ", " g ", " g ", " g "]),
                {"f": "flower", "F": "ea_hi", "g": "pg_dk"}, fx, fy)
    return c


def main():
    s = strip()
    plat = platforms()
    clear_marks(s, plat)
    full = compose(s, plat)
    if "--preview" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--preview") + 1])
        preview_canvas(full, PAL, out / "grass_canvas.png")
        preview_canvas(full, PLAIN, out / "plain_canvas.png")
        preview_canvas(sweep(), PAL, out / "grass_sweep.png")
    build_bg(full, PAL, ENV / "tall_grass")
    PAL.write_jasc(ENV / "tall_grass/palette.pal")
    if "--plain-grove" in sys.argv:
        PLAIN.write_jasc(ENV / "plain/palette.pal")
    build_anim(sweep(), PAL, ENV / "tall_grass")


if __name__ == "__main__":
    main()
