#!/usr/bin/env python3
"""Battle background: a temple hall (building, indoor).

Inside a Doric temple such as the Temple of Hestia. Fluted marble columns hold
up the entablature across the top of the screen (triglyphs, guttae,
architrave). Between them, the cella wall carries a painted meander frieze;
bronze braziers burn in front of it and throw warm light on the wall and the
polished marble floor, and votive shields hang in the other bays. The
platforms are raised marble discs with an inlaid bronze ring.

The engine uses these tiles for several environments, each with its own
palette, all written here with the same layout:
  building/palette.pal     BATTLE_ENVIRONMENT_BUILDING: every indoor map
  building/gym.pal         BATTLE_ENVIRONMENT_GYM (MAP_BATTLE_SCENE_GYM): a
                           cooler hall with an Aegean-blue frieze
  building/leader.pal      BATTLE_ENVIRONMENT_LEADER (leader-class trainers,
                           so the Hierophants): the hearth blazing
  plain/palette.pal        BATTLE_ENVIRONMENT_PLAIN (paths and open ground):
                           the same colonnade in the open air, sky and far
                           hills between the columns, a sunny limestone terrace
  stadium/battle_frontier.pal  BATTLE_ENVIRONMENT_FRONTIER (link battles):
                           the hall by moonlight

Also anim_tiles.png/anim_map.bin: the light that streaks across at the start.
Those tiles are also drawn with the Hoenn stadium palettes (Magma, Aqua, the
Elite Four), so like vanilla they use only BG palette 4, colors 1-5; every
palette above keeps its streak colors in those slots.

Usage: python3 tools/ichor/art/battle_bg_building.py [--preview DIR]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle_bg_lib import (ENV, OPP_PLATFORM, PLR_PLATFORM, STRIP, Canvas, Pal,  # noqa: E402
                           build_anim, build_bg, check_grid, compose, hash2,
                           platform, preview_canvas)

OUT = ENV / "building"

# --- Palette ----------------------------------------------------------------
#   0: entablature, capitals, shafts, the wall and its frieze, shields
#   1: braziers, their glow on the wall, the stylobate
#   2: colors 1-5 the entry streaks (fixed slots, see above); 6-15 the floor
#      and the marble discs
COLORS = {
    # marble
    "m_hi": (248, 248, 240), "m": (216, 208, 192), "m_md": (192, 184, 168),
    "m_dk": (168, 160, 152), "m_sh": (120, 112, 104), "ink": (32, 24, 24),
    # the cella wall: plaster, its painted frieze, the dado
    "w_lt": (232, 216, 176), "w": (208, 184, 136),
    "wf": (184, 88, 48), "wf_ink": (32, 24, 24), "wf_line": (120, 48, 24),
    "dado": (144, 112, 72), "dado_lt": (176, 144, 96),
    # light
    "glow": (240, 216, 152), "glow2": (224, 200, 136),
    "flame_hi": (248, 248, 240), "flame": (248, 232, 160), "flame_md": (240, 192, 64),
    "flame_dk": (224, 136, 88),
    "bronze": (200, 144, 40), "bronze_dk": (120, 72, 24),
    # votive shields: their own colors, so plains can fade them into the sky
    "sh_rim": (200, 144, 40), "sh_face": (184, 88, 48), "sh_lt": (224, 136, 88),
    "sh_ink": (32, 24, 24),
    # floor
    "fl": (224, 216, 200), "fl_dk": (184, 176, 160), "refl": (240, 224, 176),
    # entry streaks (BG palette 4, colors 1-5)
    "st1": (248, 224, 144), "st2": (240, 192, 64), "st3": (248, 240, 200),
    "st4": (232, 200, 120), "st5": (248, 248, 240),
}
SUBS = [
    ["m_hi", "m", "m_md", "m_dk", "m_sh", "ink", "w_lt", "w", "wf", "wf_ink",
     "wf_line", "dado", "dado_lt"],
    ["w", "dado", "dado_lt", "glow", "glow2", "flame_hi", "flame", "flame_md",
     "flame_dk", "bronze", "bronze_dk", "sh_rim", "sh_face", "sh_lt", "sh_ink"],
    ["st1", "st2", "st3", "st4", "st5",
     "m_hi", "m", "m_md", "m_dk", "m_sh", "fl", "fl_dk", "refl", "bronze", "bronze_dk"],
]
PAL = Pal(COLORS, SUBS)
assert PAL.subs[2][:5] == ["st1", "st2", "st3", "st4", "st5"]

# BATTLE_ENVIRONMENT_GYM: a cooler hall, the frieze in Aegean blue.
GYM = PAL.variant(
    w_lt=(224, 224, 216), w=(200, 200, 192),
    wf=(48, 104, 176), wf_ink=(24, 56, 120), wf_line=(24, 56, 120),
    dado=(112, 120, 136), dado_lt=(144, 152, 168), glow=(232, 224, 192), glow2=(216, 208, 184),
    sh_face=(48, 104, 176), sh_lt=(112, 168, 224), refl=(232, 224, 208),
    st1=(232, 240, 248), st2=(208, 224, 240), st3=(216, 232, 248), st4=(192, 208, 232),
    st5=(248, 248, 240),
)
# BATTLE_ENVIRONMENT_LEADER: the hearth blazing for a Hierophant.
LEADER = PAL.variant(
    w_lt=(240, 200, 136), w=(224, 160, 96),
    dado=(120, 56, 32), dado_lt=(160, 80, 40), wf=(120, 48, 24), wf_ink=(32, 24, 24),
    wf_line=(32, 24, 24), glow=(248, 216, 120), glow2=(240, 184, 96),
    m=(232, 208, 176), m_md=(208, 176, 144), m_dk=(176, 136, 104), m_sh=(120, 80, 56),
    fl=(232, 200, 160), fl_dk=(192, 152, 112), refl=(248, 216, 120),
    st1=(248, 224, 112), st2=(248, 200, 64), st3=(240, 160, 64), st4=(248, 240, 176),
    st5=(248, 248, 224),
)
# BATTLE_ENVIRONMENT_PLAIN: the colonnade in the open air. The wall becomes
# sky, its frieze vanishes into it, the dado becomes far hills, the floor a
# sunny limestone terrace.
PLAIN = PAL.variant(
    w_lt=(176, 216, 240), w=(144, 192, 232),
    wf=(176, 216, 240), wf_ink=(176, 216, 240), wf_line=(176, 216, 240),
    dado=(120, 144, 104), dado_lt=(160, 176, 128), glow=(208, 232, 248), glow2=(192, 224, 240),
    sh_rim=(144, 192, 232), sh_face=(144, 192, 232), sh_lt=(144, 192, 232),
    sh_ink=(144, 192, 232),
    fl=(232, 216, 176), fl_dk=(200, 176, 128), refl=(240, 232, 200),
    m_sh=(136, 120, 96),
    st1=(232, 248, 224), st2=(208, 232, 176), st3=(224, 240, 208), st4=(200, 224, 168),
    st5=(248, 248, 240),
)
# BATTLE_ENVIRONMENT_FRONTIER (link battles): the hall by moonlight.
FRONTIER = PAL.variant(
    m_hi=(232, 240, 248), m=(192, 200, 216), m_md=(168, 176, 200), m_dk=(136, 144, 168),
    m_sh=(88, 96, 120), w_lt=(152, 160, 192), w=(120, 128, 168),
    wf=(72, 80, 120), wf_ink=(40, 48, 80), wf_line=(40, 48, 80),
    dado=(64, 72, 104), dado_lt=(88, 96, 128), glow=(176, 184, 216), glow2=(152, 160, 200),
    flame=(216, 232, 248), flame_md=(152, 192, 232), flame_dk=(112, 168, 224),
    bronze=(152, 144, 136), bronze_dk=(88, 80, 80), sh_rim=(152, 144, 136),
    sh_face=(72, 80, 120), sh_lt=(104, 112, 152),
    fl=(184, 192, 208), fl_dk=(144, 152, 176), refl=(208, 216, 240),
    st1=(232, 240, 248), st2=(200, 216, 240), st3=(216, 224, 248), st4=(176, 192, 224),
    st5=(248, 248, 248),
)

# --- Layout -----------------------------------------------------------------
PERIOD = 64
COLUMNS = [16 + PERIOD * k for k in range(4)]     # column centers
BRAZIERS = (112, 240)                              # bays with a brazier
SHIELDS = (48, 176)                                # bays with a votive shield
TOP_ARCH = 8         # architrave rows 8-12
CAP = 14             # capitals 14-20
FRIEZE = 16          # painted wall frieze 16-23
DADO = 40            # dado 40-47
STYLO = 48           # stylobate 48-55
FLOOR = 56           # floor from here down


def entablature(c):
    """Across the top: the bottom of the Doric frieze (triglyphs between plain
    metopes), the taenia, guttae under each triglyph, the architrave."""
    for x in range(STRIP):
        p = x % 16
        for y in range(0, 5):
            if p < 6:                                  # triglyph: two grooves
                c.set(x, y, "ink" if p in (1, 4) else ("m_dk" if p in (2, 5) else "m_md"))
            else:
                c.set(x, y, "m" if y > 0 else "m_md")  # metope
        c.set(x, 5, "m_hi")                            # taenia
        c.set(x, 6, "m_dk" if p < 6 else "m")
        c.set(x, 7, ("m_dk" if p in (0, 2, 4) else "m_sh") if p < 6 else "m")  # guttae
        c.set(x, TOP_ARCH, "m_hi")
        for y in range(TOP_ARCH + 1, 12):
            c.set(x, y, "m")
        c.set(x, 12, "m_dk")
        c.set(x, 13, "m_sh")                           # shadow under the beam


MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]


def wall(c):
    """The cella wall between the columns."""
    for x in range(STRIP):
        for y in range(14, FRIEZE):
            c.set(x, y, "w_lt")
        c.set(x, FRIEZE, "wf_line")
        c.set(x, FRIEZE + 1, "wf")
        for j, row in enumerate(MEANDER):
            ch = row[x % 8]
            c.set(x, FRIEZE + 2 + j, "wf_ink" if ch == "#" else "wf")
        c.set(x, FRIEZE + 7, "wf_line")
        for y in range(FRIEZE + 8, DADO):
            c.set(x, y, "w")
        c.set(x, DADO, "dado_lt")
        for y in range(DADO + 1, STYLO):
            c.set(x, y, "dado")


def column(c, cx):
    """A fluted Doric column: square abacus, swelling echinus, annulets, and a
    shaft lit from the left."""
    x0 = cx - 8
    cap = [
        "pppppppppppppppp",   # abacus
        "MMMMMMMMMMMMMMMd",
        " hhMMMMMMMMMMMd ",   # echinus
        "  hMMMMMMMMMMd  ",
        "  hhMMMMMMMMdd  ",
        "   hMMMMMMMdd   ",
        "  sdsdsdsdsdsd  ",   # annulets
    ]
    key = {"p": "m_hi", "M": "m", "h": "m_hi", "d": "m_dk", "s": "m_sh"}
    c.stamp(cap, key, x0, CAP)
    # shaft: 12 px, flutes as alternating light and dark lines
    shaft = ["m_sh", "m_hi", "m_hi", "m", "m_hi", "m", "m", "m_md", "m", "m_md", "m_dk", "m_sh"]
    for y in range(CAP + 7, STYLO):
        for i, n in enumerate(shaft):
            c.set(x0 + 2 + i, y, n)


def brazier(c, bx):
    """A bronze tripod brazier on the stylobate, its fire lighting the wall."""
    # glow on the wall: two rings of warm light behind the flame
    for y in range(FRIEZE + 8, STYLO):
        for x in range(bx - 20, bx + 21):
            d = math.hypot(x + 0.5 - bx, (y + 0.5 - 34) * 1.3)
            cur = c.get(x, y)
            if cur in ("w", "dado", "dado_lt"):
                if d < 11:
                    c.set(x, y, "glow")
                elif d < 16 and (x + y) % 2 == 0:
                    c.set(x, y, "glow")
                elif d < 16:
                    c.set(x, y, "glow2" if cur == "w" else cur)
                elif d < 20 and (x + y) % 2 == 0 and cur == "w":
                    c.set(x, y, "glow2")
    flame = check_grid([
        "      F      ",
        "     FF   F  ",
        "  F  FoF FF  ",
        "  FF FooFFo  ",
        "  FoFoyooFo  ",
        " FooFoyyooFo ",
        " FoyyoyhyyoF ",
        " roooyhhhyoor",
        "  rroyyhyorr ",
    ])
    c.stamp(flame, {"F": "flame_dk", "o": "flame_md", "y": "flame", "h": "flame_hi",
                    "r": "flame_dk"}, bx - 6, 26)
    bowl = check_grid([
        "bbbbbbbbbbbbbbb",
        "kBBBBBBBBBBBBBk",
        " kBBBBBBBBBBBk ",
        "  kkBBBBBBBkk  ",
        "     kkbkk     ",
        "      kBk      ",
        "     kB Bk     ",
        "    kB   Bk    ",
        "   kB  B  Bk   ",
        "  kB   B   Bk  ",
        " kk    k    kk ",
    ])
    c.stamp(bowl, {"b": "flame", "B": "bronze", "k": "bronze_dk"}, bx - 7, 35)


def shield(c, sx):
    """A round bronze hoplite shield hung on the wall: a lit bronze rim, a
    terracotta face, and Hestia's flame painted on it in black."""
    cy = 31.5
    for y in range(25, 39):
        for x in range(sx - 8, sx + 9):
            d = math.hypot(x + 0.5 - sx, y + 0.5 - cy)
            if d < 6.8:
                if d > 5.4:
                    n = "sh_rim"
                else:
                    lit = -((x + 0.5 - sx) + (y + 0.5 - cy)) / 6
                    n = "sh_lt" if lit > 0.45 else "sh_face"
                c.set(x, y, n)
    c.stamp(check_grid(["  k  ", " kk  ", " kkk ", "kkkkk", " kkk "]), {"k": "sh_ink"},
            sx - 2, 29)


