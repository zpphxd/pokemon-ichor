"""Knossa's land: Cretan limestone cliffs and terrace walls, the Cave of
Eileithyia's mouth and the goat path up to it, the Bull Road's vineyard,
olive-terrace ledges, phrygana and thyme, the beekeeper's hut, the labrys
door and Ida's labrys gate.

The cliff and terrace kits are Kythera's (kythera_coast.cliff,
kythera_land.terrace), recolored from its pink stone into Cretan limestone
(knossa_lib.ROSE_TO_STONE): the same shapes, so the two islands' coasts read
as one world, in Crete's grey-gold stone. New pieces paint with
kythera_coast.stone_px through stone(), so they match the kits.
"""
from __future__ import annotations

import math

import knossa_lib as N
from knossa_lib import anim_layer, ground, grid, put, struct

SEC_LAND = "land"


def stone(X, Y, dark=0):
    import kythera_coast as Co
    return N.ROSE_TO_STONE.get(Co.stone_px(X, Y, dark), "cv0")


# --------------------------------------------------------------------------
# Kythera's kits in Cretan stone
# --------------------------------------------------------------------------

def cliff(key="cliff", names_only=None, notes_extra=""):
    import kythera_coast as Co
    src = Co.cliff()
    N.recolor(src, N.ROSE_TO_STONE)
    src.key = key
    src.title = "Low limestone cliffs"
    src.section = SEC_LAND
    src.notes = ("Crete's grey-gold limestone, Kythera's cliff kit in Knossa's stone. A cliff whose "
                 "face looks south is `lip` (the plateau's edge, on borrowed grass) over `face` "
                 "over a foot: `foot_sea` (borrowed sea, foam breaking at the base, animated), "
                 "`foot_sand` or `foot_grass` (walkable ground with fallen stones). `_L` / `_R` "
                 "end a run. Stack `face` rows for a taller cliff. The plateau's other edges: "
                 "`side_E` (plateau to the west, the drop to the east), `side_W`, `back` (plateau "
                 "to the south, the drop to the north, the face hidden), `back_NW` / `back_NE`; "
                 "`corner_in_E` / `_W` turn a south face into a side going north. `seep` is the "
                 "face where a spring runs out. Lip and face cells are impassable." + notes_extra)
    if names_only:
        return N.pick(src, names_only, w=8, key=key, notes=src.notes, section=SEC_LAND)
    return src


def terrace(key="terrace", title="Limestone terrace walls", notes=None):
    import kythera_land as La
    src = La.terrace()
    N.recolor(src, N.ROSE_TO_STONE)
    src.key = key
    src.title = title
    src.section = SEC_LAND
    src.notes = notes or (
        "A dry-stone retaining wall one cell high, Kythera's terrace kit in Cretan limestone. Lay "
        "a `top_*` row (the upper terrace's edge, walkable, on borrowed grass) above a wall row: "
        "`L` `M` (`M2`) `R`. `steps` cuts a stair through the wall (walkable) under `top_steps`. "
        "`niche` is an arched niche with a low plinth (a votive's); `spout` is a spring spout "
        "dribbling into a trough. Wall cells are impassable.")
    return src


# --------------------------------------------------------------------------
# The Cave of Eileithyia's mouth, and the goat path up the cliff
# --------------------------------------------------------------------------

def face_fill(L, ox, oy, w=16, h_=16, dark=0, b=0):
    for y in range(h_):
        for x in range(w):
            c = stone(ox + x + 5 * b, oy + y, dark)
            if y > 11 + (h_ - 16) and c in ("cs3", "cs4"):
                c = "cs2"
            L.px(ox + x, oy + y, c)


def lip_row(M, ox, oy, b=0):
    """Kythera's cliff brow in Cretan stone, over borrowed grass."""
    import kythera_coast as Co
    for x in range(16):
        top = 10 + int(round(Co.wob(x + 4 * b, 0.8) * 0.8))
        for y in range(top, 16):
            c = "cs5" if y == top else ("cs4" if y == top + 1 else stone(ox + x, oy + y))
            M.px(ox + x, oy + y, c)
        if (x * 7 + b) % 5 == 0:
            M.px(ox + x, oy + top, "my3")
            M.px(ox + x, oy + top - 1, "my2")


