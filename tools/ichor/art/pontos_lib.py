"""Shared toolkit for gTileset_Pontos, the Black Sea's outdoor secondary.

The Black Sea (OIKOUMENE.md §4.3, §7): a dark green sea under low cloud, white
cliffs, Colchian timber and Aietes's bronze. Pontos draws with kalliste_lib's
Layer and Struct, like every Ichor secondary, and adds:

  - The palette plan. Porytiles packs six groups into slots 6-11; validate()
    makes every 8x8 tile draw from one group. "kyanean" is "chalk" slot for
    slot with the rock ramp darkened, so a white cliff piece recolored to the
    Clashing Rocks' blue-black is the same 4bpp tile in another palette.
  - Slot 12, the Pontic sea, is not packed: pontos_build.py writes it as
    aethos's sea palette (slot 5) with every blue turned dark sea green. Any
    pontos metatile that points at aethos's water tiles with palette 12 shows
    aethos's animated water, recolored, for no tiles at all. Ground kind "psea"
    is that water under a drawn piece; DERIVED pieces are whole aethos water
    metatiles (the open sea, the beach edges, rocks in the sea) re-pointed the
    same way.
  - Ground per cell, as emporion_lib: "grass", "sand", "path" and "psea" borrow
    aethos's ground (the build points the bottom layer at it); "quay" and
    "none" are drawn.

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
SEC = "pontos"

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # chalk: the Pontic coast's white cliffs, its quays and paving
    "ck4": (224, 224, 208), "ck3": (192, 192, 176), "ck2": (152, 152, 144), "ck1": (112, 112, 112),
    "ck0": (72, 72, 80),
    # kyanean: the Clashing Rocks' blue-black, the same ramp darkened
    "ky4": (144, 160, 184), "ky3": (104, 120, 152), "ky2": (72, 88, 120), "ky1": (48, 56, 88),
    "ky0": (40, 40, 64),
    # what both rock groups share: foam, weed, the wet foot, aethos's grass and sand
    "pf": (160, 200, 184), "wg": (56, 96, 72), "wt": (40, 56, 56),
    "gr0": (184, 184, 104), "gr1": (144, 152, 72), "gr2": (208, 200, 128), "gs": (112, 128, 64),
    "sn": (232, 208, 144),
    # bronze, Hephaestus's work, and what runs in his fountains
    "bz0": (72, 40, 24), "bz1": (120, 72, 24), "bz2": (176, 112, 40), "bz3": (224, 160, 72),
    "bz4": (248, 216, 136), "vd0": (32, 88, 80), "vd1": (72, 144, 120), "mk": (216, 216, 200),
    "wn0": (104, 24, 48), "wn1": (168, 48, 72), "oil": (240, 200, 80), "wa": (96, 160, 208),
    "fire": (216, 72, 32),
    # timber: Colchian log houses, Thracian thatch, docks and boats
    "wd4": (240, 208, 152), "th0": (112, 96, 48), "th1": (168, 144, 72), "th2": (216, 192, 112),
    "cl0": (136, 88, 56), "cl1": (184, 136, 96), "sh": (40, 40, 48),
    # flora: the wet Pontic woods, the Phasis's reeds, vines
    "fg0": (24, 48, 32), "fg1": (40, 80, 48), "fg2": (72, 120, 64), "fg3": (120, 168, 88),
    "fg4": (168, 200, 120), "tr0": (72, 56, 40), "tr1": (112, 88, 64), "rd0": (152, 128, 64),
    "rd1": (200, 176, 96), "bry": (192, 56, 72),
    # accent: linen and its dyes, the dove, Ares's black stone, feathers, banners
    "gy1": (176, 176, 184), "gy0": (104, 104, 112), "blk": (48, 40, 48), "saf": (232, 176, 48),
    "saf2": (176, 112, 32), "ind": (56, 64, 136), "ind2": (96, 112, 184), "mad": (168, 40, 48),
    "mad2": (216, 96, 88), "crm": (240, 224, 184), "tan": (184, 144, 104),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "chalk": ["ink", "w0", "ck4", "ck3", "ck2", "ck1", "ck0", "pf", "wg", "wt", "gr0", "gr1",
              "gr2", "gs", "sn"],
    "kyanean": ["ink", "w0", "ky4", "ky3", "ky2", "ky1", "ky0", "pf", "wg", "wt", "gr0", "gr1",
                "gr2", "gs", "sn"],
    "bronze": ["ink", "bz0", "bz1", "bz2", "bz3", "bz4", "w0", "vd0", "vd1", "mk", "wn0", "wn1",
               "oil", "wa", "fire"],
    "timber": ["ink", "wd0", "wd1", "wd2", "wd3", "wd4", "th0", "th1", "th2", "cl0", "cl1", "rp",
               "w0", "rd", "sh"],
    "flora": ["ink", "fg0", "fg1", "fg2", "fg3", "fg4", "gr0", "gr1", "gr2", "gs", "tr0", "tr1",
              "rd0", "rd1", "bry"],
    "accent": ["ink", "w0", "gy1", "gy0", "blk", "saf", "saf2", "ind", "ind2", "mad", "mad2",
               "crm", "tan", "wd1", "wd2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# chalk -> kyanean: the dark rock is the white cliff, slot for slot
DARK = dict(zip(GROUPS["chalk"], GROUPS["kyanean"]))

# --------------------------------------------------------------------------
# The Pontic sea: palette 12, aethos's sea palette with the blues turned green
# --------------------------------------------------------------------------

SEA_SLOT = 12
AETHOS_SEA_SLOT = 5
# aethos palette 5 index -> the Black Sea's color (indices not listed keep aethos's)
PONTIC = {
    3: (168, 208, 184),    # the glint on a wave
    6: (64, 120, 104),     # ripples
    7: (16, 48, 48),       # the deep
    9: (104, 160, 136),    # light ripples
    10: (40, 88, 80),      # the water's body
    15: (80, 144, 120),    # the shallows over rock
}


def aethos_palette(n):
    p = ROOT / f"data/tilesets/primary/aethos/porytiles_bin/palettes/{n:02d}.pal"
    v = [int(t) for t in p.read_text().split()[3:]]
    return [tuple(v[k * 3:k * 3 + 3]) for k in range(16)]


def pontic_palette():
    pal = list(aethos_palette(AETHOS_SEA_SLOT))
    for i, c in PONTIC.items():
        assert all(x % 8 == 0 for x in c)
        pal[i] = c
    return pal


GROUND_METATILE = {"grass": 0x001, "sand": 0x124, "path": 0x1D9, "psea": 0x170, "tall": 0x00D}
BORROWED = set(GROUND_METATILE)
DRAWN = {"quay", "none"}


# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------

class Struct(K.Struct):
    """A kalliste Struct with a ground kind per cell (see the module docstring).

    derived: for a whole aethos metatile re-pointed at the Pontic sea, its aethos
    id; such a structure draws nothing and costs no tiles."""

    def __init__(self, key, title, w, h, walk=None, notes="", ground="none", section=SEC,
                 derived=None):
        super().__init__(key, title, w, h, section, walk=walk, notes=notes)
        self.ground = {}
        self.derived = derived
        self.names = {}
        self.set_ground(ground)

    def set_ground(self, kind, cells=None):
        cells = cells if cells is not None else [(x, y) for y in range(self.h) for x in range(self.w)]
        for c in cells:
            assert kind in BORROWED | DRAWN, kind
            self.ground[c] = kind

    def name(self, part, cx, cy=0):
        self.names[part] = (cx, cy)

    @property
    def borrowed(self):
        if self.derived is not None:
            return {}
        return {c: k for c, k in self.ground.items() if k in BORROWED}


def derived(key, title, aethos_ids, walk, notes=""):
    """A row of aethos water metatiles re-pointed at the Pontic sea."""
    ids = aethos_ids if isinstance(aethos_ids[0], (list, tuple)) else [aethos_ids]
    s = Struct(key, title, len(ids[0]), len(ids), walk=walk, notes=notes, derived=ids)
    return s


def recolor(s: Struct, mapping, key=None, title=None, notes=None):
    """A copy of s with colors swapped by name (e.g. DARK: chalk -> kyanean)."""
    t = copy.deepcopy(s)
    if key:
        t.key = key
    if title:
        t.title = title
    if notes is not None:
        t.notes = notes
    rgb = {C[a]: C[b] for a, b in mapping.items()}
    for layer in t.layers.values():
        flat = layer.a.reshape(-1, 4)
        for i in np.nonzero(flat[:, 3])[0]:
            c = tuple(int(v) for v in flat[i, :3])
            if c in rgb:
                flat[i, :3] = rgb[c]
    return t


def mirror(s: Struct, key, title=None, notes=None):
    """s flipped left to right (walk, behaviors, ground and part names follow)."""
    t = copy.deepcopy(s)
    t.key = key
    t.title = title or s.title + " (mirrored)"
    if notes is not None:
        t.notes = notes
    for layer in t.layers.values():
        layer.a[:] = layer.a[:, ::-1].copy()
    t.walk = [row[::-1] for row in t.walk]
    t.behaviors = {(t.w - 1 - x, y): mb for (x, y), mb in t.behaviors.items()}
    t.ground = {(t.w - 1 - x, y): g for (x, y), g in t.ground.items()}
    t.names = {n: (t.w - 1 - x, y) for n, (x, y) in t.names.items()}
    return t


def finish(s: Struct):
    """Paint drawn ground under the art and flatten cells that drew in both upper
    layers (their middle layer goes into the bottom, which holds the ground)."""
    B, M, T = s.B, s.M, s.T
    for (cx, cy), kind in s.ground.items():
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        if kind == "quay":
            ground = Layer(16, 16)
            quay_paving(ground, 0, 0, 16, 16)
            old = B.a[sl].copy()
            B.a[sl] = ground.a
            m = old[..., 3] > 0
            B.a[sl][m] = old[m]
        if kind in BORROWED:
            continue
        hasM = (M.a[sl][..., 3] > 0).any()
        hasT = (T.a[sl][..., 3] > 0).any()
        if hasM and hasT:
            src = M.a[sl]
            m = src[..., 3] > 0
            B.a[sl][m] = src[m]
            M.a[sl] = 0
    return s


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(structs):
    problems = []
    for s in structs:
        if s.derived is not None:
            continue
        gr = s.borrowed
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if not cols:
                        continue
                    if not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                if (cx, cy) in gr:
                    if (s.B.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has holes below the sprites layer")
    return problems


# --------------------------------------------------------------------------
# aethos metatiles as pixels, with the Pontic sea where they use palette 5
# --------------------------------------------------------------------------

_AETHOS = {}


def _aethos_data():
    if "tiles" not in _AETHOS:
        from PIL import Image
        base = ROOT / "data/tilesets/primary/aethos/porytiles_bin"
        a = np.array(Image.open(base / "tiles.png"))
        w = a.shape[1] // 8
        tiles = [a[(i // w) * 8:(i // w) * 8 + 8, (i % w) * 8:(i % w) * 8 + 8] % 16
                 for i in range((a.shape[0] // 8) * w)]
        _AETHOS["tiles"] = tiles
        _AETHOS["meta"] = np.fromfile(base / "metatiles.bin", "<u2").reshape(-1, 8)
        _AETHOS["attrs"] = np.fromfile(base / "metatile_attributes.bin", "<u2")
        pals = [aethos_palette(n) for n in range(6)]
        _AETHOS["pals"] = pals
    return _AETHOS


def aethos_entries(mid, pontic=True):
    """aethos metatile `mid`'s eight entries, with palette 5 re-pointed at 12."""
    ent = [int(e) for e in _aethos_data()["meta"][mid]]
    if pontic:
        ent = [(e & 0x0FFF) | (SEA_SLOT << 12) if (e >> 12) == AETHOS_SEA_SLOT else e for e in ent]
    return ent


