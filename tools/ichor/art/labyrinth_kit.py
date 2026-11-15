"""The rings' house kit: what every ring of the Labyrinth is built from.

Shared by gTileset_Labyrinth and its sister gTileset_Mychos (the inner rings and
the heart), drawn by the same code at the same metatile ids in both, so a map
builder's walls, floors and thread work on either.

  walls     the corridor walls as an autotile: every wall cell is a *top* (the
            dark top of the masonry, rim-lit where it meets a corridor) or a *face*
            (the masonry seen from the south, one row tall). autotile() picks the
            piece for each wall cell from its neighbours.
  thread    the rings' floor, "the same stone in the dark": the gypsum slabs one
            shade down from the workshop's, laid in the same running bond; each
            half with the ten twins Ariadne's thread is drawn with (ENGINE_API.md
            §6: H, V, NE, NW, SE, SW, cap N, S, W, E), the floor first and its
            twins right after it, so `Ichor_AddThreadFloor(floor, floor + 1)`.
  anchor    the bronze rings in the floor that the thread is tied off at.
  stairs    the stairways from ring to ring, down and up, in a north wall.

The thread is an overlay: its tiles sit in the middle layer over the floor, so
every floor's twins share the same ten thread tiles. Light pools (Ring V) and the
starlit marble (mychos) reuse them the same way.
"""
from __future__ import annotations

import labyrinth_art as A
from labyrinth_art import Struct, blit

# --------------------------------------------------------------------------
# The rings' floor: the slabs in the dark
# --------------------------------------------------------------------------

# Each floor kind: per-pixel role -> color. Roles: j joint (top/left edge where
# the next slab begins), e lit edge (just inside the joint), b body, s shadow
# edge (bottom / right), p pit.
FLOORS = {
    "dark": {"j": "ls3", "e": "ls5", "b": "ls4", "s": "ls4", "p": "ls3", "q": "ls5"},
    "sun": {"j": "lj", "e": "ld1", "b": "lw1", "s": "ls6", "p": "ls6", "q": "ld1"},
    "moon": {"j": "ls3", "e": "ld1", "b": "ld0", "s": "ls5", "p": "ls5", "q": "ld1"},
}
# small marks in the slabs (per half), so a run of floor isn't sterile
PITS = {"l": ((4, 10), (10, 5)), "r": ((5, 4), (12, 11))}
GLINTS = {"l": ((7, 4),), "r": ((9, 9),)}


def dark_slab(L, x0, y0, half="l", kind="dark"):
    """One cell of a ring floor at (x0, y0): a slab's left half where x + y is
    even, its right half where odd (the workshop's running bond)."""
    col = FLOORS[kind]
    for y in range(16):
        for x in range(16):
            if y == 0 or (half == "l" and x == 0):
                r = "j"
            elif y == 1 or (half == "l" and x == 1):
                r = "e"
            elif y == 15 or (half == "r" and x == 15):
                r = "s"
            else:
                r = "b"
                if (x, y) in PITS[half]:
                    r = "p"
                elif (x, y) in GLINTS[half]:
                    r = "q"
            L.px(x0 + x, y0 + y, col[r])


MARBLE = {"j": "nn1", "e": "nm2", "b": "nm1", "s": "nm0", "v": "nm0", "g": "ns0"}


def marble_slab(L, x0, y0):
    """Starlit Cretan marble, one square slab a cell, veined (night palette):
    the Choros and the Starry Chamber."""
    for y in range(16):
        for x in range(16):
            if y == 0 or x == 0:
                c = MARBLE["j"]
            elif y == 1 or x == 1:
                c = MARBLE["e"]
            elif y == 15 or x == 15:
                c = MARBLE["s"]
            else:
                c = MARBLE["b"]
            L.px(x0 + x, y0 + y, c)
    # a faint vein and the polish catching the starlight
    for (x, y) in ((9, 11), (10, 11), (11, 10), (12, 10)):
        L.px(x0 + x, y0 + y, MARBLE["v"])
    for (x, y) in ((4, 4), (5, 4), (4, 5), (6, 3)):
        L.px(x0 + x, y0 + y, MARBLE["e"])
    L.px(x0 + 4, y0 + 3, MARBLE["g"])


