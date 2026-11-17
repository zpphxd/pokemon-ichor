"""The karst cave the Labyrinth was cut into (design/LABYRINTH_MAZE.md §1, §4).

Daedalus built the house into the limestone caves under Knossa, and in Rings
I-IV the cave breaks through the masonry. This module gives `labyrinth` its
natural cave pieces:

- the cave rock: cave_dark's rock with depth (a 3/4 view, two-cell faces of
  flowstone flutes, rim-lit tops, outer and inner corners in every direction),
  redrawn in the house's own limestone ramp, so the masonry reads as cut from
  the same rock;
- the cave floor: packed earth and gravel (MB_CAVE, so the wild things live
  here and not in the built corridors), each with Ariadne's thread twins;
- still water (the underground stream, LABYRINTH_MAZE.md §3) and a chasm, the
  same regions drawn as a black drop with earth lips, with a timber beam
  bridge across it (thread twins too);
- formations: stalagmites, a tall one, a column where stalactite and
  stalagmite meet, boulders, roof-fall, low ledges, a hole down, a seep;
- the breach: the house's signature piece, dressed ashlar breaking into raw
  rock, and the rubble of a collapsed wall.

The cave pieces reuse cave_dark's drawing (tools/ichor/art/cave_dark_kit.py,
cave_dark_props.py) recolored into this tileset's palettes: the rock into the
`stone` ramp, the floor, water and chasm into the new `cave` group.
"""
from __future__ import annotations

import numpy as np

import cave_dark_kit as CK
import cave_dark_lib as CL
import cave_dark_props as CP
import labyrinth_art as A
import labyrinth_kit as KIT
from labyrinth_art import Struct

SEC = "cave"

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # the cave group: packed red-brown Cretan earth, the stream, moss
    "cv0": (24, 16, 16), "ce1": (56, 40, 32), "ce2": (80, 64, 48), "ce3": (112, 88, 64),
    "ce4": (144, 112, 80), "ce5": (184, 152, 112),
    "cw0": (8, 24, 40), "cw1": (16, 40, 64), "cw2": (24, 64, 96), "cw3": (48, 104, 128),
    "cw4": (88, 152, 168), "cw5": (168, 216, 216),
    "ca1": (48, 80, 48), "ca2": (96, 128, 72),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, _n
    A.C[_n] = _c
    A.K.RGB2NAME.setdefault(_c, _n)

# cave_dark's names -> ours
# (the rock is the house's own limestone ramp; the wet flowstone streaks take its
# cool dawn-light greys)
ROCK = {"k0": "lk", "k1": "lk", "k2": "ls1", "k3": "ls2", "k4": "ls3", "k5": "ls4",
        "k6": "ls5", "k7": "ls6", "k8": "ls6", "tl1": "ld0", "tl2": "ld1", "f3": "ls2",
        "wh": "ls6", "ch1": "ls3", "ch2": "ls5"}
EARTH = {"k0": "cv0", "f0": "cv0", "f1": "cv0", "f2": "ce1", "f3": "ce2", "f4": "ce3",
         "f5": "ce4", "f6": "ce5", "pd1": "cw1", "pd2": "cw3", "mn1": "ce3", "mn2": "ce4",
         "dl": "ce5", "ch1": "ce3", "ch2": "ce4"}
WATER = {"k0": "cv0", "w0": "cw0", "w1": "cw1", "w2": "cw2", "w3": "cw3", "w4": "cw4",
         "w5": "cw5", "f1": "cv0", "f2": "ce1", "f3": "ce2", "f4": "ce3", "al1": "ca1",
         "al2": "ca2", "an": "ca2", "sf": "ce4"}