def aethos_attr(mid):
    return int(_aethos_data()["attrs"][mid])


def render_entries(entries):
    """16x16 RGB of a metatile from entries into aethos's tiles (and palette 12)."""
    d = _aethos_data()
    pals = list(d["pals"]) + [None] * 7
    pals[SEA_SLOT] = pontic_palette()
    out = np.zeros((16, 16, 3), np.uint8)
    out[:] = pals[0][0]
    for layer in (0, 1):
        for q in range(4):
            e = entries[layer * 4 + q]
            tile, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            if tile >= 512 or pals[pal] is None:
                continue
            t = d["tiles"][tile]
            if hf:
                t = t[:, ::-1]
            if vf:
                t = t[::-1, :]
            x0, y0 = (q % 2) * 8, (q // 2) * 8
            for yy in range(8):
                for xx in range(8):
                    c = int(t[yy, xx])
                    if c == 0 and layer == 1:
                        continue
                    if c == 0:
                        continue
                    out[y0 + yy, x0 + xx] = pals[pal][c]
    return out


def aethos_metatile(mid, pontic=True):
    key = (mid, pontic)
    if key not in _AETHOS:
        _AETHOS[key] = render_entries(aethos_entries(mid, pontic))
    return _AETHOS[key]


def aethos_grass_pixels():
    """aethos's plain grass (0x001) as color names, 16x16, to continue it in a piece."""
    rgb = aethos_metatile(0x001, pontic=False)
    return [[K.RGB2NAME[tuple(int(v) for v in rgb[y, x])] for x in range(16)] for y in range(16)]


def composite(s: Struct):
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    if s.derived is not None:
        for cy, row in enumerate(s.derived):
            for cx, mid in enumerate(row):
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos_metatile(mid)
        return out
    gr = s.borrowed
    for (cx, cy), kind in gr.items():
        out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos_metatile(GROUND_METATILE[kind])
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        m = a[..., 3] > 0
        if ln == "bottom":
            for (cx, cy) in gr:
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        out[m] = a[..., :3][m]
    return out


def preview(structs, scale=2, bg=(40, 40, 48), cols=5):
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key, Image.fromarray(composite(s)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                         Image.NEAREST)) for s in structs]
    rows, cur, curw = [], [], 0
    maxw = cols * (16 * 5 * scale + pad)
    for k, i in imgs:
        if cur and curw + max(i.width, 80) + pad > maxw:
            rows.append(cur)
            cur, curw = [], 0
        cur.append((k, i))
        curw += max(i.width, 80) + pad
    if cur:
        rows.append(cur)
    width = max(sum(max(i.width, 80) + pad for _, i in r) for r in rows) + pad
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, i in r:
            d.text((x, y), key[:16], fill=(230, 230, 200))
            out.paste(i, (x, y + 12))
            x += max(i.width, 80) + pad
        y += max(i.height for _, i in r) + pad + 12
    return out