def on_ring_floor(s, cells=None, odd=False, kind="dark"):
    """Lay a ring floor in the bottom layer of `cells` (default: all)."""
    if cells is None:
        cells = [(x, y) for y in range(s.h) for x in range(s.w)]
    s.floor_cells = list(cells)
    s.floor_kind = kind
    for (cx, cy) in cells:
        if kind == "marble":
            marble_slab(s.B, cx * 16, cy * 16)
        else:
            dark_slab(s.B, cx * 16, cy * 16, "l" if (cx + cy + odd) % 2 == 0 else "r", kind)
    return s


def ring_twins(s):
    """[s, its odd twin] on the dark floor (labyrinth_workshop.twins for the
    rings): the twin holds the rows of s that show floor, on the other parity."""
    import copy
    rows = sorted({cy for (_, cy) in s.floor_cells})
    r0, r1 = rows[0], rows[-1] + 1
    t = copy.deepcopy(s)
    t.key = s.key + "_odd"
    t.title = s.title + " (odd cells)"
    on_ring_floor(t, s.floor_cells, odd=True, kind=s.floor_kind)
    if (r0, r1) != (0, s.h):
        t.h = r1 - r0
        for ln in t.layers:
            sub = A.K.Layer(t.w * 16, t.h * 16)
            sub.a[:] = t.layers[ln].a[r0 * 16:r1 * 16]
            t.layers[ln] = sub
        t.walk = t.walk[r0:r1]
        t.behaviors = {(x, y - r0): mb for (x, y), mb in t.behaviors.items() if r0 <= y < r1}
        t.ground = {(x, y - r0): g for (x, y), g in t.ground.items() if r0 <= y < r1}
        t.names = {n: (x, y - r0) for n, (x, y) in t.names.items() if r0 <= y < r1}
        t.floor_cells = [(x, y - r0) for (x, y) in s.floor_cells]
        if getattr(t, "anims", None):
            for an in t.anims.values():
                an["frames"] = [_sub(f, r0, r1) for f in an["frames"]]
    t.twin_of = (s.key, r0)
    t.notes = (f"`{s.key}` for a top-left cell where x + y is odd" +
               (f": its rows {r0}-{r1 - 1}; keep `{s.key}`'s other rows." if (r0, r1) != (0, s.h)
                else "."))
    s.parity = "even"
    t.parity = "odd"
    return [s, t]


def _sub(layer, r0, r1):
    sub = A.K.Layer(layer.w, (r1 - r0) * 16)
    sub.a[:] = layer.a[r0 * 16:r1 * 16]
    return sub


# --------------------------------------------------------------------------
# Ariadne's thread
# --------------------------------------------------------------------------

# The ten shapes, in the engine's order (src/ichor_labyrinth.c, SHAPE_*).
SHAPES = ["h", "v", "ne", "nw", "se", "sw", "cap_n", "cap_s", "cap_w", "cap_e"]
# The thread runs a little up and left of the cell's middle, through its top
# and left tiles, so a straight changes two tiles and every other tile of the
# cell is the floor's own.
TY = 5          # the cord's top row (rows 5-6) and left column (columns 5-6)


def thread_mask(shape):
    """The cord's pixels in a cell for one of the ten shapes."""
    m = set()
    n = shape in ("v", "ne", "nw", "cap_n")
    s = shape in ("v", "se", "sw", "cap_s")
    w = shape in ("h", "nw", "sw", "cap_w")
    e = shape in ("h", "ne", "se", "cap_e")
    c0, c1 = TY, TY + 1
    if n:
        m |= {(x, y) for x in (c0, c1) for y in range(0, c1 + 1)}
    if s:
        m |= {(x, y) for x in (c0, c1) for y in range(c0, 16)}
    if w:
        m |= {(x, y) for y in (c0, c1) for x in range(0, c1 + 1)}
    if e:
        m |= {(x, y) for y in (c0, c1) for x in range(c0, 16)}
    if shape.startswith("cap"):
        # the end: a little knot
        m |= {(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)}
    return m


