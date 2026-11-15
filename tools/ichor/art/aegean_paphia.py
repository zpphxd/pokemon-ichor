#!/usr/bin/env python3
"""Paphia's pieces: the temple town's crafts (design/phase4/ROOMS_aegean.md).

Peristera's nesting holes, doves, feathers, the Egg in its wool and the ladder;
Lysis's kick-wheel, beehive kiln, fish-bone heap and shelf of fish flasks;
Pygmalion's marble blocks, hoist, jointed model, dust-sheeted statue, chisels
and table for two; Leukippe's bronze mirrors, turning mirror, mold, casting pit
and polishing bench; Eumelos's old apple tree (bare, and in leaf with one golden
apple), apple racks, crates, pruning hook and golden-apple plate; and the yards'
hedge and stone threshold. Drawn in oikia's palettes (aegean_art.PALETTES).
"""
import math

import numpy as np

from aegean_art import Canvas, STAMPS, grid, stamp

# ==========================================================================
# The dovecote
# ==========================================================================


def _pigeonholes(doves):
    """Two rows of arched nesting holes let into the whitewash, a ledge under
    each row, doves looking out of some. 16x32 over the back wall (rows 0-1)."""
    c = Canvas(16, 32)
    for row, y in enumerate((9, 16)):
        for col, x in enumerate((0, 5, 10)):
            c.paste("""
.SSS.
S111S
S1k1S
S1k1S""", x + 1, y)
            if (row, col) in doves:
                c.paste("""
..ww.
.wwko
.wws.""", x + 1, y + 1)
        c.hline(0, 15, y + 4, "s")
        c.hline(0, 15, y + 5, "S")
    return c


stamp("pigeonholes", "wall", _pigeonholes({(0, 1), (1, 0), (1, 2)}), 1, 2,
      note="nesting holes in the wall, doves looking out of three")
stamp("pigeonholes_b", "wall", _pigeonholes({(0, 0), (0, 2), (1, 1)}), 1, 2,
      note="nesting holes in the wall, doves in three")

stamp("doves", "wall", """
................
................
................
................
................
....kk..........
...kwwk.........
..kowwSk........
...kwwwSkk......
...kwwwwssk.....
....kwwwsSk..kk.
.....kSkkk..kwwk
.....kok...kwwok
...........kswwk
..p.p......kSssk
.p.p.p......kokk
""", 1, 1, note="two doves pecking at spilled seed")
stamp("feathers", "wall", """
................
................
...........w....
..w.......ws....
..ws.......s....
...s............
................
.......w........
.......sw.......
........s.......
................
.w...........w..
.sw.........ws..
..s.............
................
................
""", 1, 1, walk={(0, 0)}, note="feathers drifted down from the nesting floor (walkable)")

stamp("egg_basket", "nature", """
................
................
.....kkkk.......
....kwwwwk......
...kwwpwwwk.....
...kwwwwpwk.....
..kwwwwwwwwk....
kkkwwpwwwwwkkkk.
kJwkwwwwwpwkwJk.
kjjwkkwwwwkwjjk.
kJjjjwkkkkwjjJk.
kjKjjjKjjjKjjjk.
.kjjjjjjjjjjjk..
..kKKKKKKKKKk...
...kkkkkkkkk....
................
""", 1, 1, note="a wool basket with one big speckled egg in it, not a dove's")


def _ladder(hatch=True):
    """A ladder up through a hatch in the ceiling beam: 16x48, rows 0-2."""
    c = Canvas(16, 48)
    if hatch:
        c.rect(2, 0, 13, 9, "k")
        c.hline(2, 13, 10, "d")
        c.vline(1, 0, 10, "d")
        c.vline(14, 0, 10, "d")
    for x in (3, 11):
        c.vline(x, 2, 44, "k")
        c.vline(x + 1, 2, 44, "l" if x == 3 else "m")
        c.vline(x + 2, 2, 44, "k")
    for y in range(6, 44, 5):
        c.hline(5, 10, y, "h")
        c.hline(5, 10, y + 1, "d")
    c.hline(3, 5, 45, "k")
    c.hline(11, 13, 45, "k")
    return c