def stylobate(c):
    for x in range(STRIP):
        c.set(x, STYLO, "m_hi")
        for y in range(STYLO + 1, STYLO + 4):
            c.set(x, y, "m")
        c.set(x, STYLO + 4, "m_dk")
        c.set(x, STYLO + 5, "m_hi")
        c.set(x, STYLO + 6, "m")
        c.set(x, STYLO + 7, "m_sh")


def floor(c):
    """Polished marble slabs, rows growing toward the viewer, joints staggered;
    the braziers glint on the floor near the steps."""
    rows = [FLOOR, 64, 74, 86, 100, 116, 134, 154, 176, 200, 226, 240]
    for i in range(len(rows) - 1):
        y0, y1 = rows[i], rows[i + 1]
        step = 32
        off = (i * 16) % 32
        for y in range(y0, y1):
            for x in range(STRIP):
                if y == y0:
                    n = "fl_dk"
                elif y == y0 + 1:
                    n = "m_hi"
                elif (x + off) % step == 0:
                    n = "fl_dk"
                else:
                    n = "fl"
                c.set(x, y, n)
    for cx in COLUMNS:                    # the columns mirrored in the polish
        for y in range(FLOOR + 2, FLOOR + 16):
            for x in range(cx - 5, cx + 5):
                if c.get(x, y) == "fl" and (x + y) % 2 == 0 and (y - FLOOR) < 16 - abs(x - cx):
                    c.set(x, y, "refl")
    for bx in BRAZIERS:
        for y in range(FLOOR + 2, FLOOR + 22):
            w = 3 - (y - FLOOR) // 8
            for x in range(bx - w, bx + w + 1):
                if c.get(x, y) == "fl" and (x + y) % 2 == 0:
                    c.set(x, y, "refl")