def draw_thread(L, x0, y0, shape):
    """The cord, shaded as a twisted two-ply red thread lying on the stone, with
    its shadow down and to the right."""
    m = thread_mask(shape)
    knot = shape.startswith("cap")
    for (x, y) in m:
        lit = (x, y - 1) not in m or (x - 1, y) not in m
        dark = (x, y + 1) not in m or (x + 1, y) not in m
        if lit and not dark:
            c = "lt2" if (x + y) % 4 == 0 else "lt1"
        elif dark and not lit:
            c = "lt1" if (x + y) % 4 == 2 else "lt0"
        elif lit and dark:
            c = "lt1"
        else:
            c = "lt1"
        L.px(x0 + x, y0 + y, c)
    if knot:
        L.px(x0 + 4, y0 + 4, "lt1")
        L.px(x0 + 5, y0 + 5, "lt2")
        L.px(x0 + 6, y0 + 6, "lt0")
    for (x, y) in list(m):
        for (qx, qy) in ((x + 1, y), (x, y + 1), (x + 1, y + 1)):
            if (qx, qy) not in m and 0 <= qx < 16 and 0 <= qy < 16:
                L.px(x0 + qx, y0 + qy, "ls3")
    # shadows must not fall on the cord itself (a later cord pixel may have been
    # overwritten above): repaint the cord's lit pixels last
    for (x, y) in m:
        if L.get(x0 + x, y0 + y) == "ls3":
            L.px(x0 + x, y0 + y, "lt1")


def thread_block(key, title, floors, notes="", section="thread"):
    """Several floors with their twins as one struct 8 wide, so each floor's ids
    run on: the floor at n, its ten twins at n + 1 ... n + 10. floors: [(name,
    kind, half, behavior)], kind a FLOORS name, "marble", or a painter
    f(layer, x0, y0) for a floor that covers its cell (no parity)."""
    n = len(floors) * 11
    h = (n + 7) // 8
    s = Struct(key, title, 8, h, walk=["." * 8] * h, section=section, notes=notes)
    s.names = {}
    s.runs = {}
    for k, (name, kind, half, beh) in enumerate(floors):
        for i in range(11):
            idx = k * 11 + i
            cx, cy = idx % 8, idx // 8
            if kind == "marble":
                marble_slab(s.B, cx * 16, cy * 16)
            elif callable(kind):
                kind(s.B, cx * 16, cy * 16)
            else:
                dark_slab(s.B, cx * 16, cy * 16, half, kind)
            if i:
                draw_thread(s.M, cx * 16, cy * 16, SHAPES[i - 1])
            if beh:
                s.behaviors[(cx, cy)] = beh
            s.names[name if i == 0 else f"{name}_{SHAPES[i - 1]}"] = (cx, cy)
        s.runs[name] = k * 11
    # cells past the last run: plain void, blocked
    for idx in range(n, h * 8):
        cx, cy = idx % 8, idx // 8
        s.B.rect(cx * 16, cy * 16, 16, 16, "lk")
        s.walk[cy] = s.walk[cy][:cx] + "X" + s.walk[cy][cx + 1:]
    return s


# --------------------------------------------------------------------------
# The walls: an autotile of tops and faces
# --------------------------------------------------------------------------

RIM = ["lk", "ls5", "ls3", "ls2"]   # from the corridor's edge inward: seam, lit edge, bevel
SPECKS = ((2, 3), (6, 6))           # in every 8 x 8 of a top's fill


def _fill(x, y):
    """The top of the masonry, dark (the glow paint's latent color is this)."""
    return "ls2" if (x % 8, y % 8) in SPECKS else "ls1"