# the chasm: the water's banks and shapes, its water a black drop
PIT = {**WATER, "w0": "cv0", "w1": "cv0", "w2": "cv0", "w3": "ce1", "w4": "ce1", "w5": "ce2"}
# props stand on the cave floor and are drawn in rock colors
PROP = {**EARTH, **{k: v for k, v in ROCK.items() if k.startswith("k") and k != "k0"},
        "k0": "lk", "tl1": "ld0", "tl2": "ld1", "wh": "ls6"}

# this tileset's seven palettes (labyrinth_art.groups_for)
GROUPS = {
    "stone": A.GROUPS["stone"],

    "cave": ["cv0", "ce1", "ce2", "ce3", "ce4", "ce5", "cw0", "cw1", "cw2", "cw3", "cw4",
             "cw5", "ca1", "ca2"],
}


def recolor(a, table):
    """An RGBA array with cave_dark's named colors swapped for ours."""
    out = a.copy()
    rgb = out[..., :3]
    opaque = out[..., 3] > 0
    for src, dst in table.items():
        s = np.array(CL.C[src], np.uint8)
        m = opaque & (rgb == s).all(-1)
        rgb[m] = A.C[dst]
    return out


def _check(a, table, what):
    left = {tuple(int(v) for v in p) for p in a[a[..., 3] > 0][:, :3]} - {A.C[v] for v in table.values()}
    assert not left, (what, [CL.RGB2NAME.get(c, c) for c in left])


def _paste(table, cell):
    def paint(L, x0, y0):
        a = recolor(cell, table)
        _check(a, table, "floor")
        L.a[y0:y0 + 16, x0:x0 + 16] = a
    return paint


# --------------------------------------------------------------------------
# The rock and the regions
# --------------------------------------------------------------------------

FLUTES = ["A", "C"]          # two flute variants are enough at this size
CK.FLUTE_SETS["labyrinth"] = (FLUTES, FLUTES)


def _grid(key, title, cells, walk_of, beh_of, table, notes):
    n = len(cells)
    h = (n + 7) // 8
    s = Struct(key, title, 8, h, walk=["X" * 8] * h, section=SEC, notes=notes)
    s.names = {}
    s.behaviors = getattr(s, "behaviors", {})
    walk = [list(r) for r in s.walk]
    for i, (name, a) in enumerate(cells):
        cx, cy = i % 8, i // 8
        r = recolor(a, table)
        _check(r, table, name)
        s.B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = r
        s.names[name] = (cx, cy)
        walk[cy][cx] = walk_of(name)
        b = beh_of(name)
        if b:
            s.behaviors[(cx, cy)] = b
    for i in range(n, h * 8):
        cx, cy = i % 8, i // 8
        s.B.rect(cx * 16, cy * 16, 16, 16, "lk")
    s.walk = ["".join(r) for r in walk]
    return s


def rock():
    cells = []
    for key, (N, W, E, nubs) in CK.mass_keys():
        cells.append((key, CK.mass_cell(N, W, E, nubs)))
    for kind in ("ft", "fb"):
        for l in FLUTES + ["end", "inner"]:
            for r in FLUTES + ["end", "inner"]:
                cells.append((f"{kind}|{l}|{r}", CK.face_cell(kind, l, r)))
    return _grid("cave_rock", "Cave rock: the karst the house was cut into", cells,
                 lambda n: "X", lambda n: None, ROCK,
                 "The cave's rock in 3/4 view, an autotile (`labyrinth_tiles.cave_autotile`): "
                 "`T|...` tops (sides open to floor, inner-corner nubs), and two-cell faces, "
                 "`ft|l|r` over `fb|l|r`, whose ends are `end` (an outer corner), `inner` (the "
                 "rock turns down beside it) or a flute. Drawn in the house's limestone ramp, so "
                 "dressed walls and raw cave are one stone. All block.")