def strip():
    c = Canvas(STRIP, 256)
    wall(c)
    for bx in BRAZIERS:
        brazier(c, bx)
    for sx in SHIELDS:
        shield(c, sx)
    for cx in COLUMNS:
        column(c, cx)
    entablature(c)
    stylobate(c)
    floor(c)
    c.rect(0, 240, STRIP, 256, "m")      # above row 0 when the screen shakes
    return c


# --- Platforms ----------------------------------------------------------------
def disc_top(x, y, u, v):
    """A white marble dais with an inlaid bronze ring, lit from the top left."""
    r = math.sqrt(u * u + v * v)
    lx, ly = int(round(u * 62)), int(round(v * 13))
    if r > 0.95:
        return "m_dk" if v > 0 else "m_md"
    if 0.70 < r <= 0.78:
        return "bronze" if v < 0.2 else "bronze_dk"           # the inlay
    if 0.66 < r <= 0.70 or 0.78 < r <= 0.82:
        return "m_dk" if v > 0.3 else "m_md"
    lit = -(0.5 * u + 0.8 * v) + 0.1 - 0.3 * r
    vein = (lx * 2 - ly * 5 + 40) % 23 == 0 or (lx + ly * 7 + 60) % 31 == 0
    if vein and r < 0.64:
        return "m_md"
    if lit > 0.2:
        return "m_hi"
    if lit > -0.3:
        return "m" if (lx + ly) % 2 or lit < -0.05 else "m_hi"
    return "m"