def draw_top(L, x0, y0, n=False, w=False, e=False, nw=False, ne=False, sw=False, se=False):
    """A wall's top seen from above: dark stone, rim-lit along every side that
    meets a corridor. n, w, e: floor on that side. nw, ne: floor only at that
    diagonal (an inner corner). sw, se: the wall turns down beside a face there
    (floor at that diagonal): the rim of the wall below starts at the face's lip."""
    for y in range(16):
        for x in range(16):
            ds = []
            if n:
                ds.append(y)
            if w:
                ds.append(x)
            if e:
                ds.append(15 - x)
            r = len(RIM)
            if nw and x < r and y < r:
                ds.append(max(x, y))
            if ne and x > 15 - r and y < r:
                ds.append(max(15 - x, y))
            if sw and x < r and y >= 4:
                ds.append(x)
            if se and x > 15 - r and y >= 4:
                ds.append(15 - x)
            d = min(ds) if ds else 99
            c = RIM[d] if d < len(RIM) else _fill(x, y)
            L.px(x0 + x, y0 + y, c)


def draw_face(L, x0, y0, left="cont", right="cont"):
    """A wall's south face, one row: the coping (the top's lip catching the light)
    over two courses of ashlar, sixteen-pixel blocks staggered. left / right:
    'open' (the wall ends, a corridor beyond: its edge shows), 'cont' (the face
    runs on) or 'inner' (it meets a wall that turns down beside it)."""
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "ls1"
            elif y == 1:
                c = "ls2"
            elif y == 2:
                c = "ls3"
            elif y == 3:
                c = "ls5"
            elif y == 4:
                c = "ls1"
            elif y == 15:
                c = "lk"
            else:
                course, yy = (0, y - 5) if y < 10 else (1, y - 10)
                jx = 0 if course == 0 else 8
                if yy == 4:
                    c = "ls2"
                elif x == jx:
                    c = "ls2"
                elif x == jx + 1:
                    c = "ls4"
                elif yy == 0:
                    c = "ls4"
                else:
                    c = "ls3"
            L.px(x0 + x, y0 + y, c)
    # wear in the blocks (the same marks every cell)
    for (x, y) in ((5, 7), (12, 12), (3, 12), (13, 6)):
        L.px(x0 + x, y0 + y, "ls2")
    for (x, y) in ((6, 6), (4, 11)):
        L.px(x0 + x, y0 + y, "ls4")
    for side, kind in (("l", left), ("r", right)):
        X = (lambda v: v) if side == "l" else (lambda v: 15 - v)
        if kind == "open":
            # the top's side rim comes down to the coping, then the wall's end
            for y in range(0, 3):
                for d in range(len(RIM)):
                    L.px(x0 + X(d), y0 + y, RIM[d])
            for y in range(3, 15):
                L.px(x0 + X(0), y0 + y, "lk")
                if y < 5:
                    continue
                if side == "l":
                    L.px(x0 + X(1), y0 + y, "ls4")
                else:
                    L.px(x0 + X(1), y0 + y, "ls2")
            L.px(x0 + X(1), y0 + 3, "ls5")
        elif kind == "inner":
            for y in range(4, 16):
                L.px(x0 + X(0), y0 + y, "lk" if y > 4 else "ls1")


# every valid top: (n, w, e) and the inner corners each allows
def top_combos():
    out = []
    for n in (0, 1):
        for w in (0, 1):
            for e in (0, 1):
                opts = []
                if not n and not w:
                    opts.append("nw")
                if not n and not e:
                    opts.append("ne")
                if not w:
                    opts.append("sw")
                if not e:
                    opts.append("se")
                for mask in range(1 << len(opts)):
                    inner = tuple(o for i, o in enumerate(opts) if mask >> i & 1)
                    out.append((n, w, e, inner))
    return out


def top_name(n, w, e, inner):
    sides = "".join(c for c, v in (("n", n), ("w", w), ("e", e)) if v)
    name = "top" + (f"_{sides}" if sides else "")
    if inner:
        name += "_in_" + "_".join(inner)
    return name


FACE_KINDS = ("open", "cont", "inner")


def face_name(left, right):
    short = {"open": "o", "cont": "c", "inner": "i"}
    return f"face_{short[left]}{short[right]}"


