#!/usr/bin/env python3
"""The Temple of Hestia map: design, layout, checks and review renders.

The room is the Hearth Trial hall (design/phase1/SCRIPT.md Part 5) drawn with the
temple_hestia tileset (design/phase1/TILES_temple.md). ROOM below is the design;
this script turns it into LAYOUT_AKTI_TOWN_TEMPLE_OF_HESTIA and checks it.

1. Writes data/layouts/AktiTown_TempleOfHestia/map.bin (collision 1 on every
   blocking metatile, elevation 3 throughout) and border.bin (the `void` metatile),
   and generates the brazier scripts in scripts.pory.
2. Checks the map against data/maps/AktiTown_TempleOfHestia/map.json and scripts.pory:
   - every person stands on a walkable tile, every warp and trigger sits on the
     door mat, and every bg event is on a blocking tile the player can face;
   - every walkable tile is reachable from the door, with the people in place;
   - the dais is shut while the cord is up and open once it burns away;
   - every setmetatile() in the script targets a brazier, its light or the cord,
     with that piece's own cold or lit metatile;
   - scripts.pory's brazier scripts (Light*, Douse*, DrawBraziers), which this
     script writes between two markers, match the room.
3. Renders, in design/phase1/img/ (from the compiled tileset, as the game draws it):
   temple_map.png         the layout as built, braziers cold, at 3x
   temple_map_lit.png     after the trial: every brazier lit, the cord gone
   temple_map_events.png  2x plan with people, sight lines, warps, triggers and bg events
   With --review NAME, design review sheets drawn straight from the tileset's
   source grids (no Porytiles compile needed), in design/phase1/img/:
   temple_NAME_room.png    the room at 2x, cold and solved, side by side
   temple_NAME_views.png   GBA-screen-sized views (15 x 10 tiles) along the route, 2x
   temple_NAME_stages.png  the room at each step of the trial, 1x

Usage: /usr/bin/python3 tools/ichor/maps/temple.py [--check] [--review NAME]
  --check only verifies that map.bin, border.bin and the brazier scripts are
  current; it writes nothing.
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map  # noqa: E402
import temple_hestia  # noqa: E402

LAYOUT_ID = "LAYOUT_AKTI_TOWN_TEMPLE_OF_HESTIA"
LAYOUT_DIR = ROOT / "data/layouts/AktiTown_TempleOfHestia"
MAP_DIR = ROOT / "data/maps/AktiTown_TempleOfHestia"
IMG = ROOT / "design/phase1/img"

# --- The design ----------------------------------------------------------------------
# One short code per cell; LEGEND maps codes to temple_hestia metatile names.
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
    "rr": "riser", "rl": "riser_l", "rR": "riser_r", "ST": "steps_runner", "Sp": "steps_plain",
    "i1": "inner_hearth_l", "i2": "inner_hearth_c", "i3": "inner_hearth_r",
    "RN": "runner_end_n_dais", "RU": "runner", "RS": "runner_end_s", "RC": "runner_cord",
    "It": "inlay_tl", "Ir": "inlay_tr", "Ib": "inlay_bl", "IR": "inlay_br",
    "Ih": "inlay_h", "Iv": "inlay_v",
    "Bt": "brazier_top_cold",
    "bT": "brazier_table_cold", "bL": "brazier_loom_cold", "bD": "brazier_door_cold",
    "bB": "brazier_bed_cold", "bH": "brazier_hearth_cold",
    "T1": "table_tl", "T2": "table_tr", "T3": "table_bl", "T4": "table_br",
    "L1": "loom_tl", "L2": "loom_tr", "L3": "loom_bl", "L4": "loom_br",
    "K1": "kline_tl", "K2": "kline_tr", "K3": "kline_bl", "K4": "kline_br",
    "St": "stele_top", "Sb": "stele_bottom",
    "Am": "amphora", "Ar": "amphora_red", "Lt": "laurel_top", "Lb": "laurel_bottom",
    "Vo": "votive_lamps",
    "Ml": "mat_l", "Mm": "mat_m", "Mr": "mat_r",
    "P1": "basin_top", "P2": "basin_bottom", "Q1": "lampstand_top", "Q2": "lampstand_bottom",
    "db": "dais_band", "fw": "floor_worn", "fr": "floor_rosette",
}
GLOW = "GG"  # the great hearth's 5 x 5 pool of light, filled in from GLOW_ORIGIN

ROOM = """
WL WT WT WT WT WT WT WT WT WT WT WT WT WT WT WT WR
SL Fa Fk Fp Pt Fk Ff Fp Hl Hr Fp Ff Pt Fk Dt Ff SR
SL Lw Ll Lw Pb Ll Lw Lw Lr Lw Lw Ll Pb Lw Db Lw SR
SL T1 T2 Bt .. dl Q1 dd dS dd Q1 dr .. Bt .. .. SR
SL T3 T4 bT .. dl Q2 i1 i2 i3 Q2 dr .. bD .. .. SR
SL .. .. .. .. dl db db RN db db dr .. .. .. .. SR
SL .. f1 .. Ct rl rr rr ST rr rr rR Ct .. .. .. SR
SL Am .. .. Cb .. .. Bt RC Bt .. .. Cb .. f2 Ar SR
SL Am .. .. fr .. .. bH RU bH .. .. fr .. .. .. SR
SL .. .. f2 .. fw .. .. RU .. .. fw .. .. .. Vo SR
SL .. .. .. Ct It Ih Ih RU Ih Ih Ir Ct .. .. .. SR
SL Vo f1 .. Cb Iv GG GG GG GG GG Iv Cb .. .. .. SR
SL .. .. .. fr Iv GG GG GG GG GG Iv fr .. f1 .. SR
SL .. .. .. .. Iv GG GG GG GG GG Iv .. .. .. Am SR
SL .. .. .. Ct Iv GG GG GG GG GG Iv Ct .. .. .. SR
SL f2 .. .. Cb Iv GG GG GG GG GG Iv Cb .. .. .. SR
SL L1 L2 Bt .. Ib Ih Ih RU Ih Ih IR .. Bt K1 K2 SR
SL L3 L4 bL .. .. fw .. RU .. .. .. .. bB K3 K4 SR
SL .. .. .. Ct .. .. .. RU .. fw .. Ct .. .. .. SR
SL .. .. .. Cb .. .. .. RU .. .. .. Cb .. .. .. SR
SL .. .. .. .. .. St .. RU .. P1 .. .. .. .. .. SR
SL Am Lt .. .. .. Sb fw RU fw P2 .. .. .. Lt Ar SR
SL .. Lb .. .. .. .. .. RS .. .. .. .. .. Lb .. SR
SL .. .. .. .. .. .. Ml Mm Mr .. .. .. .. .. .. SR
"""
GLOW_ORIGIN = (6, 11)  # top-left of the great hearth's 5 x 5 block

# The trial's pieces: each brazier's bowl (its legs are the tile below).
STATIONS = {"door": (13, 3), "table": (3, 3), "loom": (3, 16), "bed": (13, 16)}
DAIS_BRAZIERS = [(7, 7), (9, 7)]
CORD = (8, 7)
HYMN = ["door", "table", "loom", "bed"]  # the order the stele gives

# The floor a lit brazier warms, relative to its bowl: brazier_light's ring.
RING = {(-1, 0): "bglow_l0", (1, 0): "bglow_r0", (-1, 1): "bglow_l1", (1, 1): "bglow_r1",
        (-1, 2): "bglow_bl", (0, 2): "bglow_b", (1, 2): "bglow_br"}

DOOR = (8, 23)          # warp 0, where the player arrives
IONE_TALK = (8, 5)      # the tile south of the inner hearth's counter
# Ione's place behind the inner hearth, walled in by the lampstands: dais marble the
# player never stands on, so it gets collision like the furniture around it.
BLOCKED = {(7, 3), (9, 3)}

# After the trial: every brazier burns and the cord is gone.
LIT = {
    "brazier_top_cold": "brazier_top_lit",
    "brazier_table_cold": "brazier_table_lit", "brazier_loom_cold": "brazier_loom_lit",
    "brazier_door_cold": "brazier_door_lit", "brazier_bed_cold": "brazier_bed_lit",
    "brazier_hearth_cold": "brazier_hearth_lit", "runner_cord": "runner",
}
# Metatiles the player can walk on; everything else gets collision 1.
PASSABLE_PREFIXES = ("floor", "runner", "inlay", "glow", "bglow", "dais", "steps", "mat")
PASSABLE_EXCEPTIONS = {"runner_cord", "dais_edge_l", "dais_edge_r"}
ELEVATION = 3  # vanilla interiors use elevation 3 throughout

# Camera positions for the review views: the route a player walks, in order.
VIEWS = [
    ("entry", 8, 22), ("the stele and the basin", 7, 20), ("Lampon and the hearth", 7, 16),
    ("the Loom station", 4, 16), ("the Bed station", 12, 16), ("Pyrrha's crossing", 4, 12),
    ("the Door station", 12, 4), ("the Table station", 4, 4), ("the gate", 8, 9),
    ("Ione", 8, 5),
]


def names_grid(room=None):
    rows = [r.split() for r in (room or ROOM).strip().splitlines()]
    w = len(rows[0])
    for n, r in enumerate(rows):
        if len(r) != w:
            raise ValueError(f"ROOM row {n} is {len(r)} wide, expected {w}")
    grid = [[None if c == GLOW else LEGEND[c] for c in r] for r in rows]
    gx, gy = GLOW_ORIGIN
    for j in range(5):
        for i in range(5):
            inner = 1 <= i <= 3 and 1 <= j <= 3
            grid[gy + j][gx + i] = f"hearth_{j - 1}{i - 1}" if inner else f"glow_{j}{i}"
    return grid


def passable(name):
    return name.startswith(PASSABLE_PREFIXES) and name not in PASSABLE_EXCEPTIONS


def staged(grid, lit=(), solved=False):
    """The grid with the named stations lit, or everything lit once solved."""
    out = [row[:] for row in grid]
    cells = []
    for name in (HYMN if solved else lit):
        x, y = STATIONS[name]
        cells += [(x, y), (x, y + 1)]
    if solved:
        for x, y in DAIS_BRAZIERS:
            cells += [(x, y), (x, y + 1)]
        cells.append(CORD)
    for x, y in cells:
        out[y][x] = LIT.get(out[y][x], out[y][x])
    # Each burning brazier warms the plain floor around it.
    burning = [STATIONS[n] for n in (HYMN if solved else lit)] + (DAIS_BRAZIERS if solved else [])
    for bx, by in burning:
        for (dx, dy), name in RING.items():
            x, y = bx + dx, by + dy
            if 0 <= y < len(out) and 0 <= x < len(out[0]) and grid[y][x] == "floor":
                out[y][x] = name
    return out


def layout_blocks(grid, ids):
    """map.bin words: metatile id, collision in bits 10-11, elevation in 12-15."""
    out = []
    for y, row in enumerate(grid):
        for x, name in enumerate(row):
            v = ids[name]
            v |= (0 if passable(name) and (x, y) not in BLOCKED else 1) << 10
            v |= ELEVATION << 12
            out.append(v)
    return np.array(out, "<u2")


def border_blocks(ids):
    return np.array([ids["void"]] * 4, "<u2")


# --- The brazier scripts ----------------------------------------------------------------
# Which cells a brazier changes depends on the room (its light only falls on plain
# floor), so scripts.pory's brazier scripts are generated here, between two markers.

SCRIPT_BEGIN = "// --- Brazier scripts: generated by tools/ichor/maps/temple.py from the room. Do not edit. ---"
SCRIPT_END = "// --- End of generated brazier scripts. ---"
PREFIX = "AktiTown_TempleOfHestia_EventScript_"
LABEL = {
    "floor": "Floor", "runner": "Runner", "runner_cord": "RunnerCord",
    "brazier_top_cold": "BrazierTop_Cold", "brazier_top_lit": "BrazierTop_Lit",
    "bglow_l0": "BrazierLight_Left0", "bglow_r0": "BrazierLight_Right0",
    "bglow_l1": "BrazierLight_Left1", "bglow_r1": "BrazierLight_Right1",
    "bglow_bl": "BrazierLight_BelowLeft", "bglow_b": "BrazierLight_Below",
    "bglow_br": "BrazierLight_BelowRight",
}
for _g in ("door", "table", "loom", "bed", "hearth"):
    LABEL[f"brazier_{_g}_cold"] = f"Brazier{_g.title()}_Cold"
    LABEL[f"brazier_{_g}_lit"] = f"Brazier{_g.title()}_Lit"


def brazier_cells(grid, bowl, glyph, lit):
    """(x, y, metatile name, impassable) for one brazier and the floor it lights."""
    bx, by = bowl
    state = "lit" if lit else "cold"
    cells = [(bx, by, f"brazier_top_{state}", True), (bx, by + 1, f"brazier_{glyph}_{state}", True)]
    for (dx, dy), name in RING.items():
        x, y = bx + dx, by + dy
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == "floor":
            cells.append((x, y, name if lit else "floor", False))
    return cells


def brazier_script(grid):
    def body(cells):
        return "".join(f"    setmetatile({x}, {y}, METATILE_TempleHestia_{LABEL[n]}, {'TRUE' if b else 'FALSE'})\n"
                       for x, y, n, b in cells)

    out = [SCRIPT_BEGIN, ""]
    out.append("// Draws every brazier, its light and the cord from the trial's state.")
    out.append(f"script {PREFIX}DrawBraziers {{")
    out.append("    if (flag(FLAG_ICHOR_HEARTH_TRIAL_DONE)) {")
    for name in HYMN:
        out.append(f"        call({PREFIX}Light{name.title()})")
    out.append(f"        call({PREFIX}LightDais)")
    out.append("        return")
    out.append("    }")
    for n, name in enumerate(HYMN):
        out.append(f"    if (var(VAR_ICHOR_HEARTH_TRIAL) >= {n + 2}) {{")
        out.append(f"        call({PREFIX}Light{name.title()})")
        out.append("    } else {")
        out.append(f"        call({PREFIX}Douse{name.title()})")
        out.append("    }")
    out.append("    return")
    out.append("}")
    for name in HYMN:
        for lit, verb in ((True, "Light"), (False, "Douse")):
            out.append("")
            out.append(f"script {PREFIX}{verb}{name.title()} {{")
            out.append(body(brazier_cells(grid, STATIONS[name], name, lit)).rstrip("\n"))
            out.append("    return")
            out.append("}")
    dais = [c for bowl in DAIS_BRAZIERS for c in brazier_cells(grid, bowl, "hearth", True)]
    dais.append((CORD[0], CORD[1], "runner", False))
    out.append("")
    out.append("// The dais pair flares when the last flame goes home, and the cord burns away.")
    out.append(f"script {PREFIX}LightDais {{")
    out.append(body(dais).rstrip("\n"))
    out.append("    return")
    out.append("}")
    out.append("")
    out.append(SCRIPT_END)
    return "\n".join(out)


def spliced_script(grid):
    """scripts.pory with its generated block brought up to date."""
    text = (MAP_DIR / "scripts.pory").read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"temple: scripts.pory needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    return text[:a] + brazier_script(grid) + text[b + len(SCRIPT_END):]


# --- Checks ---------------------------------------------------------------------------

def walkable(grid, x, y):
    if not (0 <= y < len(grid) and 0 <= x < len(grid[0])) or (x, y) in BLOCKED:
        return False
    return passable(grid[y][x])


def reachable(grid, people):
    seen = {DOOR}
    todo = deque([DOOR])
    while todo:
        x, y = todo.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and n not in people and walkable(grid, *n):
                seen.add(n)
                todo.append(n)
    return seen


def metatile_labels():
    text = (ROOT / "include/constants/metatile_labels.h").read_text()
    return {k: int(v, 16) for k, v in re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)", text)}


def check(grid, ids, events):
    errors = []
    width, height = len(grid[0]), len(grid)
    people = {(o["x"], o["y"]) for o in events["object_events"]}
    solved = staged(grid, solved=True)

    for o in events["object_events"]:
        if not walkable(grid, o["x"], o["y"]):
            errors.append(f"{o['local_id']} stands on {grid[o['y']][o['x']]}")
    for w in events["warp_events"]:
        if not grid[w["y"]][w["x"]].startswith("mat"):
            errors.append(f"warp at ({w['x']},{w['y']}) is not on the door mat")
    for c in events["coord_events"]:
        if not grid[c["y"]][c["x"]].startswith("mat"):
            errors.append(f"trigger at ({c['x']},{c['y']}) is not on the door mat")

    for name, (x, y) in STATIONS.items():
        if grid[y][x] != "brazier_top_cold" or grid[y + 1][x] != f"brazier_{name}_cold":
            errors.append(f"the {name} brazier is not at ({x},{y})")

    open_room = reachable(solved, people)
    # People can move off a tile (a trainer walks up to the player), so a bg event only
    # needs a walkable neighbour reachable with the room empty.
    empty_room = reachable(solved, set())
    for b in events["bg_events"]:
        x, y = b["x"], b["y"]
        if walkable(grid, x, y):
            errors.append(f"bg event at ({x},{y}) is on walkable {grid[y][x]}")
        if not any((x + dx, y + dy) in empty_room for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            errors.append(f"bg event at ({x},{y}) can't be faced from anywhere")

    shut = reachable(grid, people)
    every = {(x, y) for y in range(height) for x in range(width) if walkable(solved, x, y)} - people
    stranded = sorted(every - open_room)
    if stranded:
        errors.append(f"walkable but unreachable from the door: {stranded}")
    if IONE_TALK in shut:
        errors.append("the dais is reachable before the cord burns away")
    if IONE_TALK not in open_room:
        errors.append("the dais is unreachable after the trial")

    # setmetatile(x, y, METATILE_..., ...) must hit a brazier or the cord with its own art.
    labels = metatile_labels()
    names = {v: k for k, v in ids.items()}
    allowed = {}
    for y, row in enumerate(grid):
        for x, name in enumerate(row):
            if name in LIT:
                allowed[(x, y)] = {name, LIT[name]}
    for bx, by in list(STATIONS.values()) + DAIS_BRAZIERS:
        for (dx, dy), light in RING.items():
            x, y = bx + dx, by + dy
            if 0 <= y < height and 0 <= x < width and grid[y][x] == "floor":
                allowed.setdefault((x, y), {"floor"}).add(light)
    script = (MAP_DIR / "scripts.pory").read_text()
    calls = re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", script)
    if not calls:
        errors.append("scripts.pory has no setmetatile calls")
    for x, y, label in calls:
        x, y = int(x), int(y)
        if label not in labels:
            errors.append(f"setmetatile uses unknown label {label}")
            continue
        target = names.get(labels[label])
        if target not in allowed.get((x, y), set()):
            errors.append(f"setmetatile({x}, {y}, {label}) puts {target} over {grid[y][x]}")
    if script != spliced_script(grid):
        errors.append("scripts.pory's brazier scripts are out of date; run tools/ichor/maps/temple.py")
    return errors


# --- Renders ----------------------------------------------------------------------------

def compiled_renderer(layout):
    render_map.read_fieldmap_constants()
    symbols = render_map.scan_tileset_symbols()
    prim = render_map.resolve_tileset(layout["primary_tileset"], symbols)
    sec = render_map.resolve_tileset(layout["secondary_tileset"], symbols)
    return render_map.Renderer(render_map.Tileset(prim), render_map.Tileset(sec))


class SourceRenderer:
    """Draws metatiles straight from temple_hestia's character grids."""

    def __init__(self):
        self.tiles = {}
        for name, bottom, middle, _ in temple_hestia.build():
            img = temple_hestia.to_rgba(bottom, True)[..., :3].copy()
            if middle is not None:
                m = temple_hestia.to_rgba(middle, False)
                mask = np.any(m[..., :3] != temple_hestia.MAGENTA, axis=2)
                img[mask] = m[..., :3][mask]
            self.tiles[name] = img

    def render(self, grid, margin=0):
        h, w = len(grid), len(grid[0])
        img = np.empty(((h + 2 * margin) * 16, (w + 2 * margin) * 16, 3), np.uint8)
        void = self.tiles["void"]
        for y in range(h + 2 * margin):
            for x in range(w + 2 * margin):
                gx, gy = x - margin, y - margin
                inside = 0 <= gx < w and 0 <= gy < h
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = self.tiles[grid[gy][gx]] if inside else void
        return Image.fromarray(img)


