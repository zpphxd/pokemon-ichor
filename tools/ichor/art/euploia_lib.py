"""Shared toolkit for gTileset_Euploia, the Euploia refitted for the post-game.

Ported from world-act1's trireme_lib.py (the ship's first life, the slice's
crossing), so she is recognisably the same ship: the same oak deck, linen sail,
bronze ram and red wale. The refit adds the living quarters below deck (the
bunk, Lampon's hearth, Kydon's stall and Pithos, the trophy shelf, Diktys's
nets) and, on deck, the chart table, Poseidon's altar, the oarsmen's benches
and the gangplank.

The ship is drawn as whole scenes, not as separate structures: the deck
(24x12 cells, bow to the east) and below deck (20x10), each in three RGBA
layers, plus variants that the scripts swap in with setmetatile (the trophy
shelf's seven keepsakes, the hearth cold). euploia_build.py slices every scene
into 16x16 cells, keeps one metatile per distinct cell, and records where each
one goes, so the map IS the scene and the variants are lists of (x, y, metatile).

Drawing uses kalliste_lib's Layer (pixels by color name). On top of that:

  - the palette plan: seven groups for the secondary's palettes 6-12. Every
    8x8 tile of every layer draws from one group; validate() enforces it;
  - borrowed sea: a cell can sit on aethos's animated sea (0x170). Its bottom
    layer stays empty, the build points it at aethos's sea tiles, and the cell
    keeps one layer of art above the water;
  - per-cell collision, behavior and named pieces for the catalog.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT
CELL = 16

# --------------------------------------------------------------------------
# Colors: kalliste's names, plus the trireme's, plus the refit's
# --------------------------------------------------------------------------

NEW = {
    # the deck: sun-bleached oak planks (wd1 is the seam, wd0/ink the hull)
    "pk1": (160, 120, 72), "pk2": (192, 152, 96), "pk3": (216, 184, 128), "pk4": (240, 216, 168),
    "rd0": (120, 40, 32),
    # linen sail; the papyrus of the chart
    "ln1": (240, 232, 208), "ln2": (216, 200, 168), "ln3": (184, 168, 136), "ln4": (136, 120, 96),
    # rope in shadow, sacking
    "rp1": (176, 152, 104),
    # below deck: the dark under the deck, lamplight
    "hd0": (48, 32, 24), "lt1": (224, 184, 112),
    # the lotus on the trophy shelf
    "pn1": (232, 144, 168), "pn2": (176, 80, 112),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # the ship's timber: deck planks, bulwarks, the hull's side, the mast, the
    # stern timbers, the benches and the gangplank, bronze shields, the eye and
    # the wale (as world-act1's trireme)
    "wood": ["ink", "wd0", "wd1", "pk1", "pk2", "pk3", "pk4", "rp", "rd", "rd0", "br", "g0",
             "g1", "w0", "b1"],
    # where the ship meets the sea: waterline foam, shadow on the water, the
    # ram, the steering oars' blades
    "water": ["ink", "wd0", "wd1", "pk2", "pk3", "br", "g0", "g1", "b0", "b1", "wr", "b2",
              "b3", "w0", "rd"],
    # the linen sail, its yard and ropes; the chart table and its papyrus
    "sail": ["ink", "w0", "ln1", "ln2", "ln3", "ln4", "rd", "rd0", "wd0", "wd1", "pk2", "rp",
             "rp1", "b1", "g1"],
    # cargo: amphorae, the Pithos, the stall's goods and awning, Diktys's nets,
    # coiled rope, the mess's bowls, Iaso's chest
    "cargo": ["ink", "w0", "tc0", "tc1", "tc2", "tc3", "wd0", "wd1", "pk2", "pk3", "rp",
              "rp1", "rd", "ol1", "ol2"],
    # Poseidon's altar (marble, blue paint, the bronze trident) and the trophy
    # shelf with its seven keepsakes
    "shrine": ["ink", "w0", "m2", "m3", "m4", "b1", "b2", "g0", "g1", "br", "wd0", "wd1",
               "pn1", "pn2", "ol2"],
    # below deck: dark timber, lamplight, the bunk and its fleece and blanket
    "hold": ["ink", "hd0", "wd0", "wd1", "pk1", "pk2", "pk3", "fc", "lt1", "rd", "rd0", "b0",
             "b1", "rp", "w0"],
    # Hestia's fire: the hearth, its clay hood and pot, the flames; the ladder
    # and the daylight down the hatch
    "hearth": ["ink", "hd0", "wd0", "wd1", "pk1", "pk2", "pk3", "fc", "lt1", "tc0", "tc1",
               "tc2", "rp", "fl", "g1"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

SEA = 0x170                  # aethos's open sea (animated), MB_OCEAN_WATER


def h(x, y, salt=0, period=32):
    """A stable pseudo-random number in [0, 1) that repeats every `period` px."""
    x %= period
    y %= period
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return (v ^ (v >> 16)) % 1000 / 1000


# --------------------------------------------------------------------------
# Scenes
# --------------------------------------------------------------------------

class Scene:
    """A map-sized picture in three layers, with per-cell collision, behavior,
    ground and named pieces.

    walk[y][x]: 'X' solid, '.' walkable, '~' open sea (aethos 0x170 if the
    cell has no art; solid either way), 'w' a warp (the hatch, the ladder),
    'c' a counter (solid, MB_COUNTER: talk across it).
    """

    def __init__(self, key, w, h):
        self.key, self.w, self.h = key, w, h
        self.layers = {n: Layer(w * CELL, h * CELL) for n in ("bottom", "middle", "top")}
        self.walk = [["X"] * w for _ in range(h)]
        self.beh = {}        # (x, y) -> "MB_..."
        self.ground = {}     # (x, y) -> "sea"
        self.pieces = []     # dicts: key, title, x, y, w, h, notes

    @property
    def B(self):
        return self.layers["bottom"]

    @property
    def M(self):
        return self.layers["middle"]

    @property
    def T(self):
        return self.layers["top"]

    def copy(self, key):
        s = copy.deepcopy(self)
        s.key = key
        return s

    def cell(self, layer, x, y):
        return self.layers[layer].a[y * CELL:(y + 1) * CELL, x * CELL:(x + 1) * CELL]

    def piece(self, key, title, x, y, w, h, notes=""):
        self.pieces.append({"key": key, "title": title, "x": x, "y": y, "w": w, "h": h,
                            "notes": notes})

    def set_walk(self, x, y, code, beh=None):
        self.walk[y][x] = code
        if beh:
            self.beh[(x, y)] = beh

    def clear_cell(self, x, y):
        for layer in self.layers.values():
            layer.a[y * CELL:(y + 1) * CELL, x * CELL:(x + 1) * CELL] = 0

    def flatten(self):
        """Porytiles' dual-layer mode allows two drawn layers per metatile.
        Where a dry cell draws all three, the middle merges into the bottom;
        on borrowed sea the bottom must stay empty, so middle merges into top."""
        for y in range(self.h):
            for x in range(self.w):
                b, m, t = (self.cell(n, x, y) for n in ("bottom", "middle", "top"))
                used = [(a[..., 3] > 0).any() for a in (b, m, t)]
                if self.ground.get((x, y)) == "sea":
                    if used[1] and used[2]:
                        mm = m[..., 3] > 0
                        keep = t[..., 3] == 0
                        t[mm & keep] = m[mm & keep]
                        m[:] = 0
                    continue
                if all(used):
                    mm = m[..., 3] > 0
                    b[mm] = m[mm]
                    m[:] = 0


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(scene):
    problems = []
    for ln, layer in scene.layers.items():
        for ty in range(scene.h * 2):
            for tx in range(scene.w * 2):
                if ln == "bottom" and scene.ground.get((tx // 2, ty // 2)) == "sea":
                    continue
                cols = tile_colors(layer, tx, ty)
                if not cols:
                    continue
                if not any(cols <= g for g in GROUP_RGB.values()):
                    names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                    problems.append(f"{scene.key} {ln} tile ({tx},{ty}) cell ({tx // 2},{ty // 2}) "
                                    f"mixes groups: {names}")
    for y in range(scene.h):
        for x in range(scene.w):
            used = [(scene.cell(n, x, y)[..., 3] > 0).any() for n in ("bottom", "middle", "top")]
            if all(used):
                problems.append(f"{scene.key} cell ({x},{y}) has three layers")
            if scene.ground.get((x, y)) == "sea":
                if used[0]:
                    problems.append(f"{scene.key} cell ({x},{y}) on borrowed sea draws a bottom")
                if used[1] and used[2]:
                    problems.append(f"{scene.key} cell ({x},{y}) on borrowed sea uses both upper layers")
                continue
            if any(used):
                lower = np.maximum(scene.cell("bottom", x, y)[..., 3], scene.cell("middle", x, y)[..., 3])
                if not (lower > 0).all():
                    problems.append(f"{scene.key} cell ({x},{y}) has holes below the sprites layer")
    return problems


# --------------------------------------------------------------------------
# Previews with the real aethos sea
# --------------------------------------------------------------------------

_AETHOS = {}


def aethos_metatile(mid):
    """16x16 RGB of an aethos metatile (both layers), for previews."""
    if mid not in _AETHOS:
        sys.path.insert(0, str(ROOT / "tools/ichor"))
        import render_map as R
        R.read_fieldmap_constants()
        sy = R.scan_tileset_symbols()
        r = R.Renderer(R.Tileset(sy["gTileset_Aethos"]), R.Tileset(sy["gTileset_Akti"]))
        _AETHOS[mid] = r.metatile(mid)[0]
    return _AETHOS[mid]


def composite(scene, void=(0, 0, 0)):
    """The scene as it will look in game: borrowed sea, then its layers. Cells
    with nothing drawn and no ground show `void` (below deck's dark)."""
    out = np.zeros((scene.h * CELL, scene.w * CELL, 3), np.uint8)
    out[:] = void
    for (x, y), kind in scene.ground.items():
        out[y * CELL:(y + 1) * CELL, x * CELL:(x + 1) * CELL] = aethos_metatile(SEA)
    for ln in ("bottom", "middle", "top"):
        a = scene.layers[ln].a
        m = a[..., 3] > 0
        out[m] = a[..., :3][m]
    return out


def save_preview(scene, path, scale=2, void=(0, 0, 0), grid=False):
    from PIL import Image, ImageDraw
    im = Image.fromarray(composite(scene, void)).resize(
        (scene.w * CELL * scale, scene.h * CELL * scale), Image.NEAREST)
    if grid:
        d = ImageDraw.Draw(im)
        c = CELL * scale
        for x in range(scene.w + 1):
            d.line([x * c, 0, x * c, scene.h * c], fill=(255, 255, 255), width=1)
        for y in range(scene.h + 1):
            d.line([0, y * c, scene.w * c, y * c], fill=(255, 255, 255), width=1)
        for y in range(scene.h):
            for x in range(scene.w):
                d.text((x * c + 2, y * c + 1), f"{x},{y}", fill=(255, 255, 0))
    im.save(path)
    return path