def walls():
    """The autotile: every top and every face, packed 8 wide."""
    tops = top_combos()
    faces = [(l, r) for l in FACE_KINDS for r in FACE_KINDS]
    n = len(tops) + len(faces)
    h = (n + 7) // 8
    s = Struct("walls", "Walls: the corridor kit, an autotile", 8, h, walk=["X" * 8] * h,
               section="house",
               notes="Every wall cell of a ring is a **top** (the masonry's dark top, rim-lit "
                     "where it meets a corridor) or a **face** (the wall seen from the south, one "
                     "row tall; a wall cell with floor south of it). Paint a wall/floor grid and "
                     "let `labyrinth_tiles.autotile()` pick each cell: a top's name lists the "
                     "sides that meet floor (`top_nwe`) and its inner corners (`_in_nw`: floor "
                     "only at that diagonal; `_in_sw`, `_in_se`: the wall turns down beside a "
                     "face there); a face's two letters are its west and east ends: `o` open (the "
                     "wall ends, its edge shows), `c` continuing, `i` meeting a wall that turns "
                     "down beside it. `top` is solid rock: fill everything outside the rings "
                     "with it. Walls one cell thick work both ways: a row of faces, or a column "
                     "of `top_we` ending in `face_oo`. All block.")
    s.names = {}
    for i, (nn, ww, ee, inner) in enumerate(tops):
        cx, cy = i % 8, i // 8
        draw_top(s.B, cx * 16, cy * 16, n=nn, w=ww, e=ee, nw="nw" in inner, ne="ne" in inner,
                 sw="sw" in inner, se="se" in inner)
        s.names[top_name(nn, ww, ee, inner)] = (cx, cy)
    for j, (l, r) in enumerate(faces):
        i = len(tops) + j
        cx, cy = i % 8, i // 8
        draw_face(s.B, cx * 16, cy * 16, l, r)
        s.names[face_name(l, r)] = (cx, cy)
    for idx in range(n, h * 8):
        cx, cy = idx % 8, idx // 8
        draw_top(s.B, cx * 16, cy * 16)
    return s


def classify(grid, x, y):
    """The kit piece for wall cell (x, y) of a grid of booleans (True = wall);
    outside the grid counts as wall."""
    H, W = len(grid), len(grid[0])

    def wall(xx, yy):
        return not (0 <= xx < W and 0 <= yy < H) or grid[yy][xx]
    if not wall(x, y + 1):
        def end(dx):
            if not wall(x + dx, y):
                return "open"
            if wall(x + dx, y + 1):
                return "inner"
            return "cont"
        return face_name(end(-1), end(1))
    n, w, e = not wall(x, y - 1), not wall(x - 1, y), not wall(x + 1, y)
    inner = []
    if not n and not w and not wall(x - 1, y - 1):
        inner.append("nw")
    if not n and not e and not wall(x + 1, y - 1):
        inner.append("ne")
    if not w and not wall(x - 1, y + 1):
        inner.append("sw")
    if not e and not wall(x + 1, y + 1):
        inner.append("se")
    return top_name(int(n), int(w), int(e), tuple(inner))


# --------------------------------------------------------------------------
# The bronze anchor rings
# --------------------------------------------------------------------------