def regions():
    keys = [(k, v) for k, v in CK.region_keys(CK.water_key) if len(v[4]) <= 1]   # rarer nubs fall back
    water = [(k, CK.water_cell(N, S, W, E, nubs)) for k, (N, S, W, E, nubs) in keys]
    pit = [("pit" + k[5:], CK.water_cell(N, S, W, E, nubs)) for k, (N, S, W, E, nubs) in keys]
    w = _grid("cave_water", "The underground stream: still water", water,
              lambda n: ".", lambda n: "MB_POND_WATER", WATER,
              "Still water with earth banks, a region autotile (`water|NSWE|nubs`): the stream "
              "that runs down through the house (LABYRINTH_MAZE.md §3). Surf with Poseidon's "
              "Conch; fish it.")
    p = _grid("cave_pit", "A chasm: the drop into the dark", pit,
              lambda n: "X", lambda n: None, PIT,
              "The same region shapes as the water, the water a black drop between earth lips "
              "(`pit|NSWE|nubs`). Blocks; cross it on `cave_floors` `beam_h` / `beam_v`.")
    return [w, p]


def _beam(vertical):
    def paint(L, x0, y0):
        a = recolor(CK.water_cell(False, False, False, False), PIT)
        L.a[y0:y0 + 16, x0:x0 + 16] = a
        # two squared timbers lashed side by side, a rope at each end
        for i in range(16):
            for j in range(3, 13):
                c = "ce4" if j in (3, 8) else ("ce2" if j in (7, 12) else "ce3")
                if j in (5, 10) and i % 6 == 2:
                    c = "ce2"
                x, y = (j, i) if vertical else (i, j)
                L.a[y0 + y, x0 + x] = (*A.C[c], 255)
        for e in (1, 14):
            for j in range(3, 13):
                x, y = (j, e) if vertical else (e, j)
                L.a[y0 + y, x0 + x] = (*A.C["ce5"], 255)
    return paint


def floors():
    return KIT.thread_block(
        "cave_floors", "Cave floors: earth, gravel and the beam bridges, with their thread twins",
        [("earth", _paste(EARTH, CK.floor_cell()), None, "MB_CAVE"),
         ("gravel", _paste(EARTH, CK.floor_cell(rows=CK.FLOOR2)), None, "MB_CAVE"),
         ("beam_h", _beam(False), None, "MB_NORMAL"),
         ("beam_v", _beam(True), None, "MB_NORMAL")],
        section=SEC,
        notes="The cave's walkable floors, each followed by its ten thread twins (the engine's "
              "order, as `thread`): `earth`, packed red-brown earth, and `gravel`, the same "
              "with scattered stones (scatter it, no parity), both MB_CAVE so the wild Pokémon "
              "live in the caves and not the built corridors (LABYRINTH_MAZE.md §5); "
              "`beam_h` and `beam_v`, timbers laid across a chasm. Register every one a ring "
              "uses with `Ichor_AddThreadFloor(f, f + 1)` (eight floors at most).")


# --------------------------------------------------------------------------
# Formations
# --------------------------------------------------------------------------

def convert(cs, key=None, title=None):
    """A cave_dark Struct as one of ours, recolored onto the earth floor."""
    s = Struct(key or cs.key, title or cs.title, cs.w, cs.h, walk=list(cs.walk), section=SEC,
               notes=cs.notes)
    s.names = dict(cs.names)
    s.behaviors = dict(getattr(s, "behaviors", {}))
    for (c, b) in cs.behaviors.items():
        s.behaviors[c] = "MB_CAVE" if b == "MB_CAVE" else b
    for n in ("bottom", "middle", "top"):
        a = recolor(cs.layers[n].a, PROP)
        _check(a, PROP, cs.key)
        s.layers[n].a[:] = a
    return s


KEEP = ["stalagmite", "stalagmites", "stalagmite_tall", "column", "boulder", "rock_pile",
        "slab", "ledge_w", "ledge_a", "ledge_b", "ledge_e"]