def disc_side(x, y, t, u):
    if t == 0:
        return "m_hi" if u < 0.3 else "m"
    if t >= 3:
        return "m_sh"
    return "m_md" if u < 0.4 else "m_dk"


def platforms():
    p = Canvas(STRIP, 256, wrap=False)
    for (cx, cy) in (OPP_PLATFORM, PLR_PLATFORM):
        platform(p, cx, cy, 62, 13, 4, disc_top, disc_side, shadow="fl_dk",
                 under=("fl", "refl", "m_hi", "fl_dk"))
    return p


def plain_floor_tiles(s, plat):
    """Keep the floor plain in tiles the platforms touch (left block) so the
    two discs share their edge tiles."""
    for ty in range(FLOOR // 8, 32):
        for tx in range(32):
            if any(plat.px[ty * 8 + j][tx * 8 + i] is not None for j in range(8) for i in range(8)):
                for j in range(8):
                    for i in range(8):
                        y, x = ty * 8 + j, tx * 8 + i
                        if plat.px[y][x] is None and s.px[y][x] == "refl":
                            plat.px[y][x] = "fl"


# --- The light that streaks across at the start --------------------------------
def streaks():
    """BG1 overlay: long rays of light at different speeds of brightness, in
    BG palette 4 colors 1-5 only (see the module docstring)."""
    c = Canvas(256, 256, wrap=True)
    names = ["st1", "st2", "st3", "st4", "st5"]
    for k in range(18):
        r = hash2(k * 41, 3)
        y = 66 + (r % 44)
        x = (k * 37 + (r >> 6) % 30) % 256
        ln = 16 + (r >> 10) % 60
        core = names[(r >> 3) % 5]
        for i in range(ln):
            n = core if 2 < i < ln - 3 else "st4"
            c.set(x + i, y, n)
            if ln > 50 and 6 < i < ln - 8:
                c.set(x + i, y + 1, "st3")
    return c


def main():
    s = strip()
    plat = platforms()
    plain_floor_tiles(s, plat)
    full = compose(s, plat)
    if "--preview" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--preview") + 1])
        for name, pal in (("building", PAL), ("gym", GYM), ("leader", LEADER),
                          ("plain", PLAIN), ("frontier", FRONTIER)):
            preview_canvas(full, pal, out / f"{name}_canvas.png")
    build_bg(full, PAL, OUT)
    PAL.write_jasc(OUT / "palette.pal")
    GYM.write_jasc(OUT / "gym.pal")
    LEADER.write_jasc(OUT / "leader.pal")
    PLAIN.write_jasc(ENV / "plain/palette.pal")
    FRONTIER.write_jasc(ENV / "stadium/battle_frontier.pal")
    build_anim(streaks(), PAL, OUT)


if __name__ == "__main__":
    main()