def cave_mouth():
    """3 x 3: the carved mouth in a two-row cliff face, and the goat path."""
    names = {"lip_L": (0, 0), "lip": (1, 0), "lip_R": (2, 0),
             "arch_L": (0, 1), "arch": (1, 1), "arch_R": (2, 1),
             "sill_L": (0, 2), "door": (1, 2), "sill_R": (2, 2),
             "stair_lip": (3, 0), "stair": (3, 1), "stair_foot": (3, 2)}
    s = struct("cave_mouth", "The Cave of Eileithyia's mouth, and the goat path", 4, 3,
               SEC_LAND, walk=["XXX.", "XXX.", "XDX."], names=names,
               notes="Set into a two-row stretch of the limestone cliff above Amnisos's west end "
                     "(SCRIPT.md Part 2; stack two `cliff.face` rows either side): the brow "
                     "(`lip_L` `lip` `lip_R`, on borrowed grass) over `arch_*` over `sill_L` "
                     "`door` `sill_R`. A low cave mouth, its jambs squared by old hands and cut "
                     "with double axes; clay figurines, a honey cake and a lamp left on the sill. "
                     "`door` is `MB_NON_ANIMATED_DOOR`, the warp into the cave. The goat path "
                     "climbs beside it: `stair_lip` over `stair` over `stair_foot`, rough steps "
                     "cut up the face (walkable; give them elevation 0, as for stairs).")
    ground(s, "grass", [(0, 0), (1, 0), (2, 0), (3, 0)])
    M, B = s.M, s.B
    for cx in range(4):
        lip_row(M, cx * 16, 0, cx)
    face_fill(B, 0, 16, 64, 32)
    # the mouth: an arch, rough at the edges
    cx0, top = 24, 19
    def half(y):
        if y < top:
            return -1
        yy = y - top
        if yy < 10:
            return 10.5 * math.sqrt(max(0.0, 1 - ((10 - yy) / 10.5) ** 2))
        return 10.5
    for y in range(16, 48):
        hw = half(y)
        if hw < 0:
            continue
        for x in range(0, 48):
            d = abs(x + 0.5 - cx0)
            jit = (N.h(x, y, 3) % 3) * 0.5
            if d < hw - jit:
                edge = hw - jit - d
                c = "cv0" if edge > 2.5 else "cs0"
                if y >= 45:
                    c = "cs1" if (x + y) % 3 else "cs0"
                B.px(x, y, c)
            elif d < hw - jit + 1.2:
                B.px(x, y, "cs1" if x < cx0 else "cs0")
        # the lit rim over the arch's crown
    for x in range(14, 35):
        for y in range(16, 48):
            if B.get(x, y) in ("cv0", "cs0") and B.get(x, y - 1) not in ("cv0", "cs0", "cs1", None):
                B.px(x, y - 1, "cs5")
                break
    # squared jambs, cut with double axes
    for (jx, lit) in ((10, True), (36, False)):
        for y in range(26, 47):
            for x in range(jx, jx + 3):
                c = ("cs4", "cs3", "cs2") if lit else ("cs3", "cs2", "cs1")
                B.px(x, y, c[x - jx])
        B.px(jx + (3 if lit else -1), 26, "cs1")
        grid(B, jx - 1 if lit else jx - 1, 30, [
            "c...c",
            "cc.cc",
            "ccccc",
            "cc.cc",
            "c.c.c",
            "..c..",
            "..c..",
        ], {"c": "cs0"})
    # the threshold slab, worn smooth, lit
    for x in range(13, 36):
        B.px(x, 44, "cs3")
        B.px(x, 45, "cs4" if (x + 1) % 7 else "cs3")
        B.px(x, 46, "cs3")
        B.px(x, 47, "cs1")
    # offerings beside the jambs and on the slab (middle layer: clay and honey)
    fig = [".k.k.", "k2.2k", ".k1k.", ".k1k.", "kk1kk"]
    lg = {"k": "mt0", "1": "mt1", "2": "mt2"}
    for fx in (4, 40):
        grid(M, fx, 41, fig, lg)
    grid(M, 6 + 1, 42, ["kk", "21", "kk"], lg) if False else None
    grid(M, 16, 43, [".kk.", "k21k", ".kk."], {"k": "mo0", "2": "mo2", "1": "mo1"})
    grid(M, 30, 42, ["..k.", ".k2k", "kk1k"], {"k": "mt0", "1": "mt1", "2": "mo1"})
    # the goat path: a worn notch in the lip, steps cut down the face
    ox = 48
    for x in range(5, 11):
        for y in range(11, 16):
            M.px(ox + x, y, "cs4" if y in (11, 14) else "cs3")
    for i in range(8):
        y0 = 16 + i * 4
        for x in range(4, 12):
            B.px(ox + x, y0, "cs5")
            B.px(ox + x, y0 + 1, "cs4")
            B.px(ox + x, y0 + 2, "cs3")
            B.px(ox + x, y0 + 3, "cs1")
        B.px(ox + 3, y0 + 1, "cs1")
        B.px(ox + 12, y0 + 2, "cs0")
    return s


def build_amnisos():
    return [cliff(), terrace(), cave_mouth()]