def scaled(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


def font(size):
    return ImageFont.load_default(size=size)


def labelled(img, text, pad=22):
    out = Image.new("RGB", (img.width, img.height + pad), (40, 40, 48))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text((6, 4), text, fill=(230, 230, 200), font=font(14))
    return out


def sheet(images, cols, gap=10, bg=(40, 40, 48)):
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), bg)
    for n, im in enumerate(images):
        r, c = divmod(n, cols)
        out.paste(im, (gap + c * (w + gap), gap + r * (h + gap)))
    return out


def screen_view(room_img_with_margin, margin, cx, cy):
    """The 240 x 160 GBA screen with the camera on tile (cx, cy): the player's tile
    sits at screen column 7, its top 72 px down."""
    x0 = (cx + margin - 7) * 16
    y0 = (cy + margin) * 16 - 72
    return room_img_with_margin.crop((x0, y0, x0 + 240, y0 + 160))


def review(name, grid, views=None):
    r = SourceRenderer()
    cold, solved = r.render(grid), r.render(staged(grid, solved=True))
    room = sheet([labelled(scaled(cold, 2), "before the trial"),
                  labelled(scaled(solved, 2), "after the trial")], 2)
    room.save(IMG / f"temple_{name}_room.png")

    margin = 8
    big = r.render(grid, margin)
    views = [labelled(scaled(screen_view(big, margin, x, y), 2), f"{label} ({x},{y})")
             for label, x, y in (views or VIEWS)]
    sheet(views, 3).save(IMG / f"temple_{name}_views.png")

    stages = [("cold", grid)]
    for n in range(1, len(HYMN) + 1):
        stages.append(("+ " + HYMN[n - 1], staged(grid, lit=HYMN[:n])))
    stages.append(("the last flame home", staged(grid, solved=True)))
    sheet([labelled(r.render(g), t, 18) for t, g in stages], len(stages)).save(IMG / f"temple_{name}_stages.png")
    return [IMG / f"temple_{name}_{k}.png" for k in ("room", "views", "stages")]