stamp("ladder", "wood", _ladder(), 1, 3, note="a ladder up through a hatch in the ceiling")

# ==========================================================================
# The potter's house
# ==========================================================================

stamp("kick_wheel", "clay", """
................
.....kkkkk......
....kmlhlmk.....
...kmlhhllmk....
...kdmlllmdk....
.kk.kdmmmdk.kk..
kmdkkkkkkkkkdmk.
kmkhllllllllkmk.
kmkdmmmmmmmdkmk.
kmdkkkkdkkkkdmk.
kmdk..kdk...kmk.
kmdkkkkdkkkkdmk.
kmkStttttttSkmk.
kmkSSSSSSSSskmk.
kkkkkkkkkkkkkkk.
................
""", 1, 1, note="the kick-wheel in its frame, a wet pot thrown on its head, the flywheel below")


def _kiln():
    c = Canvas(32, 32)

    def sh(x, y, nx, ny):
        v = -0.55 * nx - 0.85 * ny
        return "h" if v > 0.55 else "l" if v > 0.1 else "m" if v > -0.45 else "d"
    c.ellipse(16, 17, 13.5, 13.0, shade=sh)
    c.rect(2, 22, 29, 29, "m")
    c.hline(2, 29, 29, "d")
    for y in range(18, 30):
        c.px(2, y, "l")
    # the coil courses of the dome
    for y in (9, 14, 19, 24):
        for x in range(4, 29):
            if c.get(x, y) in "hlm":
                c.px(x, y, "d" if c.get(x, y) == "m" else "m")
    # the firing mouth and the vent
    c.paste("""
..kkkkkk..
.kaaaaaak.
kaafFFfaak
kafFYYFfak
kfFYYYYFfk
kFYYYYYYFk""", 11, 21)
    c.paste(".kkkk.\nkaaaak\n.kkkk.", 13, 3)
    c.outline()
    c.hline(3, 28, 30, "k")
    return c


stamp("kiln", "clay", _kiln(), 2, 2, note="the beehive kiln, its firing mouth glowing")

stamp("fish_bones", "nature", """
................
................
................
........k.......
.......kwk......
...kk.kwSwk.....
..kwwkwwwkwk....
..kwSwkwkwSwk...
.kwkwwkwkwwkwk..
kwSkwSwkwSwkSwk.
kwkwwkwSwkwwkwk.
.kSwkwwkwwkSwk..
..kkwSkwkSwkk...
....kkkkkkk.....
................
................
""", 1, 1, note="a heap of fish bones nobody has thrown away")

stamp("flask_shelf", "clay", """
................................
................................
................................
................................
................................
................................
................................
...kk....kk....kk....kk....kk...
...kk....kk....kk....kk....kk...
..kmmk..kmmk..kmmk..kmmk..kmmk..
.kmlhmk.klhmk.kmlhk.kmlhk.klhmk.
.klkalk.kkalk.kakmk.klakk.kakmk.
.kmakmk.kakmk.kmaak.kaamk.kmkak.
.kmlllk.kmllk.kmllk.kmllk.kmllk.
..kmdk..kmdk...kdk..kmdk..kmdk..
...kk....kk....kk....kk....kk...
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
kddddddddddddddddddddddddddddddk
kdmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
...kdk....................kdk...
...kdk....................kdk...
....k......................k....
""", 2, 2, note="perfume flasks drying on a shelf, every one with the same little painted fish")

# ==========================================================================
# Pygmalion's workshop
# ==========================================================================