# --------------------------------------------------------------------------
# Painters
# --------------------------------------------------------------------------

def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def quay_paving(L, x0, y0, w, h, ox=0, oy=0):
    """Gray Pontic stone in courses: big blocks in a running bond, lit along their
    tops, soft joints. Repeats every 16 px (chalk group)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            row = Y // 8
            bx, by = (X + (0 if row == 0 else 8)) % 16, Y % 8
            if by == 7 or bx == 15:
                c = "ck1"
            elif by == 0:
                c = "ck4"
            else:
                c = "ck3"
                if (bx, by, row) in ((4, 3, 0), (11, 5, 0), (2, 4, 1), (9, 2, 1)):
                    c = "ck2"
            L.px(x, y, c)


def logs(L, x0, y0, w, h, course=4, ends=None):
    """Colchian log walls (Vitruvius 2.1.4): round logs laid flat, one course every
    `course` px, each lit along its top and shaded below, with a dark chink. Ends:
    (left, right) booleans for the crossed log ends at the corners."""
    for y in range(y0, y0 + h):
        Y = (y - y0) % course
        for x in range(x0, x0 + w):
            if Y == 0:
                c = "wd3"
            elif Y == course - 1:
                c = "wd0"
            elif Y == course - 2:
                c = "wd1"
            else:
                c = "wd2"
                if ((x % 16) * 7 + ((y - y0) // course % 2) * 5) % 11 == 0:
                    c = "wd1"
            L.px(x, y, c)
    if ends:
        for side, on in zip((x0 - 1, x0 + w), ends):
            if not on:
                continue
            for y in range(y0, y0 + h, course):
                L.blit(["kk", "ec", "ck"][:course - 1] if course < 4 else ["ccc", "ced", "cdd", "kkk"][:course],
                       {"k": "wd0", "e": "wd4", "c": "wd3", "d": "wd2"}, side - (1 if side > x0 else 1), y)


def thatch(L, x0, y0, w, h, ox=0):
    """Reed thatch, combed downward in tufts: light, mid and dark streaks. The
    pattern repeats every 8 px both ways, so a long roof costs few tiles."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 8, y % 8
            c = "th1"
            if X in (0, 5):
                c = "th0" if (X + Y) % 3 else "th1"
            elif X in (2, 3):
                c = "th2" if (Y + X) % 4 else "th1"
            elif (X * 3 + Y) % 7 == 0:
                c = "th0"
            L.px(x, y, c)


def outline_box(L, x, y, w, h, c="ink"):
    L.hline(x, x + w - 1, y, c)
    L.hline(x, x + w - 1, y + h - 1, c)
    L.vline(x, y, y + h - 1, c)
    L.vline(x + w - 1, y, y + h - 1, c)


def mirror_half(L, x0, w, y0, y1):
    """Copy the left half of the box over its right half, flipped."""
    h = w // 2
    left = L.a[y0:y1, x0:x0 + h].copy()
    L.a[y0:y1, x0 + w - h:x0 + w] = left[:, ::-1]