BZ = {"k": "ink", "0": "bz0", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4"}


def anchor():
    """A bronze ring lying in a round socket in the floor, its staple set in
    the stone: stand on it and tie off (LABYRINTH.md §5.1)."""
    s = Struct("anchor", "A bronze anchor ring in the floor", 1, 1, walk=["."],
               section="house",
               notes="A bronze ring lying in its socket, where the thread is tied off: register "
                     "its cell with `Ichor_AddThreadAnchor`. Walkable; thread is never drawn "
                     "over it. `anchor_odd` where x + y is odd.")
    on_ring_floor(s)
    # a heavy bronze ring lying flat, the floor showing through it, hung from
    # a staple let into the stone
    blit(s.M, ["......kkkk......",
               ".....k4432k.....",
               "......kkkk......",
               "....kkk33kkk....",
               "...k44333221k...",
               "..k43kk..kk21k..",
               ".k43k......k21k.",
               ".k4k........k1k.",
               ".k3k........k1k.",
               ".k3k........k0k.",
               ".k32k......k10k.",
               "..k21kk..kk10k..",
               "...k21111100k...",
               "....kkkkkkkk....",
               "................",
               "................"], BZ, 0, 1)
    s.names = {"ring": (0, 0)}
    return ring_twins(s)


# --------------------------------------------------------------------------
# Stairs from ring to ring
# --------------------------------------------------------------------------

def stairs():
    """Two-cell stairways in a face row: down to the next ring (into the dark)
    and up to the last (toward the lamplight above)."""
    s = Struct("stairs", "Stairs from ring to ring", 4, 1, walk=["...."],
               section="house",
               notes="Two stairways, each two cells wide, for a face row: (0, 1) the stair "
                     "**down** to the next ring, its steps dropping away into the dark; (2, 3) "
                     "the stair **up** to the last, its steps climbing toward lamplight. "
                     "MB_NORTH_ARROW_WARP on all four: put a warp on each cell. Their ends "
                     "meet the face's open ends, so lay them in a run of faces.")
    L = s.B
    for half in (0, 1):
        x0 = half * 32
        down = half == 0
        for y in range(16):
            for x in range(32):
                X = x if x < 16 else 31 - x        # mirror about the middle
                if y < 5:
                    # the coping, cut by the stair's lintel
                    c = ("ls1", "ls2", "ls4", "ls6", "ls1")[y]
                    if y >= 2 and 3 <= X:
                        c = ("ls4", "ls6", "ls1")[y - 2] if X > 3 else c
                elif X < 3:
                    # the jambs: dressed posts (the stair is mirror-symmetric, so its
                    # two cells share their tiles)
                    c = ("lk", "ls4", "ls3")[X]
                else:
                    step = (y - 5) // 2
                    nose = (y - 5) % 2 == 1
                    if down:
                        # steps dropping away: the nearest (lowest row) lit,
                        # each farther one darker, into the black
                        shade = ["lk", "lk", "ls1", "ls2", "ls3"][min(step, 4)]
                        c = {"lk": "ls1", "ls1": "ls2", "ls2": "ls3", "ls3": "ls5"}[shade] \
                            if nose else shade
                    else:
                        # steps climbing: each nosing lit from the lamps above
                        shade = ["ls3", "ls3", "ls4", "ls4", "ls5"][min(step, 4)]
                        c = {"ls3": "ls5", "ls4": "ls6", "ls5": "lw1"}[shade] if nose else shade
                L.px(x0 + x, y, c)
        L.px(x0, 15, "lk")
        L.px(x0 + 31, 15, "lk")
        for c in range(2):
            s.behaviors[(half * 2 + c, 0)] = "MB_NORTH_ARROW_WARP"
    s.names = {"down_l": (0, 0), "down_r": (1, 0), "up_l": (2, 0), "up_r": (3, 0)}
    return s


# --------------------------------------------------------------------------
# The kit
# --------------------------------------------------------------------------

def house_kit():
    """The shared pieces in the house section (after floor, arcade, arch4, edge)."""
    return [walls(), *anchor(), stairs()]


def thread_floors():
    """The rings' threadable floors at fixed ids in both tilesets."""
    return [thread_block(
        "thread", "Floors: the rings' slabs and Ariadne's thread",
        [("dark_l", "dark", "l", None), ("dark_r", "dark", "r", None)],
        notes="The rings' floor: the house's gypsum slabs in the dark, a shade down from the "
              "workshop's, in the same running bond: **`dark_l` where x + y is even, `dark_r` "
              "where odd**. Each is followed by its ten thread twins (the engine's order: "
              "`h`, `v`, `ne`, `nw`, `se`, `sw`, `cap_n`, `cap_s`, `cap_w`, `cap_e`), so a "
              "ring's ON_LOAD registers `Ichor_AddThreadFloor(dark_l, dark_l + 1)` and "
              "`(dark_r, dark_r + 1)`. Every walkable cell of a threaded ring must be one of "
              "the registered floors (or an anchor): the thread stops at anything else. The "
              "last two cells are void.")]
