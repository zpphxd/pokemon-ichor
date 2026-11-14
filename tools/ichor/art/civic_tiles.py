#!/usr/bin/env python3
"""Build gTileset_Civic, the Greek public halls: Asclepeion, Agora, Akademia.

The art lives in civic_art.py as hand-drawn character grids. This script cuts
it into 16x16 metatiles, writes the Porytiles sources (bottom/middle/top.png
and attributes.csv), compiles them, and checks the result.

Civic is a secondary that must work on any primary (aethos today, oikos for
interiors). Porytiles can only compile a secondary against a primary it
manages, so it pairs with aethos (porytiles/tilesets/gTileset_Civic/config.yaml),
but civic never borrows from it:
  - every metatile uses civic's own tiles (or the transparent tile 0) and civic's
    palettes 6-12, which the verify step enforces;
  - no civic color equals an aethos color, so Porytiles can't pack a civic tile
    into an aethos palette;
  - bottom layers are fully opaque, so the primary's backdrop never shows.

Metatile ids follow the order of METATILES below (0x200 upward). Room layouts
in civic_rooms.py refer to metatiles by name, so regenerate the rooms after any
change here.

Usage:
  /usr/bin/python3 tools/ichor/art/civic_tiles.py            # build, compile, verify, sheet
  /usr/bin/python3 tools/ichor/art/civic_tiles.py --no-compile
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import civic_art  # noqa: E402
from civic_art import ART, LEGEND  # noqa: E402

ART_PIECES = {"SCALE": civic_art.SCALE, "GOODS": civic_art.GOODS}

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/tilesets/secondary/civic/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/civic/porytiles_bin"
PRIMARY_PALS = ROOT / "data/tilesets/primary/aethos/porytiles_bin/palettes"
PORYTILES = Path.home() / ".local/bin/porytiles"
SHEET_OUT = ROOT / "design/phase1/img/civic_sheet.png"
CONFIG = ROOT / "porytiles/tilesets/gTileset_Civic/config.yaml"
MAGENTA = (255, 0, 255)
COLS = 8
FIRST_ID = 0x200

# The palette plan: seven palettes for the secondary's slots 6-12. Every 8x8
# tile must take all its colors from one of them, which keeps Porytiles'
# packing quick and the rooms' colors coherent.
PALETTES = {
    "marble": "#12345678BbGgTt",   # Asclepeion walls, counter, columns, statue
    "spring": "#1345678BbcCFGg",   # the spring basin, couches, glass, maps
    "clay": "#RTtuUrXP135678",     # pithoi, amphorae, kraters, votives, mats
    "wood": "#DdwWvpLPQRTtuU",     # Agora and Akademia timber, plaster, scrolls
    "bronze": "#zZxGghVXrDdwWv",   # braziers, the scale, coins, the sphere
    "grove": "#eEyYoOiIkKj8gA",    # grass, laurel, cypress, herbs, the snake
    "dyes": "#DdwWvMmnAaGghr",     # dyed cloth and the baskets of goods
}

# --- cells -------------------------------------------------------------------

EMPTY = ["." * 16] * 16


def C(name, cx=0, cy=0):
    """The 16x16 cell at (cx, cy) of an art piece."""
    rows = ART[name]
    return [r[cx * 16:cx * 16 + 16] for r in rows[cy * 16:cy * 16 + 16]]


def opaque(cell):
    return all("." not in r for r in cell)


def blank(cell):
    return all(set(r) == {"."} for r in cell)


def recolor(cell, mapping, rows=range(16)):
    out = list(cell)
    for y in rows:
        out[y] = "".join(mapping.get(ch, ch) for ch in out[y])
    return out


def over(base, piece):
    """Flattens piece onto base (both drawn in one layer)."""
    return ["".join(p if p != "." else b for b, p in zip(br, pr)) for br, pr in zip(base, piece)]


def hflip(cell):
    return [r[::-1] for r in cell]


# Floors in the row under a back wall sit in its shadow: darken the top rows.
SHADE = {"8": "6", "7": "5", "6": "5", "5": "4", "4": "3", "3": "2",
         "Q": "P", "P": "L", "L": "p", "U": "u", "u": "t", "t": "T",
         "I": "i", "i": "O", "O": "o", "o": "Y"}


def shadowed(cell, depth=4):
    once = recolor(cell, SHADE, range(depth))
    return recolor(once, SHADE, range(depth // 2))


# Wall ends: the wall turns the corner into the room's side, a dark edge and
# a lit return in the wall's own colors.
def wall_end(cell, side, dark="2", light="4"):
    out = []
    for y, r in enumerate(cell):
        r = list(r)
        if y > 0:
            for x, ch in ((0, dark), (1, light)):
                r[x if side == "l" else 15 - x] = ch
        out.append("".join(r))
    return out


def walls(prefix, top, body, dark, light):
    mt(f"{prefix}_wall_top", top, solid=True)
    mt(f"{prefix}_wall_top_l", wall_end(top, "l", dark, light), solid=True)
    mt(f"{prefix}_wall_top_r", wall_end(top, "r", dark, light), solid=True)
    mt(f"{prefix}_wall", body, solid=True)
    mt(f"{prefix}_wall_l", wall_end(body, "l", dark, light), solid=True)
    mt(f"{prefix}_wall_r", wall_end(body, "r", dark, light), solid=True)


def paste(cell, piece, x, y):
    out = [list(r) for r in cell]
    for j, line in enumerate(piece):
        for i, ch in enumerate(line):
            if ch != ".":
                out[y + j][x + i] = ch
    return ["".join(r) for r in out]


def vase(x, y, h=2):
    """The bottom cell of a jar answers like a vase ("…But, it was empty.")."""
    return "MB_VASE" if y == h - 1 else "MB_NORMAL"


# --- metatiles ---------------------------------------------------------------

METATILES = []   # dicts: name, bottom, middle, top, behavior, solid
BY_NAME = {}


def mt(name, bottom, middle=None, top=None, behavior="MB_NORMAL", solid=False):
    if name in BY_NAME:
        raise ValueError(f"duplicate metatile {name}")
    for layer in (bottom, middle, top):
        if layer is not None and (len(layer) != 16 or any(len(r) != 16 for r in layer)):
            raise ValueError(f"{name}: a layer is not a 16x16 cell")
    if not opaque(bottom):
        raise ValueError(f"{name}: bottom layer has transparent pixels")
    if middle is not None and blank(middle):
        middle = None
    if top is not None and blank(top):
        top = None
    if middle is not None and top is not None:
        raise ValueError(f"{name}: uses all three layers")
    m = dict(name=name, bottom=bottom, middle=middle, top=top, behavior=behavior, solid=solid)
    METATILES.append(m)
    BY_NAME[name] = len(METATILES) - 1
    return m


def obj(prefix, piece, bases, layer="middle", solid=True, behavior=None, top_rows=()):
    """Registers every cell of a piece as prefix_X_Y over the given base cells.

    bases is a list (one per cell row) of bottom cells, or a single cell.
    Rows listed in top_rows go on the top layer (drawn over sprites); the rest
    go on `layer`. A fully opaque cell replaces its base outright. solid and
    behavior may be a value or a function of (x, y)."""
    rows = ART[piece]
    w, h = len(rows[0]) // 16, len(rows) // 16
    for cy in range(h):
        # A cell is itself a list of row strings; a list of cells gives one per row.
        base = bases[cy] if isinstance(bases[0], list) else bases
        for cx in range(w):
            cell = C(piece, cx, cy)
            s = solid(cx, cy) if callable(solid) else solid
            b = behavior(cx, cy) if callable(behavior) else (behavior or "MB_NORMAL")
            name = f"{prefix}_{cx}_{cy}"
            if opaque(cell):
                mt(name, cell, behavior=b, solid=s)
            elif cy in top_rows:
                mt(name, base, top=cell, behavior=b, solid=s)
            else:
                mt(name, base, middle=cell if layer == "middle" else None,
                   top=cell if layer == "top" else None, behavior=b, solid=s)


# The void outside a room, for layout borders. A flat one-color tile would be
# matched to a flat tile of the primary, so a near-black fleck keeps it civic's.
VOID = ["#" * 16] * 16
VOID = VOID[:3] + ["###e#######e####"] + VOID[4:11] + ["####e#######e###"] + VOID[12:]


def define():
    mt("void", VOID, solid=True)

    # ---- Asclepeion ---------------------------------------------------------
    fa, fb = C("floor_marble_a"), C("floor_marble_b")
    fa_sh, fb_sh = shadowed(fa), shadowed(fb)
    mt("asc_floor_a", fa)
    mt("asc_floor_b", fb)
    mt("asc_floor_a_sh", fa_sh)
    mt("asc_floor_b_sh", fb_sh)

    top, body = C("wall_asc_top"), C("wall_asc_body")
    walls("asc", top, body, "2", "4")

    # Columns: capital and shaft draw over sprites; the plinth blocks.
    obj("asc_column", "column", [fa, fa, fa], top_rows=(0, 1),
        solid=lambda x, y: y == 2)

    # The healer's counter. The staff cell has the slab on the top layer so
    # the healer standing there is hidden from the waist down.
    for i, part in enumerate("lmr"):
        mt(f"asc_counter_{part}", fa_sh, middle=C("counter_asc_top", i, 0), solid=True)
    mt("asc_counter_staff", fa_sh, top=C("counter_asc_top", 1, 0))
    for i, part in enumerate("lmr"):
        mt(f"asc_counter_front_{part}", C("counter_asc_front", i, 0),
           behavior="MB_COUNTER", solid=True)

    obj("asc_basin", "basin", [body, fa_sh])
    obj("asc_relief", "relief", [top, body])
    obj("asc_votive_wall", "votive_wall", body)
    obj("asc_votive_counter", "votive_counter", fa_sh)

    # The Pithos corner. The great jar's bottom cells are the storage PC.
    obj("asc_pithos", "pithos_big", [top, body, fa_sh],
        behavior=lambda x, y: "MB_PC" if y == 2 else "MB_NORMAL")
    obj("asc_jar", "pithos_small", [body, fa_sh], behavior=vase)
    obj("asc_statue", "statue", [top, body, fa_sh])
    obj("asc_stairs", "stairs_up", [top, body, fa_sh],
        behavior=lambda x, y: "MB_NON_ANIMATED_DOOR" if y == 2 else "MB_NORMAL",
        solid=lambda x, y: y < 2)
    obj("asc_kline", "kline", fa)
    obj("asc_mosaic", "mosaic", fa, solid=False)
    obj("asc_snake", "snake", fa, solid=False)
    obj("asc_brazier", "brazier", fa, top_rows=(0,), solid=lambda x, y: y == 1)
    obj("asc_bench", "bench", fa)
    mt("asc_mat", fa, middle=C("mat_single"), behavior="MB_SOUTH_ARROW_WARP")

    # ---- Agora --------------------------------------------------------------
    ft = C("floor_tc")
    ft_sh = shadowed(ft)
    mt("ago_floor", ft)
    mt("ago_floor_sh", ft_sh)
    top, body = C("wall_ago_top"), C("wall_ago_body")
    walls("ago", top, body, "D", "p")

    # Dyed cloth in three colors, herbs, pottery shelves, all against the wall.
    obj("ago_cloth_purple", "cloth", [top, body], solid=True)
    for name, m in (("blue", {"n": "c", "M": "b", "m": "B", "g": "8", "G": "6", "D": "1"}),
                    ("saffron", {"n": "h", "M": "g", "m": "G", "g": "A", "G": "a"})):
        for cy, base in enumerate((top, body)):
            mt(f"ago_cloth_{name}_0_{cy}", base, middle=recolor(C("cloth", 0, cy), m), solid=True)
    obj("ago_herbs", "herbs", [top, body])
    obj("ago_shelf", "shelf_pots", [top, body, ft_sh],
        behavior=lambda x, y: "MB_SHOP_SHELF" if y == 2 else "MB_NORMAL")

    # The stall: awning, counter with the scale and the goods, its front.
    obj("ago_awning", "awning", [top, body])
    mt("ago_counter_l", ft_sh, middle=paste(C("counter_ago_top", 0, 0), ART_PIECES["SCALE"], 4, 0),
       solid=True)
    mt("ago_counter_m", ft_sh, middle=C("counter_ago_top", 1, 0), solid=True)
    mt("ago_counter_staff", ft_sh, top=C("counter_ago_top", 1, 0))
    mt("ago_counter_r", ft_sh, middle=paste(C("counter_ago_top", 2, 0), ART_PIECES["GOODS"], 2, 1),
       solid=True)
    for i, part in enumerate("lmr"):
        mt(f"ago_counter_front_{part}", C("counter_ago_front", i, 0),
           behavior="MB_COUNTER", solid=True)

    # The hall is a stoa: an inner colonnade on the clay floor.
    obj("ago_column", "column", ft, top_rows=(0, 1), solid=lambda x, y: y == 2)
    for good in ("grain", "olives", "figs", "pomegranates"):
        mt(f"ago_basket_{good}", ft, middle=C(f"basket_{good}"), solid=True)
    obj("ago_trapeza", "trapeza", ft)
    obj("ago_amphora", "amphora", ft, behavior=vase)
    obj("ago_jar", "pithos_small", ft, behavior=vase)
    mt("ago_mat", ft, middle=C("mat_single"), behavior="MB_SOUTH_ARROW_WARP")

    # ---- Akademia -----------------------------------------------------------
    ff = C("floor_flags")
    ff2 = hflip(ff)
    ff_sh = shadowed(ff)
    mt("aka_floor", ff)
    mt("aka_floor_b", ff2)
    mt("aka_floor_sh", ff_sh)
    mt("aka_floor_b_sh", shadowed(ff2))
    top, body = C("wall_aka_top"), C("wall_aka_body")
    walls("aka", top, body, "D", "L")

    # The grove: hedge, grass, the stylobate and its columns, the laurel.
    mt("aka_hedge_top", C("hedge", 0, 0), solid=True)
    mt("aka_hedge", C("hedge", 0, 1), solid=True)
    ga, gb = C("grass_a"), C("grass_b")
    mt("aka_grass", ga)
    mt("aka_grass_flowers", gb)
    mt("aka_grass_sh", shadowed(ga))
    st = C("stylobate")
    st_sh = shadowed(st)
    mt("aka_stylobate", st)
    mt("aka_stylobate_sh", st_sh)
    obj("aka_column", "column", st, top_rows=(0, 1), solid=lambda x, y: y == 2)
    mt("aka_column_cap_sh", st_sh, top=C("column", 0, 0))
    obj("aka_laurel", "laurel", ga, top_rows=(0, 1), solid=lambda x, y: y == 2)
    obj("aka_bench", "bench", ga)

    # Against the back wall: the map of Aethos, specimen jars, scrolls.
    obj("aka_map", "wall_map", [top, body])
    obj("aka_specimens", "specimens", [body, ff_sh])
    obj("aka_scrolls", "scroll_shelf", [top, body, ff_sh],
        behavior=lambda x, y: "MB_BOOKSHELF" if y == 2 else "MB_NORMAL")

    # Daphne's long marble table. Each krater has its own cell; to hide one,
    # set its cell to aka_table_m (the bare table).
    slab = [C("counter_asc_top", i, 0) for i in range(3)]
    mt("aka_table_l", ff, middle=slab[0], solid=True)
    mt("aka_table_m", ff, middle=slab[1], solid=True)
    mt("aka_table_r", ff, middle=slab[2], solid=True)
    for starter, (m1, m2, paint) in civic_art.KRATER_MOTIFS.items():
        krater = [r.replace("@" * 8, m1).replace("%" * 8, m2) for r in civic_art.KRATER]
        krater = recolor(krater, paint, range(len(krater)))
        mt(f"aka_krater_{starter}", ff, middle=paste(slab[1], krater, 1, 1), solid=True)
    obj("aka_table_front", "table_front", ff)

    # The study: the armillary sphere, writing desks and stools.
    obj("aka_armillary", "armillary", ff, top_rows=(0,), solid=lambda x, y: y == 1)
    obj("aka_desk", "desk", ff)
    mt("aka_stool", ff, middle=C("stool"), solid=True)

    # Alethea's corner: the worktable of finds, a crate, a marble head, tools.
    obj("aka_worktable", "worktable", ff)
    mt("aka_crate", ff, middle=C("crate"), solid=True)
    mt("aka_head", ff, middle=C("marble_head"), solid=True)
    mt("aka_tools", ff, middle=C("dig_tools"), solid=True)
    obj("aka_amphora", "amphora", ff, behavior=vase)
    mt("aka_mat", ff, middle=C("mat_single"), behavior="MB_SOUTH_ARROW_WARP")


# --- writing the Porytiles sources ---------------------------------------------

def to_rgba(cell):
    a = np.zeros((16, 16, 4), np.uint8)
    for y, r in enumerate(cell):
        for x, ch in enumerate(r):
            if ch == ".":
                a[y, x] = (*MAGENTA, 255)
            else:
                a[y, x] = (*LEGEND[ch], 255)
    return a


def write_sources():
    n = len(METATILES)
    rows = (n + COLS - 1) // COLS
    layers = {k: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for k in ("bottom", "middle", "top")}
    for img in layers.values():
        img[...] = (*MAGENTA, 255)
    for i, m in enumerate(METATILES):
        y, x = divmod(i, COLS)
        for k in layers:
            if m[k] is not None:
                layers[k][y * 16:y * 16 + 16, x * 16:x * 16 + 16] = to_rgba(m[k])
    SRC.mkdir(parents=True, exist_ok=True)
    for k, img in layers.items():
        Image.fromarray(img, "RGBA").save(SRC / f"{k}.png")
    with open(SRC / "attributes.csv", "w") as f:
        f.write("id,behavior\n")
        for i, m in enumerate(METATILES):
            if m["behavior"] != "MB_NORMAL":
                f.write(f"{i},{m['behavior']}\n")


# --- checks ------------------------------------------------------------------

def primary_colors():
    out = set()
    for p in sorted(PRIMARY_PALS.glob("*.pal")):
        vals = p.read_text().split()[3:]
        for i in range(0, len(vals) - 2, 3):
            out.add(tuple(int(v) for v in vals[i:i + 3]))
    return out


def tiles_of(cell):
    for ty in (0, 8):
        for tx in (0, 8):
            yield [r[tx:tx + 8] for r in cell[ty:ty + 8]]


def precheck():
    clash = {ch for ch, rgb in LEGEND.items() if rgb in primary_colors()}
    if clash:
        sys.exit(f"civic: legend colors {sorted(clash)} also appear in aethos's palettes")
    for name, cols in PALETTES.items():
        if len(set(cols)) != len(cols) or len(cols) > 15:
            sys.exit(f"civic: palette {name} must list at most 15 distinct colors")
    misfits = {}
    for m in METATILES:
        for k in ("bottom", "middle", "top"):
            if m[k] is None:
                continue
            for t in tiles_of(m[k]):
                cs = {ch for r in t for ch in r if ch != "."}
                if cs and not any(cs <= set(p) for p in PALETTES.values()):
                    misfits.setdefault("".join(sorted(cs)), m["name"])
    if misfits:
        for cs, name in misfits.items():
            print(f"  {name}: tile colors {cs} fit no palette")
        sys.exit("civic: every 8x8 tile must draw from one of the PALETTES")
    print(f"civic: {len(METATILES)} metatiles; every tile fits one of {len(PALETTES)} palettes")


def write_hints():
    """Hands the palette plan to Porytiles so its packer starts from it."""
    lines = [
        "# Generated by tools/ichor/art/civic_tiles.py; edit PALETTES there.",
        "# Civic is compiled against aethos, the Porytiles-managed primary, but must",
        "# work on any primary: it uses only its own tiles and palettes 6-12, which",
        "# civic_tiles.py verifies after every compile.",
        "tileset:",
        "  primary_pairing:",
        "    mode: manual",
        "    partners: [gTileset_Aethos]",
        "  palettes:",
        "    packing:",
        "      hints_enabled: true",
        "      hints:",
    ]
    for name, cols in PALETTES.items():
        lines.append(f"        - name: {name}")
        lines.append("          colors:")
        for ch in cols:
            lines.append(f"            - [{', '.join(str(v) for v in LEGEND[ch])}]")
    CONFIG.write_text("\n".join(lines) + "\n")


def compile_tileset():
    # --no-verify-checksums: aethos's Porytiles cache predates its last repaint,
    # and civic must not recompile aethos to refresh it.
    cmd = [str(PORYTILES), "compile-tileset", "--no-verify-checksums", "gTileset_Civic"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        print(r.stdout[-4000:], r.stderr[-4000:])
        sys.exit(f"civic: porytiles failed ({r.returncode})")


def verify():
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    # Porytiles compiles whole sheet rows, so the last row may pad with blanks.
    if not len(METATILES) <= len(raw) < len(METATILES) + COLS:
        sys.exit(f"civic: compiled {len(raw)} metatiles, expected {len(METATILES)}")
    tiles = Image.open(BIN / "tiles.png")
    ntiles = (tiles.width // 8) * (tiles.height // 8)
    bad = []
    for i, entries in enumerate(raw):
        for e in entries:
            idx, pal = int(e) & 0x3FF, int(e) >> 12
            if idx == 0:
                continue
            if idx < 512 or not 6 <= pal <= 12:
                bad.append((METATILES[i]["name"], idx, pal))
    if bad:
        sys.exit(f"civic: metatiles borrow from the primary: {bad[:8]}")
    print(f"civic: verified; {ntiles} tiles of 512, palettes 6-12 only")


def render_sheet():
    SHEET_OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["/usr/bin/python3", str(ROOT / "tools/ichor/render_map.py"), "--sheet", "civic",
                    "--primary", "aethos", "--scale", "2", "-o", str(SHEET_OUT)], cwd=ROOT, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    define()
    precheck()
    write_sources()
    write_hints()
    if args.no_compile:
        return
    compile_tileset()
    verify()
    render_sheet()


if __name__ == "__main__":
    main()