def _block(w, h, seed, marks=True):
    """A raw marble block: a lit top, a front in shade, chisel marks."""
    rnd = np.random.RandomState(seed)
    c = Canvas(w, h)
    x0, x1 = 1, w - 2
    top0, top1 = h // 2 - h // 5 - 2, h // 2 - h // 5 + 2
    c.rect(x0, top0, x1, h - 3, "m")
    c.rect(x0, top0, x1, top1, "M")
    c.vline(x1, top1 + 1, h - 3, "n")
    c.hline(x0, x1, h - 3, "n")
    if marks:
        for _ in range(w * h // 60):
            x, y = rnd.randint(x0 + 1, x1 - 1), rnd.randint(top1 + 2, h - 4)
            c.px(x, y, "n")
            c.px(x + 1, y + 1, "n")
    c.outline()
    return c


stamp("marble_block", "bronze", _block(16, 16, 1), 1, 1, note="a raw block of marble, chisel-marked")
stamp("marble_block_b", "bronze", _block(16, 16, 2, marks=False).flip(), 1, 1,
      note="a sawn marble block")
stamp("marble_block_big", "bronze", _block(32, 32, 3), 2, 2, note="a great block of marble")


def _hoist():
    """Shear legs with a block and tackle; a marble block hangs from it.
    The crossbeam and pulley are on the top layer (the player walks under)."""
    wood, top, stone = Canvas(32, 48), Canvas(32, 48), Canvas(32, 48)
    # legs splay from the crossbeam to the floor, kept in the outer columns
    for (xa, xb) in ((5, 1), (26, 30)):
        wood.line(xa, 14, xb, 44, "m")
        wood.line(xa + 1, 14, xb + 1, 44, "l")
    wood.outline()
    # rope from the pulley to the block
    wood.vline(15, 16, 31, "c")
    wood.vline(16, 16, 31, "C")
    wood.paste("kk\nkk", 15, 31)
    # crossbeam and pulley (top layer)
    top.rect(1, 6, 30, 9, "l")
    top.hline(1, 30, 6, "h")
    top.hline(1, 30, 9, "m")
    top.paste(".kkkk.\nkbyybk\nkbkkbk\nkbyybk\n.kkkk.", 13, 9)
    top.vline(15, 14, 15, "c")
    top.vline(16, 14, 15, "C")
    top.outline()
    # the legs' tops share the beam's cells: they go on the top layer too;
    # the top layer keeps to the first row of cells
    for y in range(16, 48):
        top.g[y] = ["."] * 32
    for y in range(16):
        for x in range(32):
            if wood.g[y][x] != "." and top.g[y][x] == ".":
                top.g[y][x] = wood.g[y][x]
            wood.g[y][x] = "."
    # the hanging block, in the bronze palette's marble (its own 8x8 tiles)
    stone.rect(9, 33, 22, 42, "m")
    stone.rect(9, 33, 22, 35, "M")
    stone.vline(22, 36, 42, "n")
    stone.hline(9, 22, 42, "n")
    stone.outline()
    return wood, top, stone


_w, _t, _s = _hoist()
_hw = stamp("_hoist_wood", "wood", _w, 2, 3, top=_t)
_hs = stamp("_hoist_stone", "bronze", _s, 2, 3)
_img = _hw["img"].copy()
_m = _hs["img"][..., 3] > 0
_img[_m] = _hs["img"][_m]
STAMPS["hoist"] = dict(_hw, img=_img, pal="wood+bronze",
                       note="shear legs with a block and tackle, a marble block hanging")
del STAMPS["_hoist_wood"], STAMPS["_hoist_stone"]

stamp("lay_figure", "wood", """
................
................
................
................
................
................
................
.......kk.......
......khlk......
......kllk......
.......kk.......
.......kk.......
.....kkhlkk.....
....khkllkhk....
....kl.ll.lk....
...kk.kllk.kk...
...kh.kllk.hk...
...kl.kmmk.lk...
...kk.kllk.kk...
......kllk......
.....kkmmkk.....
.....kh..hk.....
.....kl..lk.....
.....kk..kk.....
.....kl..lk.....
.....kl..lk.....
.....kk..kk.....
.......kk.......
.......kdk......
....kkkkkkkk....
...kmllllllmk...
...kkkkkkkkkk...
""", 1, 2, note="a wooden model of a woman, her joints pinned to move")


def _sheet_statue():
    """A statue under a dust sheet on its plinth, 16x48 against the back wall:
    a head, the shape of a shoulder, folds falling to the plinth."""
    return """
................
................
................
................
................
................
................
................
................
................
................
................
................
.......kkk......
......kcccCk....
.....kcccccCk...
.....kccccCCk...
......kcccCk....
....kkcccCCkk...
...kcccccccCCk..
..kcccccCccCCk..
..kccccccCcCCCk.
..kcccCcccCcCCk.
..kccccCcccCcCk.
..kcccCcccCccCk.
..kcccCccCcccCk.
..kccccCcCccCCk.
..kcccCccCccCCk.
..kccCcccCccCCk.
..kcccCccCcccCk.
..kccCccCcccCCk.
..kcccCccCccCCk.
..kccCcccCccCCk.
..kcccCccCcccCk.
.kcccCcccCccCCCk
.kccCcCccCcCcCCk
.kcCcCcCcCcCcCCk
.kkkkkkkkkkkkkkk
.khhhhhhhhhhhhmk
.klllllllllllmdk
.kkkkkkkkkkkkkkk
................
................
................
................
................
................
................
"""


stamp("statue_sheet", "wood", _sheet_statue(), 1, 3,
      note="a statue under a dust sheet on its plinth; the shape of a woman's shoulder")

stamp("chisel_rack", "wood", """
................
................
................
................
................
................
................
................
................
..kkkkkkkkkkkk..
..khhhhhhhhhhk..
..kmkkmkkmkkmk..
...kbkkbkkbkk...
...kbkkykkbk....
...kykkbkkyk....
...kbkkbkkbk....
...kmkkbkkmk....
...kmkkmkkmk....
...kdkkmkkdk....
...kmkkdkkmk....
...kkk.kk.kk....
................
................
................
................
................
................
................
................
................
................
................
""", 1, 2, note="chisels in a rack, bronze points down")

stamp("table_two", "wood", """
................................
................................
................................
................................
.....kkk..................kkk...
....kbyyk.....kkkkk......kbyyk..
....kzbbk....khhlllk.....kzbbk..
.....kzk....khlllmmdk.....kzk...
....kkkkk..kCcccccCCk....kkkkk..
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.khhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
.khlllllllllllllllllllllllllllk.
.kmmmmmmmmmmmmmmmmmmmmmmmmmmmmk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
..kmdk....................kmdk..
..kkkk....................kkkk..
""", 2, 1, note="a small table set for two: two cups and a loaf between them")

# ==========================================================================
# The mirror-house
# ==========================================================================


def _mirror(c, cx, cy, rx, ry, tilt):
    """A polished bronze disc, flat on the wall on its loop, its handle hanging
    below: a dark rim, a bright face with one diagonal glint, and in it the
    dim shape of whoever stands in the room."""
    c.ellipse(cx, cy, rx, ry, fill="z")

    # The face reflects the room: the pale wall above, the red dado, the
    # floor below, a glint at the top left, and a dim figure standing there.
    def face(x, y, nx, ny):
        if nx + ny < -0.95:
            return "M"
        if ny < 0.15 + 0.25 * tilt * nx:
            return "Y"
        if ny < 0.4 + 0.25 * tilt * nx:
            return "r"
        return "b"
    c.ellipse(cx, cy, rx - 1, ry - 1, shade=face)
    fx, fy = int(cx + 0.5 * tilt), int(cy)
    c.paste(".z.\nzzz\n.z.", fx - 1, fy - 1)
    hx = int(cx + tilt * 2)
    c.vline(hx, int(cy + ry), int(cy + ry) + 4, "z")
    c.px(hx, int(cy + ry) + 5, "b")
    c.px(int(cx), int(cy - ry) - 1, "z")


def _mirrors(variant):
    c = Canvas(32, 32)
    if variant == 0:
        _mirror(c, 8, 15, 5.5, 5.5, 0)
        _mirror(c, 23, 14, 4.5, 6.0, 1)
    else:
        _mirror(c, 9, 14, 4.5, 6.0, -1)
        _mirror(c, 23, 16, 5.5, 5.0, 0)
    for x in (8, 23):
        c.paste(".k.\nkzk", x - 1, 6)
    c.outline()
    return c


stamp("mirrors", "bronze", _mirrors(0), 2, 2, note="bronze mirrors hung at different angles, dimly reflecting")
stamp("mirrors_b", "bronze", _mirrors(1), 2, 2, note="bronze mirrors hung at different angles")


def _mirror_post():
    c = Canvas(16, 32)
    _mirror(c, 8, 8, 5.5, 5.5, 0)
    c.vline(7, 14, 27, "z")
    c.vline(8, 14, 27, "b")
    c.paste("..kkkkkkkk..\n.kbyyyyyybk.\n..kzzzzzzk..", 2, 27)
    c.outline()
    return c


stamp("mirror_post", "bronze", _mirror_post(), 1, 2, note="a mirror turning on its post, as in the rose court")

stamp("mirror_mold", "clay", """
................
................
................
................
....kkkkkkk.....
..kkmlllllmkk...
.kmlkkkkkkklmk..
.klkSSSSSSSkmdk.
kmlkSttttSSkmdk.
kmlkStSSSSskmdk.
.kmkkSSSSskkmk..
.kdmkkkkkkkmdk..
..kkdmmmmmdkk...
....kkkkkkk.....
................
................
""", 1, 1, note="a clay mold for a round mirror")


def _pit():
    c = Canvas(32, 32)
    c.ellipse(16, 17, 14, 11, fill="S")
    c.ellipse(16, 18, 11.5, 8.5, fill="s")
    c.ellipse(16, 19, 10, 7, fill="a")
    for (x, y) in [(9, 21), (12, 23), (20, 22), (23, 19), (10, 17), (21, 25), (15, 25)]:
        c.paste("fF\nFf", x, y)
    # the crucible on the embers, bronze glowing at its lip
    c.paste("""
.kkkkkk.
kYFFYFFk
kmkkkkmk
kmlllmdk
.kmmmdk.
..kkkk..""", 12, 12)
    c.outline()
    return c


stamp("casting_pit", "clay", _pit(), 2, 2, note="the casting pit: a crucible of bronze on the embers")

stamp("polish_bench", "wood", """
................................
................................
................................
................................
................................
...kkkkk......kkkkkkk...........
..kCCCCCk....kbyyyybk...kkkk....
..kCcCcCk...kbyhyyybzk.kccCk....
...kkkkk....kzbbbbbzk..kcCCk....
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
kllllllllllllllllllllllllllllllk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
..kdk......................kdk..
..kkk......................kkk..
""", 2, 1, note="the polishing bench: a pot of sand, felt pads, a mirror half-polished")

# ==========================================================================
# The orchard house
# ==========================================================================


def _branch(c, x, y, ang, length, width, depth, rnd, ch_lit, ch_dark):
    """A crooked branch from (x, y) at angle ang (radians, 0 = up)."""
    pts = []
    for i in range(int(length)):
        ang += (rnd.rand() - 0.5) * 0.5
        x += math.sin(ang)
        y -= math.cos(ang)
        pts.append((x, y))
        w = max(1, int(round(width * (1 - i / length * 0.6))))
        for k in range(w):
            c.px(int(round(x)) + k, int(round(y)), ch_lit if k == 0 else ch_dark)
    if depth > 0:
        for d in (-0.6, 0.55):
            _branch(c, x, y, ang + d + (rnd.rand() - 0.5) * 0.3, length * 0.62,
                    max(1, width - 1), depth - 1, rnd, ch_lit, ch_dark)


def _trunk(c, ch_lit, ch_mid, ch_dark):
    """A twisted trunk standing in rows 32-47 of a 32x48 tree."""
    c.paste("""
.......k....k..
......kmlk.kmk.
.....kmlldkmlk.
.....kmlldmlk..
......kmlldk...
......kmllddk..
.....kmlllddk..
.....kmllldk...
.....kmlllddk..
....kmlllldddk.
...kmllllllddk.
..kmmlkmlldkmdk
..kkkk.kkkk.kkk""", 8, 33)
    c.replace({"l": ch_lit, "m": ch_mid, "d": ch_dark})


def _bare_tree():
    rnd = np.random.RandomState(7)
    crown, trunk = Canvas(32, 48), Canvas(32, 48)
    for (x, ang, ln, w) in [(15, -0.5, 13, 3), (17, 0.35, 15, 3), (16, -0.05, 12, 2)]:
        _branch(crown, x, 33, ang, ln, w, 2, rnd, "s", "S")
    crown.outline()
    _trunk(trunk, "s", "S", "1")
    # crown pixels below row 32 belong to the trunk's layer
    for y in range(32, 48):
        for x in range(32):
            if crown.g[y][x] != "." and trunk.g[y][x] == ".":
                trunk.g[y][x] = crown.g[y][x]
            crown.g[y][x] = "."
    return crown, trunk


_crown, _trunk_c = _bare_tree()
stamp("apple_tree_bare", "wall", _trunk_c, 2, 3, top=_crown, walk={(0, 0), (1, 0), (0, 1), (1, 1)},
      note="the old apple tree: gray, twisted, leafless (crown drawn over the player)")


def _leafy_tree():
    """The same tree in leaf: the crown is nature-palette leaves over the bare
    branches' shape; one 8x8 tile holds the golden apple in wood's bronze."""
    rnd = np.random.RandomState(7)
    crown = Canvas(32, 48)
    for (cx, cy, rx, ry) in [(16, 14, 13, 10), (8, 19, 7.5, 7), (24, 18, 7.5, 7.5), (16, 6, 9, 6)]:
        def sh(x, y, nx, ny):
            v = -0.55 * nx - 0.8 * ny + (rnd.rand() - 0.5) * 0.5
            return "V" if v > 0.6 else "v" if v > 0.05 else "g" if v > -0.55 else "G"
        crown.ellipse(cx, cy, rx, ry, shade=sh)
    for (x, y) in [(7, 9), (21, 7), (12, 20), (26, 14), (17, 24), (5, 16)]:
        crown.px(x, y, "G")
        crown.px(x + 1, y, "g")
    crown.outline()
    trunk = Canvas(32, 48)
    _trunk(trunk, "j", "K", "K")
    trunk.replace({"d": "K"})
    return crown, trunk


_lc, _lt = _leafy_tree()
_leafy = stamp("apple_tree_gold", "nature", _lt, 2, 3, top=_lc, walk={(0, 0), (1, 0), (0, 1), (1, 1)},
               note="the old apple tree in leaf, one golden apple on it (for after the quest)")
# The golden apple's 8x8 tile, in the crown's shaded right lobe, is drawn in
# wood's palette: its bronze for the apple, its olive for the leaves round it.
_ay, _ax = 16, 24
_cell = Canvas(8, 8)
_crown_tile = _lc.g
for _y in range(8):
    for _x in range(8):
        ch = _crown_tile[_ay + _y][_ax + _x]
        if ch != ".":
            _cell.g[_y][_x] = "k" if ch == "k" else ("o" if (_x + _y) % 3 else "d")
_cell.paste("""
..kk....
.kyhk...
kyyyyk..
kbyybk..
.kbzk...
..kk....""", 1, 1)
_apple = grid("wood", _cell.text(), 8, 8)
_top = _leafy["top"].copy()
_top[_ay:_ay + 8, _ax:_ax + 8] = _apple
_leafy["top"] = _top
_leafy["pal"] = "nature+wood"


def _racks(n_apples_tray):
    """Slatted racks for apples, three trays, empty but for one tray."""
    c = Canvas(32, 48)
    for x in (1, 29):
        c.rect(x, 4, x + 1, 44, "m")
        c.vline(x, 4, 44, "l")
    for i, y in enumerate((12, 24, 36)):
        c.rect(1, y, 30, y + 2, "l")
        c.hline(1, 30, y, "h")
        c.hline(1, 30, y + 2, "d")
        for x in range(4, 29, 4):
            c.px(x, y + 1, "d")
        if i == n_apples_tray:
            for x in (8, 13, 18):
                c.paste(".kk.\nkook\nkoo.k\n.kk.", x, y - 4)
    c.outline()
    c.hline(1, 2, 45, "k")
    c.hline(29, 30, 45, "k")
    return c


stamp("apple_racks", "wood", _racks(1), 2, 3,
      note="apple racks along the wall, all empty but one tray with three small green apples")
stamp("apple_racks_empty", "wood", _racks(-1), 2, 3, note="empty apple racks")

stamp("apple_crate", "wood", """
................
................
................
................
................
..kkkkkkkkkkkk..
.kdmmmmmmmmmmdk.
.kdkkkkkkkkkkdk.
.khhhhhhhhhhhhk.
.klllllllllllmk.
.kkkkkkkkkkkkkk.
.khhhhhhhhhhhhk.
.klllllllllllmk.
.kmmmmmmmmmmmdk.
.kkkkkkkkkkkkkk.
................
""", 1, 1, note="an empty apple crate")

stamp("pruning_hook", "wood", """
................
................
................
................
................
................
................
................
................
.......kk.......
......kdk.......
......kk........
....kkkkk.......
...kyybbzk......
..kyk.kkzk......
..kbk...kmk.....
..kzk...kmlk....
...k.....kmlk...
.........kmlk...
.........kmlk...
.........kmdk...
.........kmdk...
.........kddk...
..........kk....
................
................
................
................
................
................
................
................
""", 1, 2, note="a pruning hook on a peg")

stamp("plate_gold", "clay", """
................................
................................
................................
................................
................................
................................
................................
..........kkkkkkkkkkk...........
........kkdddddddddddkk.........
.......kddmcmcmcmcmcmddk........
......kdmcccccccccccccmdk.......
.....kdmcccccccbkccccccmdk......
.....kdccccccckkkcccccccdk......
....kdmcccccknnnnkccccccmdk.....
....kdcccccknYYnnnkcccccmdk.....
....kdmccccknYnnnnbkccccmdk.....
....kdcccccknnnnnnbkcccccdk.....
....kdmcccccknnnnbbkccccmdk.....
....kdccccccknnbbbkcccccmdk.....
.....kdmcccccckkkkccccccdk......
.....kdccccccccccccccccmdk......
......kdmcccccccccccccmdk.......
.......kddmcmcmcmcmcmddk........
........kkdddddddddddkk.........
..........kkkkkkkkkkk...........
................................
................................
................................
................................
................................
................................
................................
""", 2, 2, note="a painted plate on the wall: a golden apple on white")

# ==========================================================================
# Yards
# ==========================================================================


def _hedge():
    """A clipped myrtle hedge, lit along its top, leaf clusters in rows, a
    few white flowers, its foot in shadow."""
    rnd = np.random.RandomState(11)
    c = Canvas(16, 32)
    c.rect(0, 0, 15, 31, "g")
    c.rect(0, 0, 15, 2, "v")
    c.hline(0, 15, 0, "V")
    for y in range(3, 27, 4):
        for x in range((y * 3) % 5, 16, 5):
            c.paste(".V.\nVvv\ngvG", x, y)
            if rnd.rand() < 0.3:
                c.px(x + 1, y + 1, "w")
    c.rect(0, 27, 15, 31, "G")
    for x in range(0, 16, 2):
        c.px(x, 27, "g")
    return c


stamp("hedge", "nature", _hedge(), 1, 2, note="a clipped myrtle hedge, the yard's back wall")

stamp("threshold", "floor", """
QQQQQQQQQQQQQQQQ
LLLLLLLLLLLLLLLq
LlllllllllllllLq
lllllllllllllllq
llllllylllllllyq
lllllllllllllllq
lllyllllllllllq.
lllllllllllllllq
llllllllllyllllq
lllllllllllllllq
qqqqqqqqqqqqqqqq
QQQQQQQQQQQQQQQQ
QqqqQqqqqQqqqqQq
QQQQQQQQQQQQQQQQ
gggggggggggggggg
gggggggggggggggg
""", 1, 1, walk={(0, 0)}, flatten=True,
      note="the limestone threshold and its step down into the yard (walkable)")

stamp("mat_single", "nature", """
................
................
................
.kkkkkkkkkkkkkk.
.kJJJJJJJJJJJJk.
.kJjKjjKjjKjjKk.
.kJKjjKjjKjjKjk.
.kJjjKjjKjjKjjk.
.kJjKjjKjjKjjKk.
.kJKjjKjjKjjKjk.
.kJjjKjjKjjKjjk.
.kjKKKKKKKKKKKk.
.kkkkkkkkkkkkkk.
................
................
................
""", 1, 1, walk={(0, 0)}, behavior={(0, 0): "MB_SOUTH_ARROW_WARP"},
      note="a reed mat for a one-tile door; a south-arrow warp")

stamp("ladder_lean", "wood", _ladder(hatch=False), 1, 3, note="a ladder leaning on the wall")
