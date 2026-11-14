#!/usr/bin/env python3
"""Build, check and show the Temple of Hestia tileset in a proposed room.

1. Draws the tileset (temple_hestia.py) and compiles it with Porytiles.
2. Checks the compiled metatiles: every tile is the temple's own (or the
   transparent tile 0 in an upper layer) and every palette is 6-12.
3. Lays out the Hearth Trial room proposed in design/phase1/TILES_temple.md,
   cold and after the trial, and renders it with tools/ichor/render_map.py on
   the building primary and on aethos. The two renders must match pixel for
   pixel, which shows the temple works on any primary.

Writes, in design/phase1/img/:
  temple_room.png      the proposed room at 3x, braziers cold, the dais closed
  temple_room_lit.png  the same room after the trial
  temple_identity.png  building and aethos renders side by side, and the diff
  temple_sheet.png     every metatile with its id, from the compiled tileset

Usage: /usr/bin/python3 tools/ichor/art/temple_room.py [--layout-out map.bin]
  --layout-out writes the cold room as a map.bin (with collision and
  elevation) for whoever builds the real layout.
  --skip-compile renders what is already compiled.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import temple_hestia  # noqa: E402

BIN = ROOT / "data/tilesets/secondary/temple_hestia/porytiles_bin"
IMG = ROOT / "design/phase1/img"
BUILD = ROOT / "build/render"
PY = sys.executable

# --- The proposed room: 15 x 22 --------------------------------------------------
# One short code per cell; LEGEND maps codes to metatile names. The nave runs
# up the middle between two colonnades (x 3 and 11) with an aisle on each side.
LEGEND = {
    "..": "floor", "f1": "floor_vein_a", "f2": "floor_vein_b",
    "WT": "wall_top", "WL": "wall_corner_l", "WR": "wall_corner_r",
    "SL": "side_wall_l", "SR": "side_wall_r",
    "Fk": "frieze_key", "Fp": "frieze_palmette", "Ff": "frieze_flame",
    "Fa": "frieze_amphora", "Hl": "frieze_hestia_l", "Hr": "frieze_hestia_r",
    "Lw": "wall_lower", "Lr": "wall_lower_wreath", "Ll": "wall_lower_lamps",
    "Pt": "pilaster_top", "Pb": "pilaster_bottom",
    "Dt": "side_door_top", "Db": "side_door_bottom",
    "N1": "bed_niche_tl", "N2": "bed_niche_tr", "N3": "bed_niche_bl", "N4": "bed_niche_br",
    "Ct": "column_top", "Cb": "column_bottom",
    "dd": "dais", "dS": "dais_sun", "dl": "dais_edge_l", "dr": "dais_edge_r",
    "rr": "riser", "rl": "riser_l", "rR": "riser_r", "ST": "steps_runner",
    "i1": "inner_hearth_l", "i2": "inner_hearth_c", "i3": "inner_hearth_r",
    "RN": "runner_end_n_dais", "RU": "runner", "RS": "runner_end_s", "RC": "runner_cord",
    "It": "inlay_tl", "Ir": "inlay_tr", "Ib": "inlay_bl", "IR": "inlay_br",
    "Ih": "inlay_h", "Iv": "inlay_v",
    "Bt": "brazier_top_cold",
    "bT": "brazier_table_cold", "bL": "brazier_loom_cold", "bD": "brazier_door_cold",
    "bB": "brazier_bed_cold", "bH": "brazier_hearth_cold",
    "T1": "table_tl", "T2": "table_tr", "T3": "table_bl", "T4": "table_br",
    "L1": "loom_tl", "L2": "loom_tr", "L3": "loom_bl", "L4": "loom_br",
    "St": "stele_top", "Sb": "stele_bottom",
    "Am": "amphora", "Ar": "amphora_red", "Lt": "laurel_top", "Lb": "laurel_bottom",
    "Vo": "votive_lamps",
    "Ml": "mat_l", "Mm": "mat_m", "Mr": "mat_r",
}
# The great hearth in its pool of light: a 5 x 5 block, filled in below.
GLOW = "GG"

ROOM = """
WL WT WT WT WT WT WT WT WT WT WT WT WT WT WR
SL N1 N2 Pt Fk Fp Hl Hr Ff Fp Fk Pt Ff Dt SR
SL N3 N4 Pb Ll Lw Lw Lr Lw Lw Ll Pb Lw Db SR
SL .. .. Ct dl dd dd dS dd dd dr Ct .. .. SR
SL T1 T2 Cb dl dd i1 i2 i3 dd dr Cb L1 L2 SR
SL T3 T4 f1 dl dd dd RN dd dd dr .. L3 L4 SR
SL .. .. .. rl rr rr ST rr rr rR .. .. .. SR
SL .. f2 .. .. .. Bt RC Bt .. .. .. f1 .. SR
SL .. .. Ct .. .. bH RU bH .. .. Ct .. .. SR
SL Bt .. Cb .. f1 .. RU .. .. .. Cb .. Bt SR
SL bT .. .. It Ih Ih RU Ih Ih Ir .. .. bD SR
SL .. .. .. Iv GG GG GG GG GG Iv .. f2 .. SR
SL .. .. .. Iv GG GG GG GG GG Iv .. .. .. SR
SL .. f1 Ct Iv GG GG GG GG GG Iv Ct .. .. SR
SL .. .. Cb Iv GG GG GG GG GG Iv Cb .. .. SR
SL Bt .. .. Iv GG GG GG GG GG Iv .. .. Bt SR
SL bL .. .. Ib Ih Ih RU Ih Ih IR .. .. bB SR
SL .. .. f2 .. .. .. RU .. .. f1 .. .. .. SR
SL .. .. Ct .. .. .. RU .. .. .. Ct .. .. SR
SL Am Ar Cb .. St .. RU .. Lt .. Cb Vo .. SR
SL .. .. .. .. Sb .. RS .. Lb .. .. .. Am SR
SL .. .. .. .. .. Ml Mm Mr .. .. .. .. .. SR
"""
GLOW_ORIGIN = (5, 11)  # top-left of the 5 x 5 hearth block

# After the trial: every brazier burns and the cord is gone.
LIT = {
    "brazier_top_cold": "brazier_top_lit",
    "brazier_table_cold": "brazier_table_lit", "brazier_loom_cold": "brazier_loom_lit",
    "brazier_door_cold": "brazier_door_lit", "brazier_bed_cold": "brazier_bed_lit",
    "brazier_hearth_cold": "brazier_hearth_lit", "runner_cord": "runner",
}

# Metatiles the player can walk on; everything else gets collision 1.
PASSABLE_PREFIXES = ("floor", "runner", "inlay", "glow", "dais", "steps", "mat")
PASSABLE_EXCEPTIONS = {"runner_cord", "dais_edge_l", "dais_edge_r"}
ELEVATION = 3  # vanilla interiors use elevation 3 throughout


def names_grid():
    rows = [r.split() for r in ROOM.strip().splitlines()]
    w = len(rows[0])
    assert all(len(r) == w for r in rows), "ragged ROOM"
    grid = [[None if c == GLOW else LEGEND[c] for c in r] for r in rows]
    gx, gy = GLOW_ORIGIN
    for j in range(5):
        for i in range(5):
            inner = 1 <= i <= 3 and 1 <= j <= 3
            grid[gy + j][gx + i] = f"hearth_{j - 1}{i - 1}" if inner else f"glow_{j}{i}"
    return grid


def passable(name):
    return name.startswith(PASSABLE_PREFIXES) and name not in PASSABLE_EXCEPTIONS


def blockdata(grid, ids, lit=False, collision=False):
    out = []
    for row in grid:
        for name in row:
            if lit:
                name = LIT.get(name, name)
            v = ids[name]
            if collision:
                v |= (0 if passable(name) else 1) << 10
                v |= ELEVATION << 12
            out.append(v)
    return np.array(out, "<u2")


# --- Compile and check --------------------------------------------------------------

def compile_tileset():
    subprocess.run([PY, str(HERE / "temple_hestia.py")], check=True)
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.local/bin:/opt/homebrew/bin:" + env.get("PATH", "")
    # aethos's Porytiles cache is stale (its sources were repainted after its
    # last compile), so checksum verification has to be off to pair with it.
    r = subprocess.run(["porytiles", "compile-tileset", "--no-verify-checksums",
                        "gTileset_TempleHestia"], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        sys.exit("porytiles failed:\n" + r.stdout + r.stderr)


def check_compiled():
    mt = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    idx, pal = mt & 0x3FF, mt >> 12
    errors = []
    for n in range(len(mt)):
        for k in range(8):
            if idx[n, k] >= 512:
                if not 6 <= pal[n, k] <= 12:
                    errors.append(f"metatile {0x200 + n:#x} entry {k} uses palette {pal[n, k]}")
            elif idx[n, k] != 0:
                errors.append(f"metatile {0x200 + n:#x} entry {k} uses primary tile {idx[n, k]}")
            elif k < 4:
                errors.append(f"metatile {0x200 + n:#x} has a transparent first layer")
    tiles = Image.open(BIN / "tiles.png").size
    count = tiles[0] // 8 * tiles[1] // 8
    if errors:
        sys.exit("temple_room: compiled tileset is not self-contained:\n  " + "\n  ".join(errors[:20]))
    return len(mt), count


# --- Render ---------------------------------------------------------------------------

def render(blocks_path, width, primary, out):
    subprocess.run([PY, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(blocks_path),
                    "--width", str(width), "--primary", primary, "--secondary", "temple_hestia",
                    "-o", str(out)], check=True, capture_output=True)
    return np.array(Image.open(out).convert("RGB"))


def scaled(a, s):
    return Image.fromarray(a).resize((a.shape[1] * s, a.shape[0] * s), Image.NEAREST)


def identity_image(a, b):
    diff = np.any(a != b, axis=2)
    pad, s = 12, 2
    font = ImageFont.load_default(size=14)
    h, w = a.shape[0] * s, a.shape[1] * s
    img = Image.new("RGB", (3 * w + 4 * pad, h + 3 * pad + 18), (40, 40, 48))
    d = ImageDraw.Draw(img)
    vis = np.zeros_like(a)
    vis[diff] = (255, 0, 0)
    vis[~diff] = (a[~diff] // 3)
    for i, (label, arr) in enumerate((("--primary building", a), ("--primary aethos", b),
                                      (f"differing pixels: {int(diff.sum())}", vis))):
        x = pad + i * (w + pad)
        d.text((x, pad), label, fill=(230, 230, 200), font=font)
        img.paste(scaled(arr, s), (x, 2 * pad + 18))
    return img, int(diff.sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--layout-out", help="also write the cold room as a map.bin")
    ap.add_argument("--skip-compile", action="store_true")
    args = ap.parse_args()

    if not args.skip_compile:
        compile_tileset()
    n_meta, n_tiles = check_compiled()
    ids = temple_hestia.catalog()
    grid = names_grid()
    width, height = len(grid[0]), len(grid)

    BUILD.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    cold, lit = BUILD / "temple_room.bin", BUILD / "temple_room_lit.bin"
    blockdata(grid, ids).tofile(cold)
    blockdata(grid, ids, lit=True).tofile(lit)
    if args.layout_out:
        blockdata(grid, ids, collision=True).tofile(args.layout_out)

    a = render(cold, width, "building", BUILD / "temple_room_building.png")
    b = render(cold, width, "aethos", BUILD / "temple_room_aethos.png")
    la = render(lit, width, "building", BUILD / "temple_room_lit_building.png")
    lb = render(lit, width, "aethos", BUILD / "temple_room_lit_aethos.png")
    scaled(a, 3).save(IMG / "temple_room.png")
    scaled(la, 3).save(IMG / "temple_room_lit.png")
    ident, ndiff = identity_image(a, b)
    ident.save(IMG / "temple_identity.png")
    ndiff_lit = int(np.any(la != lb, axis=2).sum())

    subprocess.run([PY, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "temple_hestia",
                    "--primary", "building", "--scale", "3", "-o", str(IMG / "temple_sheet.png")],
                   check=True, capture_output=True)

    print(f"temple_room: {n_meta} metatiles, {n_tiles}/512 tiles; room {width}x{height}")
    print(f"identity: cold room {ndiff} px differ, lit room {ndiff_lit} px differ "
          f"(building vs aethos)")
    if ndiff or ndiff_lit:
        sys.exit("temple_room: the renders differ between primaries")


if __name__ == "__main__":
    main()