SIGHT = {"MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_UP": (0, -1),
         "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}


def events_image(base, events, s=2):
    img = scaled(base, s).convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    c = 16 * s

    def box(x, y, fill, outline):
        d.rectangle([x * c + 1, y * c + 1, x * c + c - 2, y * c + c - 2], fill=fill, outline=outline, width=2)

    for b in events["bg_events"]:
        box(b["x"], b["y"], (80, 160, 255, 60), (80, 160, 255, 220))
    for t in {(e["x"], e["y"]) for e in events["coord_events"]}:
        box(*t, (255, 220, 0, 70), (255, 220, 0, 230))
    for w in events["warp_events"]:
        d.rectangle([w["x"] * c + 6, w["y"] * c + 6, w["x"] * c + c - 7, w["y"] * c + c - 7],
                    outline=(255, 60, 200, 255), width=2)
    for o in events["object_events"]:
        x, y = o["x"], o["y"]
        if o["trainer_type"] != "TRAINER_TYPE_NONE":
            dx, dy = SIGHT[o["movement_type"]]
            for k in range(1, int(o["trainer_sight_or_berry_tree_id"]) + 1):
                box(x + dx * k, y + dy * k, (255, 60, 40, 70), (255, 60, 40, 255))
        box(x, y, (40, 220, 90, 110), (20, 120, 40, 255))
        label = o["local_id"].removeprefix("LOCALID_TEMPLE_").title()
        d.text((x * c + c // 2, y * c - 2), label, fill=(255, 255, 255, 255), font=font(11),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    img = Image.alpha_composite(img, over)

    key = [((40, 220, 90), "person"), ((255, 60, 40), "trainer sight"), ((80, 160, 255), "bg event"),
           ((255, 220, 0), "torch-out trigger"), ((255, 60, 200), "warp to Akti")]
    pad = 18
    out = Image.new("RGBA", (img.width, img.height + pad * len(key) + 8), (40, 40, 48, 255))
    out.paste(img, (0, 0))
    d = ImageDraw.Draw(out)
    for i, (col, text) in enumerate(key):
        y = img.height + 6 + i * pad
        d.rectangle([8, y, 20, y + 12], fill=col)
        d.text((28, y), text, fill=(230, 230, 200), font=font(11))
    return out.convert("RGB")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify the layout files are current")
    ap.add_argument("--review", metavar="NAME", help="write design review sheets from source art")
    args = ap.parse_args()

    grid = names_grid()
    if args.review:
        for p in review(args.review, grid):
            print(p.relative_to(ROOT))
        return

    ids = temple_hestia.catalog()
    width, height = len(grid[0]), len(grid)
    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    layout = next(l for l in layouts if l.get("id") == LAYOUT_ID)
    if (layout["width"], layout["height"]) != (width, height):
        sys.exit(f"temple: layouts.json says {layout['width']}x{layout['height']}, the room is {width}x{height}")

    blocks, border = layout_blocks(grid, ids), border_blocks(ids)
    if args.check:
        stale = [p.name for p, want in ((LAYOUT_DIR / "map.bin", blocks), (LAYOUT_DIR / "border.bin", border))
                 if not p.exists() or not np.array_equal(np.fromfile(p, "<u2"), want)]
        if stale:
            sys.exit(f"temple: {', '.join(stale)} out of date; run tools/ichor/maps/temple.py")
    else:
        blocks.tofile(LAYOUT_DIR / "map.bin")
        border.tofile(LAYOUT_DIR / "border.bin")
        (MAP_DIR / "scripts.pory").write_text(spliced_script(grid))

    events = json.loads((MAP_DIR / "map.json").read_text())
    errors = check(grid, ids, events)
    if errors:
        sys.exit("temple: " + "\n  ".join(["layout check failed:"] + errors))

    if not args.check:
        r = compiled_renderer(layout)
        cold = render_map.render_blocks(r, blocks, width)
        lit = render_map.render_blocks(r, layout_blocks(staged(grid, solved=True), ids), width)
        IMG.mkdir(parents=True, exist_ok=True)
        scaled(cold, 3).save(IMG / "temple_map.png")
        scaled(lit, 3).save(IMG / "temple_map_lit.png")
        events_image(cold, events).save(IMG / "temple_map_events.png")
    print(f"temple: {width}x{height} on {layout['primary_tileset']} + {layout['secondary_tileset']}, "
          f"{len(events['object_events'])} people, {len(events['bg_events'])} bg events; checks pass")


if __name__ == "__main__":
    main()