def formations():
    by = {s.key: s for s in CP.stone_structs()}
    out = [convert(by[k]) for k in KEEP]
    hole = [s for s in CP.mouth_structs() if s.key == "hole_down"][0]
    h = convert(hole, "hole", "A hole in the floor: the way down")
    h.behaviors[(0, 0)] = "MB_NORMAL"
    h.notes = ("A hole broken through the floor into the ring below (LABYRINTH_MAZE.md §3): "
               "walkable; a coord event on it drops the player through. Its rough steps read "
               "as a way down.")
    out.append(h)
    return out


# --------------------------------------------------------------------------
# The breach and the rubble
# --------------------------------------------------------------------------

def _masonry_face(left, right):
    L = A.K.Layer(16, 16)
    KIT.draw_face(L, 0, 0, left=left, right=right)
    return L.a


def breach():
    """Two face cells where dressed ashlar breaks into the cave's raw rock:
    `to_cave` (masonry west, rock east) and `to_house` (rock west, masonry
    east), for a one-row face that meets a cave face's lower row; and
    `rubble`, `rubble_2` (a collapsed wall's blocks, on earth)."""
    s = Struct("breach", "The breach: where the house breaks into the cave", 4, 1,
               walk=["XXXX"], section=SEC,
               notes="The house's signature piece (LABYRINTH_MAZE.md §4). (0) `to_cave`: a "
                     "corridor face whose ashlar courses break off ragged into raw flowstone, "
                     "masonry to the west; (1) `to_house`, the mirror. Lay them where a "
                     "masonry face row meets a cave face's `fb` row. (2) `rubble`, (3) "
                     "`rubble_2`: dressed blocks fallen from a broken wall onto the earth, with "
                     "rough rock among them. All block.")
    s.names = {"to_cave": (0, 0), "to_house": (1, 0), "rubble": (2, 0), "rubble_2": (3, 0)}
    mason = _masonry_face("cont", "cont")
    cave = recolor(CK.face_cell("fb", "A", "C"), ROCK)
    rng = np.random.default_rng(7)
    edge = [6 + int(round(3 * np.sin(y / 2.3))) + int(rng.integers(0, 2)) for y in range(16)]
    for cx, flip in ((0, False), (1, True)):
        a = np.empty((16, 16, 4), np.uint8)
        for y in range(16):
            for x in range(16):
                xx = 15 - x if flip else x
                src = mason if xx < edge[y] else cave
                a[y, x] = src[y, x]
            # a broken dark seam along the break
            xe = edge[y] if not flip else 15 - edge[y]
            if 0 <= xe < 16:
                a[y, xe] = (*A.C["lk"], 255)
        s.B.a[0:16, cx * 16:cx * 16 + 16] = a
    earth = recolor(CK.floor_cell(), EARTH)
    for cx, blocks in ((2, ((1, 7, 7, 5), (8, 4, 6, 6), (5, 11, 8, 4))),
                       (3, ((2, 3, 6, 5), (9, 8, 6, 5), (1, 10, 5, 5), (7, 12, 4, 3)))):
        s.B.a[0:16, cx * 16:cx * 16 + 16] = earth
        M = s.M
        for (bx, by, bw, bh) in blocks:
            x0, y0 = cx * 16 + bx, by
            for y in range(bh):
                for x in range(bw):
                    edgep = x in (0, bw - 1) or y in (0, bh - 1)
                    c = "lk" if edgep else ("ls5" if y == 1 else ("ls4" if x < bw // 2 else "ls3"))
                    M.px(x0 + x, y0 + y, c)
            M.px(x0 + bw, y0 + bh, "ls1")   # its shadow
        # a rough rock among the blocks
        for (rx, ry) in ((cx * 16 + 12, 2), (cx * 16 + 3, 1)):
            for y in range(3):
                for x in range(3):
                    M.px(rx + x, ry + y, "ls2" if (x + y) % 2 else "ls3")
    return s


def build():
    """The cave section's pieces (rows 13-35 of the sheet)."""
    return [rock(), *regions(), floors(), breach()]
